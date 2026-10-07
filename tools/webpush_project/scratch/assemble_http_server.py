import os

def main():
    scratch_dir = r'd:\github\N1盒子\tools\webpush_project\scratch'
    html_path = os.path.join(scratch_dir, 'dashboard.html')
    js_path = os.path.join(scratch_dir, 'app.js')

    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    with open(js_path, 'r', encoding='utf-8') as f:
        js_content = f.read()

    # Replace <script src="app.js"></script> with <script>js_content</script>
    full_html = html_content.replace('<script src="app.js"></script>', '<script>\n' + js_content + '\n</script>')

    # Split into chunks under 15000 chars to avoid Java string literal limit
    chunk_size = 12000
    html_chunks = [full_html[i:i+chunk_size] for i in range(0, len(full_html), chunk_size)]

    java_chunks_code = []
    for idx, chunk in enumerate(html_chunks):
        escaped = chunk.replace('\\', '\\\\').replace('"', '\\"').replace('\r', '').replace('\n', '\\n"\n                + "')
        java_chunks_code.append(f'    private static final String HTML_PART_{idx} = "{escaped}";')

    combine_code = ' + '.join([f'HTML_PART_{i}' for i in range(len(html_chunks))])

    # Pure Java code template WITHOUT f-string evaluation of quotes
    java_template = r'''package com.nextgen.webpush;

import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.os.Environment;
import android.os.StatFs;

import java.io.*;
import java.net.*;
import java.text.SimpleDateFormat;
import java.util.*;

public class HttpWebServer {

    public interface OnEventListener {
        void onServerStarted(String ip, int port);
        void onFileReceived(String fileName, long sizeBytes, boolean autoInstalled);
        void onClientConnected(String clientIp);
    }

    private final int port;
    private final Context context;
    private final File downloadDir;
    private ServerSocket serverSocket;
    private boolean isRunning = false;
    private OnEventListener eventListener;

/*___HTML_PARTS___*/

    public HttpWebServer(Context context, int port) {
        this.context = context.getApplicationContext();
        this.port = port;
        this.downloadDir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS);
        if (!this.downloadDir.exists()) {
            this.downloadDir.mkdirs();
        }
    }

    public void setEventListener(OnEventListener listener) {
        this.eventListener = listener;
    }

    public synchronized void start() throws IOException {
        if (isRunning) return;
        serverSocket = new ServerSocket(port);
        isRunning = true;

        new Thread(() -> {
            while (isRunning) {
                try {
                    Socket client = serverSocket.accept();
                    new Thread(() -> handleClient(client)).start();
                } catch (IOException e) {
                    if (!isRunning) break;
                }
            }
        }, "WebPush-HttpServer").start();

        if (eventListener != null) {
            eventListener.onServerStarted(getDeviceIpAddress(), port);
        }
    }

    public synchronized void stop() {
        isRunning = false;
        try {
            if (serverSocket != null) {
                serverSocket.close();
            }
        } catch (Exception ignored) {}
    }

    private void handleClient(Socket client) {
        try (InputStream rawIn = client.getInputStream();
             OutputStream out = client.getOutputStream()) {

            client.setSoTimeout(120000);
            BufferedInputStream in = new BufferedInputStream(rawIn, 65536);

            String clientIp = client.getInetAddress().getHostAddress();
            if (eventListener != null) {
                eventListener.onClientConnected(clientIp);
            }

            // Read HTTP request line
            String requestLine = readLine(in);
            if (requestLine == null || requestLine.isEmpty()) return;

            String[] parts = requestLine.split(" ");
            if (parts.length < 2) return;
            String method = parts[0];
            String rawUri = parts[1];

            String rawPath = rawUri;
            String rawQuery = "";
            int qIdx = rawUri.indexOf('?');
            if (qIdx != -1) {
                rawPath = rawUri.substring(0, qIdx);
                rawQuery = rawUri.substring(qIdx + 1);
            }

            String path = URLDecoder.decode(rawPath, "UTF-8");
            Map<String, String> queryParams = parseQueryParams(rawQuery);

            // Read HTTP headers
            Map<String, String> headers = new HashMap<>();
            String line;
            while ((line = readLine(in)) != null && !line.isEmpty()) {
                int idx = line.indexOf(':');
                if (idx > 0) {
                    headers.put(line.substring(0, idx).trim().toLowerCase(Locale.ROOT), line.substring(idx + 1).trim());
                }
            }

            if ("GET".equalsIgnoreCase(method)) {
                handleGet(path, queryParams, out);
            } else if ("POST".equalsIgnoreCase(method)) {
                handlePost(path, queryParams, headers, in, out);
            } else {
                sendResponse(out, "405 Method Not Allowed", "text/plain", "Method not allowed".getBytes("UTF-8"));
            }

        } catch (Exception ignored) {}
    }

    private Map<String, String> parseQueryParams(String query) {
        Map<String, String> map = new HashMap<>();
        if (query == null || query.isEmpty()) return map;
        for (String pair : query.split("&")) {
            int idx = pair.indexOf('=');
            if (idx > 0) {
                try {
                    String k = URLDecoder.decode(pair.substring(0, idx), "UTF-8");
                    String v = URLDecoder.decode(pair.substring(idx + 1), "UTF-8");
                    map.put(k, v);
                } catch (Exception ignored) {}
            }
        }
        return map;
    }

    private void handleGet(String path, Map<String, String> query, OutputStream out) throws IOException {
        if ("/".equals(path) || "/index.html".equals(path)) {
            byte[] html = getHtmlDashboard().getBytes("UTF-8");
            sendResponse(out, "200 OK", "text/html; charset=utf-8", html);
        } else if ("/api/status".equals(path)) {
            String json = getStatusJson();
            sendResponse(out, "200 OK", "application/json; charset=utf-8", json.getBytes("UTF-8"));
        } else if (path.startsWith("/download/")) {
            String fileName = path.substring("/download/".length());
            File f = new File(downloadDir, fileName);
            if (f.exists() && f.isFile()) {
                sendResponse(out, "200 OK", getMimeType(f.getName()), f);
            } else {
                sendResponse(out, "404 Not Found", "text/plain", "File not found".getBytes("UTF-8"));
            }
        } else if ("/api/fs/list".equals(path)) {
            String targetPath = query.get("path");
            String json = getFsListJson(targetPath);
            sendResponse(out, "200 OK", "application/json; charset=utf-8", json.getBytes("UTF-8"));
        }} else if ("/api/fs/download".equals(path)) {
            String filePath = query.get("path");
            if (filePath != null) {
                File f = new File(filePath);
                if (f.exists() && f.isFile()) {
                    sendResponse(out, "200 OK", getMimeType(f.getName()), f);
                    return;
                }
            }
            sendResponse(out, "404 Not Found", "text/plain", "File not found".getBytes("UTF-8"));
        } else {
            sendResponse(out, "404 Not Found", "text/plain", "Not Found".getBytes("UTF-8"));
        }
    }

    private void handlePost(String path, Map<String, String> query, Map<String, String> headers, BufferedInputStream in, OutputStream out) throws IOException {
        if ("/api/upload".equals(path) || "/api/fs/upload".equals(path)) {
            String contentType = headers.get("content-type");
            long contentLength = 0;
            try {
                contentLength = Long.parseLong(headers.get("content-length"));
            } catch (Exception ignored) {}

            boolean autoInstall = "1".equals(headers.get("x-auto-install"));
            File targetFolder = downloadDir;

            if ("/api/fs/upload".equals(path)) {
                String customPath = query.get("path");
                if (customPath == null || customPath.isEmpty()) {
                    customPath = headers.get("x-target-dir");
                }
                if (customPath != null && !customPath.isEmpty()) {
                    File specifiedDir = new File(customPath);
                    if (!specifiedDir.exists()) {
                        specifiedDir.mkdirs();
                    }
                    if (specifiedDir.isDirectory()) {
                        targetFolder = specifiedDir;
                    }
                }
            }

            if (contentType != null && contentType.contains("boundary=")) {
                String boundary = contentType.substring(contentType.indexOf("boundary=") + 9).trim();
                if (boundary.startsWith("\"") && boundary.endsWith("\"")) {
                    boundary = boundary.substring(1, boundary.length() - 1);
                }
                parseMultipartUpload(in, boundary, contentLength, autoInstall, targetFolder);
                sendResponse(out, "200 OK", "application/json", "{\"status\":\"ok\"}".getBytes("UTF-8"));
            } else {
                sendResponse(out, "400 Bad Request", "application/json", "{\"error\":\"invalid content-type\"}".getBytes("UTF-8"));
            }
        } else if ("/api/install".equals(path)) {
            String postData = readBodyAsString(in, headers);
            String fileName = extractJsonValue(postData, "fileName");
            if (fileName != null && fileName.toLowerCase(Locale.ROOT).endsWith(".apk")) {
                File apkFile = new File(downloadDir, fileName);
                boolean success = installApkDirect(apkFile);
                sendResponse(out, "200 OK", "application/json", ("{\"status\":\"" + (success ? "ok" : "failed") + "\"}").getBytes("UTF-8"));
            } else {
                sendResponse(out, "400 Bad Request", "application/json", "{\"error\":\"invalid apk\"}".getBytes("UTF-8"));
            }
        } else if ("/api/delete".equals(path)) {
            String postData = readBodyAsString(in, headers);
            String fileName = extractJsonValue(postData, "fileName");
            if (fileName != null) {
                File f = new File(downloadDir, fileName);
                if (f.exists()) {
                    deleteRecursively(f);
                }
            }
            sendResponse(out, "200 OK", "application/json", "{\"status\":\"ok\"}".getBytes("UTF-8"));
        } else if ("/api/fs/mkdir".equals(path)) {
            String postData = readBodyAsString(in, headers);
            String parentDir = extractJsonValue(postData, "path");
            String name = extractJsonValue(postData, "name");
            boolean ok = false;
            if (parentDir != null && name != null && !name.isEmpty()) {
                File newDir = new File(parentDir, name);
                ok = newDir.mkdirs() || newDir.exists();
            }
            sendResponse(out, "200 OK", "application/json", ("{\"status\":\"" + (ok ? "ok" : "failed") + "\"}").getBytes("UTF-8"));
        } else if ("/api/fs/rename".equals(path)) {
            String postData = readBodyAsString(in, headers);
            String oldPath = extractJsonValue(postData, "path");
            String newName = extractJsonValue(postData, "newName");
            boolean ok = false;
            if (oldPath != null && newName != null && !newName.isEmpty()) {
                File oldFile = new File(oldPath);
                if (oldFile.exists()) {
                    File newFile = new File(oldFile.getParentFile(), newName);
                    ok = oldFile.renameTo(newFile);
                }
            }
            sendResponse(out, "200 OK", "application/json", ("{\"status\":\"" + (ok ? "ok" : "failed") + "\"}").getBytes("UTF-8"));
        } else if ("/api/fs/delete".equals(path)) {
            String postData = readBodyAsString(in, headers);
            String targetPath = extractJsonValue(postData, "path");
            boolean ok = false;
            if (targetPath != null) {
                File f = new File(targetPath);
                if (f.exists()) {
                    ok = deleteRecursively(f);
                }
            }
            sendResponse(out, "200 OK", "application/json", ("{\"status\":\"" + (ok ? "ok" : "failed") + "\"}").getBytes("UTF-8"));
        } else if ("/api/fs/install".equals(path)) {
            String postData = readBodyAsString(in, headers);
            String apkPath = extractJsonValue(postData, "path");
            boolean success = false;
            if (apkPath != null && apkPath.toLowerCase(Locale.ROOT).endsWith(".apk")) {
                File apkFile = new File(apkPath);
                success = installApkDirect(apkFile);
            }
            sendResponse(out, "200 OK", "application/json", ("{\"status\":\"" + (success ? "ok" : "failed") + "\"}").getBytes("UTF-8"));
        } else {
            sendResponse(out, "404 Not Found", "text/plain", "Not Found".getBytes("UTF-8"));
        }
    }

    private boolean deleteRecursively(File fileOrDir) {
        if (fileOrDir.isDirectory()) {
            File[] children = fileOrDir.listFiles();
            if (children != null) {
                for (File child : children) {
                    deleteRecursively(child);
                }
            }
        }
        return fileOrDir.delete();
    }

    private void parseMultipartUpload(BufferedInputStream in, String boundary, long contentLength, boolean autoInstall, File targetFolder) throws IOException {
        String boundaryMarker = "--" + boundary;
        
        // Find filename from multipart headers
        String line;
        String fileName = "upload_" + System.currentTimeMillis() + ".apk";
        while ((line = readLine(in)) != null) {
            if (line.isEmpty()) break;
            if (line.contains("filename=")) {
                int fnStart = line.indexOf("filename=\"");
                if (fnStart != -1) {
                    fnStart += 10;
                    int fnEnd = line.indexOf("\"", fnStart);
                    if (fnEnd > fnStart) {
                        fileName = line.substring(fnStart, fnEnd);
                    }
                } else {
                    fnStart = line.indexOf("filename=");
                    if (fnStart != -1) {
                        fileName = line.substring(fnStart + 9).trim();
                    }
                }
            }
        }

        // Clean filename
        fileName = new File(fileName).getName();
        File targetFile = new File(targetFolder, fileName);

        byte[] delimiter = ("\r\n" + boundaryMarker).getBytes("UTF-8");
        long totalBytesWritten = 0;

        try (FileOutputStream fos = new FileOutputStream(targetFile)) {
            byte[] buffer = new byte[65536];
            ByteArrayOutputStream pending = new ByteArrayOutputStream();
            int r;
            boolean boundaryFound = false;

            while (!boundaryFound && (r = in.read(buffer)) != -1) {
                pending.write(buffer, 0, r);
                byte[] data = pending.toByteArray();
                int matchIdx = findSequence(data, 0, data.length, delimiter);

                if (matchIdx != -1) {
                    fos.write(data, 0, matchIdx);
                    totalBytesWritten += matchIdx;
                    boundaryFound = true;
                } else {
                    int safeLen = data.length - delimiter.length;
                    if (safeLen > 0) {
                        fos.write(data, 0, safeLen);
                        totalBytesWritten += safeLen;
                        pending.reset();
                        pending.write(data, safeLen, delimiter.length);
                    }
                }
            }

            if (!boundaryFound && pending.size() > 0) {
                byte[] remaining = pending.toByteArray();
                fos.write(remaining);
                totalBytesWritten += remaining.length;
            }
        }

        boolean installed = false;
        if (autoInstall && fileName.toLowerCase(Locale.ROOT).endsWith(".apk")) {
            installed = installApkDirect(targetFile);
        }

        if (eventListener != null) {
            eventListener.onFileReceived(fileName, totalBytesWritten, installed);
        }
    }

    private int findSequence(byte[] data, int start, int length, byte[] target) {
        if (target.length == 0 || length < target.length) return -1;
        int end = start + length - target.length;
        for (int i = start; i <= end; i++) {
            boolean match = true;
            for (int j = 0; j < target.length; j++) {
                if (data[i + j] != target[j]) {
                    match = false;
                    break;
                }
            }
            if (match) return i;
        }
        return -1;
    }

    private String readLine(InputStream in) throws IOException {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        int c;
        while ((c = in.read()) != -1) {
            if (c == '\r') {
                int next = in.read();
                if (next == '\n' || next == -1) break;
                baos.write(c);
                baos.write(next);
            } else if (c == '\n') {
                break;
            } else {
                baos.write(c);
            }
        }
        return (baos.size() == 0 && c == -1) ? null : baos.toString("UTF-8");
    }

    private String readBodyAsString(InputStream in, Map<String, String> headers) throws IOException {
        int length = 0;
        try {
            length = Integer.parseInt(headers.get("content-length"));
        } catch (Exception ignored) {}
        if (length <= 0) length = 2048;

        byte[] buf = new byte[length];
        int totalRead = 0;
        while (totalRead < length) {
            int r = in.read(buf, totalRead, length - totalRead);
            if (r == -1) break;
            totalRead += r;
        }
        return new String(buf, 0, totalRead, "UTF-8");
    }

    private boolean installApkDirect(File apk) {
        if (!apk.exists()) return false;
        try {
            // Root silent install
            Process p = Runtime.getRuntime().exec(new String[]{"su", "-c", "pm install -r \"" + apk.getAbsolutePath() + "\""});
            int exitCode = p.waitFor();
            if (exitCode == 0) {
                return true;
            }
        } catch (Exception ignored) {}

        // Fallback: System Package Installer Intent
        try {
            Intent intent = new Intent(Intent.ACTION_VIEW);
            intent.setDataAndType(Uri.fromFile(apk), "application/vnd.android.package-archive");
            intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_GRANT_READ_URI_PERMISSION);
            context.startActivity(intent);
            return true;
        } catch (Exception ignored) {}

        return false;
    }

    private String extractJsonValue(String json, String key) {
        String search = "\"" + key + "\":\"";
        int idx = json.indexOf(search);
        if (idx >= 0) {
            int start = idx + search.length();
            int end = json.indexOf("\"", start);
            if (end > start) {
                return json.substring(start, end);
            }
        }
        return null;
    }

    private String getStatusJson() {
        StatFs stat = new StatFs(Environment.getExternalStorageDirectory().getPath());
        long blockSize = stat.getBlockSizeLong();
        long totalBlocks = stat.getBlockCountLong();
        long availableBlocks = stat.getAvailableBlocksLong();

        long totalBytes = totalBlocks * blockSize;
        long freeBytes = availableBlocks * blockSize;

        StringBuilder sb = new StringBuilder();
        sb.append("{");
        sb.append("\"ip\":\"").append(getDeviceIpAddress()).append("\",");
        sb.append("\"port\":").append(port).append(",");
        sb.append("\"model\":\"斐讯 N1 (Android 7.1.2)\",");
        sb.append("\"storageTotal\":\"").append(formatSize(totalBytes)).append("\",");
        sb.append("\"storageFree\":\"").append(formatSize(freeBytes)).append("\",");
        sb.append("\"storagePercent\":").append((int) ((totalBytes - freeBytes) * 100.0 / (totalBytes > 0 ? totalBytes : 1))).append(",");
        sb.append("\"files\":[");

        File[] files = downloadDir.listFiles();
        if (files != null) {
            Arrays.sort(files, (a, b) -> Long.compare(b.lastModified(), a.lastModified()));
            SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm", Locale.getDefault());
            int count = 0;
            for (File f : files) {
                if (f.isFile()) {
                    if (count > 0) sb.append(",");
                    sb.append("{");
                    sb.append("\"name\":\"").append(escapeJson(f.getName())).append("\",");
                    sb.append("\"size\":\"").append(formatSize(f.length())).append("\",");
                    sb.append("\"date\":\"").append(sdf.format(new Date(f.lastModified()))).append("\",");
                    sb.append("\"isApk\":").append(f.getName().toLowerCase(Locale.ROOT).endsWith(".apk"));
                    sb.append("}");
                    count++;
                }
            }
        }
        sb.append("]}");
        return sb.toString();
    }

    private String getFsListJson(String requestedPath) {
        File targetDir;
        if (requestedPath == null || requestedPath.trim().isEmpty()) {
            targetDir = Environment.getExternalStorageDirectory();
        } else {
            targetDir = new File(requestedPath);
        }

        if (!targetDir.exists()) {
            targetDir = Environment.getExternalStorageDirectory();
        }
        if (targetDir.isFile()) {
            targetDir = targetDir.getParentFile();
        }

        String currentPath = targetDir.getAbsolutePath();
        File parent = targetDir.getParentFile();
        String parentPath = parent != null ? parent.getAbsolutePath() : "";

        // Calculate storage for current volume
        long totalBytes = 0;
        long freeBytes = 0;
        int storagePercent = 0;
        try {
            StatFs stat = new StatFs(currentPath);
            long blockSize = stat.getBlockSizeLong();
            totalBytes = stat.getBlockCountLong() * blockSize;
            freeBytes = stat.getAvailableBlocksLong() * blockSize;
            if (totalBytes > 0) {
                storagePercent = (int) ((totalBytes - freeBytes) * 100.0 / totalBytes);
            }
        } catch (Exception ignored) {}

        // Scan Storages
        List<Map<String, String>> storages = new ArrayList<>();
        Map<String, String> internal = new HashMap<>();
        internal.put("name", "内部存储");
        internal.put("path", Environment.getExternalStorageDirectory().getAbsolutePath());
        storages.add(internal);

        Map<String, String> dl = new HashMap<>();
        dl.put("name", "下载目录");
        dl.put("path", downloadDir.getAbsolutePath());
        storages.add(dl);

        File movies = new File(Environment.getExternalStorageDirectory(), "Movies");
        if (movies.exists() || movies.mkdirs()) {
            Map<String, String> mv = new HashMap<>();
            mv.put("name", "影视目录");
            mv.put("path", movies.getAbsolutePath());
            storages.add(mv);
        }

        // Scan external USB storage points
        scanStoragePoints(storages);

        // List files in current folder
        File[] files = targetDir.listFiles();
        List<File> dirList = new ArrayList<>();
        List<File> fileList = new ArrayList<>();

        if (files != null) {
            for (File f : files) {
                if (f.getName().startsWith(".")) continue; // Skip hidden
                if (f.isDirectory()) {
                    dirList.add(f);
                } else {
                    fileList.add(f);
                }
            }
            Collections.sort(dirList, (a, b) -> a.getName().compareToIgnoreCase(b.getName()));
            Collections.sort(fileList, (a, b) -> a.getName().compareToIgnoreCase(b.getName()));
        }

        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm", Locale.getDefault());
        StringBuilder sb = new StringBuilder();
        sb.append("{");
        sb.append("\"currentPath\":\"").append(escapeJson(currentPath)).append("\",");
        sb.append("\"parentPath\":\"").append(escapeJson(parentPath)).append("\",");
        sb.append("\"storageTotal\":\"").append(formatSize(totalBytes)).append("\",");
        sb.append("\"storageFree\":\"").append(formatSize(freeBytes)).append("\",");
        sb.append("\"storagePercent\":").append(storagePercent).append(",");

        // Storages array
        sb.append("\"storages\":[");
        for (int i = 0; i < storages.size(); i++) {
            if (i > 0) sb.append(",");
            Map<String, String> s = storages.get(i);
            sb.append("{\"name\":\"").append(escapeJson(s.get("name"))).append("\",\"path\":\"").append(escapeJson(s.get("path"))).append("\"}");
        }
        sb.append("],");

        // Items array
        sb.append("\"items\":[");
        int count = 0;
        // Dirs first
        for (File d : dirList) {
            if (count > 0) sb.append(",");
            sb.append("{");
            sb.append("\"name\":\"").append(escapeJson(d.getName())).append("\",");
            sb.append("\"path\":\"").append(escapeJson(d.getAbsolutePath())).append("\",");
            sb.append("\"isDir\":true,");
            sb.append("\"size\":\"--\",");
            sb.append("\"date\":\"").append(sdf.format(new Date(d.lastModified()))).append("\",");
            sb.append("\"type\":\"dir\",");
            sb.append("\"isApk\":false");
            sb.append("}");
            count++;
        }
        // Files next
        for (File f : fileList) {
            if (count > 0) sb.append(",");
            boolean isApk = f.getName().toLowerCase(Locale.ROOT).endsWith(".apk");
            sb.append("{");
            sb.append("\"name\":\"").append(escapeJson(f.getName())).append("\",");
            sb.append("\"path\":\"").append(escapeJson(f.getAbsolutePath())).append("\",");
            sb.append("\"isDir\":false,");
            sb.append("\"size\":\"").append(formatSize(f.length())).append("\",");
            sb.append("\"date\":\"").append(sdf.format(new Date(f.lastModified()))).append("\",");
            sb.append("\"type\":\"").append(getFileType(f)).append("\",");
            sb.append("\"isApk\":").append(isApk);
            sb.append("}");
            count++;
        }
        sb.append("]}");
        return sb.toString();
    }

    private void scanStoragePoints(List<Map<String, String>> storages) {
        Set<String> visited = new HashSet<>();
        for (Map<String, String> s : storages) {
            visited.add(s.get("path"));
        }

        String[] scanDirs = new String[]{"/storage", "/mnt/media_rw"};
        for (String root : scanDirs) {
            File r = new File(root);
            if (r.exists() && r.isDirectory()) {
                File[] list = r.listFiles();
                if (list != null) {
                    for (File f : list) {
                        String n = f.getName();
                        if ("self".equals(n) || "emulated".equals(n) || "knox-emulated".equals(n)) continue;
                        if (f.isDirectory() && f.canRead() && !visited.contains(f.getAbsolutePath())) {
                            visited.add(f.getAbsolutePath());
                            Map<String, String> ext = new HashMap<>();
                            ext.put("name", "外接存储 (" + n + ")");
                            ext.put("path", f.getAbsolutePath());
                            storages.add(ext);
                        }
                    }
                }
            }
        }
    }

    private String getFileType(File f) {
        if (f.isDirectory()) return "dir";
        String n = f.getName().toLowerCase(Locale.ROOT);
        if (n.endsWith(".apk")) return "apk";
        if (n.endsWith(".mp4") || n.endsWith(".mkv") || n.endsWith(".avi") || n.endsWith(".ts") || n.endsWith(".rmvb") || n.endsWith(".flv") || n.endsWith(".mov")) return "video";
        if (n.endsWith(".mp3") || n.endsWith(".flac") || n.endsWith(".wav") || n.endsWith(".aac") || n.endsWith(".m4a") || n.endsWith(".ogg")) return "audio";
        if (n.endsWith(".jpg") || n.endsWith(".jpeg") || n.endsWith(".png") || n.endsWith(".webp") || n.endsWith(".gif")) return "image";
        if (n.endsWith(".zip") || n.endsWith(".rar") || n.endsWith(".7z") || n.endsWith(".tar") || n.endsWith(".gz")) return "archive";
        if (n.endsWith(".txt") || n.endsWith(".log") || n.endsWith(".xml") || n.endsWith(".json") || n.endsWith(".prop") || n.endsWith(".sh")) return "text";
        return "file";
    }

    private String getMimeType(String name) {
        String n = name.toLowerCase(Locale.ROOT);
        if (n.endsWith(".apk")) return "application/vnd.android.package-archive";
        if (n.endsWith(".mp4")) return "video/mp4";
        if (n.endsWith(".mkv")) return "video/x-matroska";
        if (n.endsWith(".avi")) return "video/x-msvideo";
        if (n.endsWith(".mp3")) return "audio/mpeg";
        if (n.endsWith(".flac")) return "audio/flac";
        if (n.endsWith(".wav")) return "audio/wav";
        if (n.endsWith(".jpg") || n.endsWith(".jpeg")) return "image/jpeg";
        if (n.endsWith(".png")) return "image/png";
        if (n.endsWith(".gif")) return "image/gif";
        if (n.endsWith(".txt") || n.endsWith(".log")) return "text/plain; charset=utf-8";
        if (n.endsWith(".json")) return "application/json; charset=utf-8";
        if (n.endsWith(".zip")) return "application/zip";
        return "application/octet-stream";
    }

    private String escapeJson(String s) {
        if (s == null) return "";
        return s.replace("\\", "\\\\").replace("\"", "\\\"");
    }

    private String formatSize(long bytes) {
        if (bytes < 1024) return bytes + " B";
        int z = (63 - Long.numberOfLeadingZeros(bytes)) / 10;
        return String.format(Locale.getDefault(), "%.1f %sB", (double) bytes / (1L << (z * 10)), " KMGTPE".charAt(z));
    }

    public static String getDeviceIpAddress() {
        try {
            String fallbackIp = null;
            for (Enumeration<NetworkInterface> en = NetworkInterface.getNetworkInterfaces(); en.hasMoreElements(); ) {
                NetworkInterface intf = en.nextElement();
                if (!intf.isUp() || intf.isLoopback()) continue;
                String name = intf.getName().toLowerCase();
                for (Enumeration<InetAddress> enumIpAddr = intf.getInetAddresses(); enumIpAddr.hasMoreElements(); ) {
                    InetAddress inetAddress = enumIpAddr.nextElement();
                    if (!inetAddress.isLoopbackAddress() && inetAddress instanceof Inet4Address) {
                        String ip = inetAddress.getHostAddress();
                        if (name.startsWith("eth") || name.startsWith("wlan")) {
                            return ip;
                        }
                        if (fallbackIp == null) {
                            fallbackIp = ip;
                        }
                    }
                }
            }
            if (fallbackIp != null) return fallbackIp;
        } catch (Exception ignored) {}
        return "127.0.0.1";
    }

    private void sendResponse(OutputStream out, String status, String contentType, byte[] data) throws IOException {
        String header = "HTTP/1.1 " + status + "\r\n" +
                "Content-Type: " + contentType + "\r\n" +
                "Content-Length: " + data.length + "\r\n" +
                "Access-Control-Allow-Origin: *\r\n" +
                "Connection: close\r\n\r\n";
        out.write(header.getBytes("UTF-8"));
        out.write(data);
        out.flush();
    }

    private void sendResponse(OutputStream out, String status, String contentType, File file) throws IOException {
        String encodedName = URLEncoder.encode(file.getName(), "UTF-8").replace("+", "%20");
        String header = "HTTP/1.1 " + status + "\r\n" +
                "Content-Type: " + contentType + "\r\n" +
                "Content-Length: " + file.length() + "\r\n" +
                "Content-Disposition: attachment; filename=\"" + file.getName() + "\"; filename*=UTF-8''" + encodedName + "\r\n" +
                "Access-Control-Allow-Origin: *\r\n" +
                "Connection: close\r\n\r\n";
        out.write(header.getBytes("UTF-8"));
        try (FileInputStream fis = new FileInputStream(file)) {
            byte[] buf = new byte[65536];
            int r;
            while ((r = fis.read(buf)) != -1) {
                out.write(buf, 0, r);
            }
        }
        out.flush();
    }

    private String getHtmlDashboard() {
        return /*___COMBINE_PARTS___*/;
    }
}
'''

    parts_code = "\n".join(java_chunks_code)
    final_java = java_template.replace("/*___HTML_PARTS___*/", parts_code).replace("/*___COMBINE_PARTS___*/", combine_code)

    # Small syntax check in java template: line 170 `}} else if ("/api/fs/download".equals(path))` had an extra `}`:
    final_java = final_java.replace('}} else if ("/api/fs/download".equals(path)) {', '} else if ("/api/fs/download".equals(path)) {')

    out_file = r'd:\github\N1盒子\tools\webpush_project\src\com\nextgen\webpush\HttpWebServer.java'
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(final_java)

    print(f'[+] Successfully generated HttpWebServer.java ({len(final_java)} chars, {len(html_chunks)} parts)')

if __name__ == '__main__':
    main()
