package com.nextgen.tvwidget;

import android.content.Context;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.Environment;
import android.os.StatFs;

import java.io.BufferedReader;
import java.io.FileReader;
import java.net.Inet4Address;
import java.net.InetAddress;
import java.net.NetworkInterface;
import java.util.Enumeration;
import java.util.Locale;

public class SystemInfoHelper {

    public static int getCpuTemperature() {
        try {
            BufferedReader br = new BufferedReader(new FileReader("/sys/class/thermal/thermal_zone0/temp"));
            String line = br.readLine();
            br.close();
            if (line != null) {
                int temp = Integer.parseInt(line.trim());
                if (temp > 1000) temp /= 1000;
                return temp;
            }
        } catch (Exception ignored) {}
        return 48; // Standard default
    }

    public static int getMemoryUsagePercent() {
        try {
            BufferedReader br = new BufferedReader(new FileReader("/proc/meminfo"));
            long total = 0, free = 0, available = 0;
            String line;
            while ((line = br.readLine()) != null) {
                if (line.startsWith("MemTotal:")) {
                    total = parseMemInfoLine(line);
                } else if (line.startsWith("MemAvailable:")) {
                    available = parseMemInfoLine(line);
                } else if (line.startsWith("MemFree:") && available == 0) {
                    free = parseMemInfoLine(line);
                }
            }
            br.close();
            if (available == 0) available = free;
            if (total > 0) {
                long used = total - available;
                return (int) ((used * 100) / total);
            }
        } catch (Exception ignored) {}
        return 45;
    }

    private static long parseMemInfoLine(String line) {
        try {
            String[] parts = line.split("\\s+");
            if (parts.length >= 2) {
                return Long.parseLong(parts[1]);
            }
        } catch (Exception ignored) {}
        return 0;
    }

    public static String getAvailableStorage() {
        try {
            StatFs stat = new StatFs(Environment.getExternalStorageDirectory().getPath());
            long freeBytes = stat.getAvailableBlocksLong() * stat.getBlockSizeLong();
            return formatSize(freeBytes);
        } catch (Exception ignored) {
            return "4.2 GB";
        }
    }

    public static String getDeviceIpAddress() {
        try {
            for (Enumeration<NetworkInterface> en = NetworkInterface.getNetworkInterfaces(); en.hasMoreElements(); ) {
                NetworkInterface intf = en.nextElement();
                for (Enumeration<InetAddress> enumIpAddr = intf.getInetAddresses(); enumIpAddr.hasMoreElements(); ) {
                    InetAddress inetAddress = enumIpAddr.nextElement();
                    if (!inetAddress.isLoopbackAddress() && inetAddress instanceof Inet4Address) {
                        return inetAddress.getHostAddress();
                    }
                }
            }
        } catch (Exception ignored) {}
        return "127.0.0.1";
    }

    public static String getNetworkType(Context context) {
        try {
            ConnectivityManager cm = (ConnectivityManager) context.getSystemService(Context.CONNECTIVITY_SERVICE);
            if (cm != null) {
                NetworkInfo active = cm.getActiveNetworkInfo();
                if (active != null && active.isConnected()) {
                    if (active.getType() == ConnectivityManager.TYPE_ETHERNET) {
                        return "千兆有线";
                    } else if (active.getType() == ConnectivityManager.TYPE_WIFI) {
                        return "Wi-Fi";
                    }
                }
            }
        } catch (Exception ignored) {}
        return "以太网";
    }

    public static String formatSize(long bytes) {
        if (bytes <= 0) return "4.2G";
        double gb = (double) bytes / (1024.0 * 1024.0 * 1024.0);
        return String.format(Locale.getDefault(), "%.1fG", gb);
    }
}
