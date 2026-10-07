package com.nextgen.webpush;

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

    private static final String HTML_PART_0 = "<!DOCTYPE html>\n"
                + "<html lang=\"zh-CN\">\n"
                + "<head>\n"
                + "  <meta charset=\"UTF-8\">\n"
                + "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no\">\n"
                + "  <title>NextGen 隔空传装 & 盒子管家 - 斐讯 N1</title>\n"
                + "  <style>\n"
                + "    :root {\n"
                + "      --bg: #090d16;\n"
                + "      --card-bg: rgba(22, 29, 47, 0.72);\n"
                + "      --card-border: rgba(255, 255, 255, 0.08);\n"
                + "      --primary: #06b6d4;\n"
                + "      --primary-hover: #22d3ee;\n"
                + "      --accent: #8b5cf6;\n"
                + "      --accent-hover: #a78bfa;\n"
                + "      --text: #f8fafc;\n"
                + "      --text-dim: #94a3b8;\n"
                + "      --danger: #ef4444;\n"
                + "      --danger-bg: rgba(239, 68, 68, 0.15);\n"
                + "      --success: #10b981;\n"
                + "      --hover-bg: rgba(255, 255, 255, 0.04);\n"
                + "    }\n"
                + "    * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }\n"
                + "    body {\n"
                + "      background: radial-gradient(circle at 80% -20%, #2e1065 0%, transparent 50%),\n"
                + "                  radial-gradient(circle at 10% 20%, #083344 0%, transparent 40%),\n"
                + "                  var(--bg);\n"
                + "      color: var(--text);\n"
                + "      min-height: 100vh;\n"
                + "      display: flex;\n"
                + "      flex-direction: column;\n"
                + "      align-items: center;\n"
                + "      padding: 20px 16px 40px;\n"
                + "    }\n"
                + "    .container { width: 100%; max-width: 980px; display: flex; flex-direction: column; gap: 16px; }\n"
                + "\n"
                + "    /* Header & Nav */\n"
                + "    header {\n"
                + "      display: flex;\n"
                + "      flex-wrap: wrap;\n"
                + "      justify-content: space-between;\n"
                + "      align-items: center;\n"
                + "      gap: 12px;\n"
                + "      padding: 4px 6px;\n"
                + "    }\n"
                + "    .brand {\n"
                + "      display: flex;\n"
                + "      align-items: center;\n"
                + "      gap: 10px;\n"
                + "      font-size: 21px;\n"
                + "      font-weight: 700;\n"
                + "      background: linear-gradient(135deg, #38bdf8 0%, #a855f7 100%);\n"
                + "      -webkit-background-clip: text;\n"
                + "      -webkit-text-fill-color: transparent;\n"
                + "    }\n"
                + "    .badge-online {\n"
                + "      font-size: 12px;\n"
                + "      padding: 4px 10px;\n"
                + "      border-radius: 999px;\n"
                + "      background: rgba(16, 185, 129, 0.12);\n"
                + "      border: 1px solid rgba(16, 185, 129, 0.3);\n"
                + "      color: #34d399;\n"
                + "      font-weight: 600;\n"
                + "      display: flex;\n"
                + "      align-items: center;\n"
                + "      gap: 6px;\n"
                + "    }\n"
                + "    .badge-dot { width: 7px; height: 7px; border-radius: 50%; background: #10b981; box-shadow: 0 0 8px #10b981; }\n"
                + "\n"
                + "    /* Segmented Tabs */\n"
                + "    .tab-bar {\n"
                + "      display: flex;\n"
                + "      background: rgba(15, 23, 42, 0.8);\n"
                + "      border: 1px solid var(--card-border);\n"
                + "      padding: 4px;\n"
                + "      border-radius: 12px;\n"
                + "      gap: 4px;\n"
                + "      margin-bottom: 4px;\n"
                + "    }\n"
                + "    .tab-btn {\n"
                + "      flex: 1;\n"
                + "      padding: 9px 18px;\n"
                + "      font-size: 14px;\n"
                + "      font-weight: 600;\n"
                + "      color: var(--text-dim);\n"
                + "      background: transparent;\n"
                + "      border: none;\n"
                + "      border-radius: 8px;\n"
                + "      cursor: pointer;\n"
                + "      display: flex;\n"
                + "      align-items: center;\n"
                + "      justify-content: center;\n"
                + "      gap: 8px;\n"
                + "      transition: all 0.2s ease;\n"
                + "    }\n"
                + "    .tab-btn:hover { color: var(--text); background: rgba(255, 255, 255, 0.03); }\n"
                + "    .tab-btn.active {\n"
                + "      color: #fff;\n"
                + "      background: linear-gradient(135deg, rgba(6, 182, 212, 0.25), rgba(139, 92, 246, 0.25));\n"
                + "      border: 1px solid rgba(56, 189, 248, 0.3);\n"
                + "      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.3);\n"
                + "    }\n"
                + "\n"
                + "    /* Cards */\n"
                + "    .card {\n"
                + "      background: var(--card-bg);\n"
                + "      backdrop-filter: blur(16px);\n"
                + "      -webkit-backdrop-filter: blur(16px);\n"
                + "      border: 1px solid var(--card-border);\n"
                + "      border-radius: 16px;\n"
                + "      padding: 20px;\n"
                + "      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);\n"
                + "      display: flex;\n"
                + "      flex-direction: column;\n"
                + "      gap: 16px;\n"
                + "    }\n"
                + "\n"
                + "    /* Drop Zone */\n"
                + "    .drop-zone {\n"
                + "      border: 2px dashed rgba(56, 189, 248, 0.35);\n"
                + "      border-radius: 14px;\n"
                + "      padding: 38px 20px;\n"
                + "      text-align: center;\n"
                + "      cursor: pointer;\n"
                + "      transition: all 0.2s ease;\n"
                + "      background: rgba(56, 189, 248, 0.02);\n"
                + "    }\n"
                + "    .drop-zone.dragover {\n"
                + "      border-color: #38bdf8;\n"
                + "      background: rgba(56, 189, 248, 0.12);\n"
                + "      transform: scale(1.008);\n"
                + "    }\n"
                + "    .drop-icon { font-size: 46px; margin-bottom: 10px; display: block; filter: drop-shadow(0 4px 12px rgba(56,189,248,0.3)); }\n"
                + "    .drop-title { font-size: 17px; font-weight: 600; margin-bottom: 6px; }\n"
                + "    .drop-sub { font-size: 13px; color: var(--text-dim); }\n"
                + "\n"
                + "    .options-row {\n"
                + "      display: flex;\n"
                + "      justify-content: space-between;\n"
                + "      align-items: center;\n"
                + "      flex-wrap: wrap;\n"
                + "      gap: 10px;\n"
                + "    }\n"
                + "    .toggle-label {\n"
                + "      display: flex;\n"
                + "      align-items: center;\n"
                + "      gap: 8px;\n"
                + "      font-size: 14px;\n"
                + "      font-weight: 500;\n"
                + "      cursor: pointer;\n"
                + "    }\n"
                + "    .toggle-label input { width: 17px; height: 17px; accent-color: var(--primary); }\n"
                + "\n"
                + "    /* Progress Box */\n"
                + "    .progress-box { display: none; margin-top: 6px; }\n"
                + "    .progress-bar-bg { width: 100%; height: 8px; background: rgba(255, 255, 255, 0.08); border-radius: 999px; overflow: hidden; margin-top: 6px; }\n"
                + "    .progress-bar-fill { height: 100%; width: 0%; background: linear-gradient(90deg, #06b6d4, #8b5cf6); transition: width 0.15s ease; }\n"
                + "\n"
                + "    /* Buttons */\n"
                + "    .btn {\n"
                + "      padding: 7px 14px;\n"
                + "      font-size: 13px;\n"
                + "      font-weight: 600;\n"
                + "      border-radius: 8px;\n"
                + "      border: none;\n"
                + "      cursor: pointer;\n"
                + "      display: inline-flex;\n"
                + "      align-items: center;\n"
                + "      gap: 6px;\n"
                + "      transition: all 0.15s ease;\n"
                + "      text-decoration: none;\n"
                + "      user-select: none;\n"
                + "    }\n"
                + "    .btn-sm { padding: 4px 10px; font-size: 12px; border-radius: 6px; }\n"
                + "    .btn-primary { background: #06b6d4; color: #000; }\n"
                + "    .btn-primary:hover { background: #22d3ee; }\n"
                + "    .btn-install { background: #06b6d4; color: #000; }\n"
                + "    .btn-install:hover { background: #22d3ee; box-shadow: 0 0 10px rgba(6,182,212,0.5); }\n"
                + "    .btn-down { background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3); }\n"
                + "    .btn-down:hover { background: rgba(56, 189, 248, 0.25); }\n"
                + "    .btn-edit { background: rgba(168, 85, 247, 0.15); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.3); }\n"
                + "    .btn-edit:hover { background: rgba(168, 85, 247, 0.25); }\n"
                + "    .btn-del { background: var(--danger-bg); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); }\n"
                + "    .btn-del:hover { background: rgba(239, 68, 68, 0.25); }\n"
                + "    .btn-secondary { background: rgba(255, 255, 255, 0.08); color: var(--text); border: 1px solid var(--card-border); }\n"
                + "    .btn-secondary:hover { background: rgba(255, 255, 255, 0.15); }\n"
                + "\n"
                + "    /* Storage Capacity Bar */\n"
                + "    .stat-row { display: flex; justify-content: space-between; font-size: 13px; color: var(--text-dim); }\n"
                + "    .storage-bar-bg { width: 100%; height: 6px; background: rgba(255, 255, 255, 0.08); border-radius: 999px; overflow: hidden; }\n"
                + "    .storage-bar-fill { height: 100%; width: 0%; background: linear-gradient(90deg, #06b6d4, #8b5cf6); }\n"
                + "\n"
                + "    /* Push File List */\n"
                + "    .file-list { display: flex; flex-direction: column; gap: 8px; }\n"
                + "    .file-item {\n"
                + "      display: flex;\n"
                + "      justify-content: space-between;\n"
                + "      align-items: center;\n"
                + "      padding: 12px 14px;\n"
                + "      background: rgba(255, 255, 255, 0.025);\n"
                + "      border: 1px solid var(--card-border);\n"
                + "      border-radius: 10px;\n"
                + "      gap: 12px;\n"
                + "    }\n"
                + "    .file-info { display: flex; flex-direction: column; gap: 4px; overflow: hidden; min-width: 0; }\n"
                + "    .file-name { font-size: 14px; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }\n"
                + "    .file-meta { font-size: 12px; color: var(--text-dim); }\n"
                + "    .btn-group { display: flex; gap: 6px; flex-shrink: 0; }\n"
                + "\n"
                + "    /* --- File Manager View (FS) --- */\n"
                + "    .fs-storage-bar {\n"
                + "      display: flex;\n"
                + "      gap: 8px;\n"
                + "      overflow-x: auto;\n"
                + "      padding-bottom: 2px;\n"
                + "    }\n"
                + "    .fs-storage-bar::-webkit-scrollbar { height: 4px; }\n"
                + "    .fs-storage-bar::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.15); border-radius: 4px; }\n"
                + "    .storage-chip {\n"
                + "      padding: 6px 12px;\n"
                + "      font-size: 13px;\n"
                + "      font-weight: 500;\n"
                + "      background: rgba(255, 255, 255, 0.04);\n"
                + "      border: 1px solid var(--card-border);\n"
                + "      border-radius: 8px;\n"
                + "      color: var(--text);\n"
                + "      cursor: pointer;\n"
                + "      white-space: nowrap;\n"
                + "      display: flex;\n"
                + "      align-items: center;\n"
                + "      gap: 6px;\n"
                + "      transition: all 0.15s;\n"
                + "    }\n"
                + "    .storage-chip:hover { background: rgba(255, 255, 255, 0.09); }\n"
                + "    .storage-chip-active {\n"
                + "      background: rgba(6, 182, 212, 0.15);\n"
                + "      border-color: rgba(6, 182, 212, 0.4);\n"
                + "      color: #38bdf8;\n"
                + "      font-weight: 600;\n"
                + "    }\n"
                + "\n"
                + "    .fs-toolbar {\n"
                + "      display: flex;\n"
                + "      flex-wrap: wrap;\n"
                + "      justify-content: space-between;\n"
                + "      align-items: center;\n"
                + "      gap: 10px;\n"
                + "      background: rgba(15, 23, 42, 0.5);\n"
                + "      border: 1px solid var(--card-border);\n"
                + "      border-radius: 10px;\n"
                + "      padding: 8px 12px;\n"
                + "    }\n"
                + "    .fs-breadcrumb {\n"
                + "      display: flex;\n"
                + "      align-items: center;\n"
                + "      gap: 4px;\n"
                + "      flex-wrap: wrap;\n"
                + "      font-size: 13px;\n"
                + "      font-weight: 500;\n"
                + "      overflow: hidden;\n"
                + "    }\n"
                + "    .bc-item {\n"
                + "      color: #38bdf8;\n"
                + "      cursor: pointer;\n"
                + "      padding: 2px 4px;\n"
                + "      border-radius: 4px;\n"
                + "    }\n"
                + "    .bc-item:hover { background: rgba(56, 189, 248, 0.12); }\n"
                + "    .bc-sep { color: var(--text-dim); }\n"
                + "    .fs-tool-btns {\n"
                + "      display: flex;\n"
                + "      gap: 6px;\n"
                + "      align-items: center;\n"
                + "      flex-wrap: wrap;\n"
                + "    }\n"
                + "    .search-input {\n"
                + "      background: rgba(255, 255, 255, 0.05);\n"
                + "      border: 1px solid var(--card-border);\n"
                + "      border-radius: 6px;\n"
                + "      padding: 5px 10px;\n"
                + "      color: #fff;\n"
                + "      font-size: 13px;\n"
                + "      width: 130px;\n"
                + "      transition: width 0.2s;\n"
                + "    }\n"
                + "    .search-input:focus {\n"
                + "      outline: none;\n"
                + "      border-color: #38bdf8;\n"
                + "      width: 170px;\n"
                + "    }\n"
                + "\n"
                + "    /* FS Table */\n"
                + "    .fs-table-wrap {\n"
                + "      width: 100%;\n"
                + "      overflow-x: auto;\n"
                + "      border: 1px solid var(--card-border);\n"
                + "      border-radius: 10px;\n"
                + "      background: rgba(15, 23, 42, 0.4);\n"
                + "    }\n"
                + "    .fs-table {\n"
                + "      width: 100%;\n"
                + "      border-collapse: collapse;\n"
                + "      text-align: left;\n"
                + "      font-size: 13px;\n"
                + "    }\n"
                + "    .fs-table th {\n"
                + "      background: rgba(255, 255, 255, 0.03);\n"
                + "      padding: 10px 12px;\n"
                + "      color: var(--text-dim);\n"
                + "      font-weight: 600;\n"
                + "      border-bottom: 1px solid var(--card-border);\n"
                + "      white-space: nowrap;\n"
                + "    }\n"
                + "    .fs-row {\n"
                + "      border-bottom: 1px solid rgba(255, 255, 255, 0.04);\n"
                + "      transition: background 0.15s;\n"
                + "    }\n"
                + "    .fs-row:last-child { border-bottom: none; }\n"
                + "    .fs-row:hover { background: var(--hover-bg); }\n"
                + "    .fs-td-name {\n"
                + "      padding: 10px 12px;\n"
                + "      display: flex;\n"
                + "      align-items: center;\n"
                + "      gap: 8px;\n"
                + "      min-width: 220px;\n"
                + "      max-width: 380px;\n"
                + "    }\n"
                + "    .fs-icon { font-size: 17px; flex-shrink: 0; }\n"
                + "    .fs-name-text {\n"
                + "      white-space: nowrap;\n"
                + "      overflow: hidden;\n"
                + "      text-overflow: ellipsis;\n"
                + "    }\n"
                + "    .fs-td-size { padding: 10px 12px; color: var(--text-dim); white-space: nowrap; width: 90px; }\n"
                + "    .fs-td-date { padding: 10px 12px; color: var(--text-dim); white-space: nowrap; width: 140px; }\n"
                + "    .fs-td-actions { padding: 10px 12px; text-align: right; white-space: nowrap; width: 190px; }\n"
                + "\n"
                + "    /* Modal */\n"
                + "    .modal-overlay {\n"
                + "      position: fixed;\n"
                + "      top: 0; left: 0; right: 0; bottom: 0;\n"
                + "      background: rgba(0, 0, 0, 0.65);\n"
                + "      backdrop-filter: blur(8px);\n"
                + "      -webkit-backdrop-filter: blur(8px);\n"
                + "      display: none;\n"
                + "      align-items: center;\n"
                + "      justify-content: center;\n"
                + "      z-index: 1000;\n"
                + "      padding: 16px;\n"
                + "    }\n"
                + "    .modal-card {\n"
                + "      background: #131b2e;\n"
                + "      border: 1px solid rgba(255, 255, 255, 0.12);\n"
                + "      border-radius: 14px;\n"
                + "      width: 100%;\n"
                + "      max-width: 400px;\n"
                + "      padding: 20px;\n"
                + "      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6);\n"
                + "      display: flex;\n"
                + "      flex-direction: column;\n"
                + "      gap: 16px;\n"
                + "    }\n"
                + "    .modal-title { font-size: 16px; font-weight: 600; color: #f8fafc; }\n"
                + "    .modal-input {\n"
                + "      width: 100%;\n"
                + "      background: rgba(255, 255, 255, 0.06);\n"
                + "      border: 1px solid rgba(255, 255, 255, 0.15);\n"
                + "      border-radius: 8px;\n"
                + "      padding: 9px 12px;\n"
                + "      color: #fff;\n"
                + "      font-size: 14px;\n"
                + "    }\n"
                + "    .modal-input:focus { outline: none; border-color: #38bdf8; }\n"
                + "    .modal-actions { display: flex; justify-content: flex-end; gap: 8px; }\n"
                + "\n"
                + "    /* Toast */\n"
                + "    .toast-container {\n"
                + "      position: fixed;\n"
                + "      top: 20px;\n"
                + "  ";
    private static final String HTML_PART_1 = "    right: 20px;\n"
                + "      display: flex;\n"
                + "      flex-direction: column;\n"
                + "      gap: 8px;\n"
                + "      z-index: 1100;\n"
                + "      pointer-events: none;\n"
                + "    }\n"
                + "    .toast {\n"
                + "      padding: 10px 16px;\n"
                + "      border-radius: 8px;\n"
                + "      font-size: 13px;\n"
                + "      font-weight: 500;\n"
                + "      background: #1e293b;\n"
                + "      color: #fff;\n"
                + "      box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);\n"
                + "      border: 1px solid rgba(255, 255, 255, 0.1);\n"
                + "      transition: all 0.3s ease;\n"
                + "      pointer-events: auto;\n"
                + "      max-width: 320px;\n"
                + "    }\n"
                + "    .toast-success { border-color: #10b981; color: #34d399; }\n"
                + "    .toast-error { border-color: #ef4444; color: #f87171; }\n"
                + "    .toast-info { border-color: #38bdf8; color: #38bdf8; }\n"
                + "\n"
                + "    @media (max-width: 640px) {\n"
                + "      .container { gap: 12px; }\n"
                + "      .card { padding: 14px; }\n"
                + "      .fs-td-date { display: none; }\n"
                + "      .fs-td-name { max-width: 160px; }\n"
                + "      .search-input { width: 90px; }\n"
                + "      .search-input:focus { width: 120px; }\n"
                + "    }\n"
                + "  </style>\n"
                + "</head>\n"
                + "<body>\n"
                + "  <div class=\"container\">\n"
                + "    <header>\n"
                + "      <div class=\"brand\">🚀 NextGen 隔空传装 & 盒子管家</div>\n"
                + "      <div class=\"badge-online\">\n"
                + "        <span class=\"badge-dot\"></span>\n"
                + "        <span id=\"device-badge\">斐讯 N1 在线</span>\n"
                + "      </div>\n"
                + "    </header>\n"
                + "\n"
                + "    <!-- Tab Bar -->\n"
                + "    <div class=\"tab-bar\">\n"
                + "      <button class=\"tab-btn active\" id=\"tab-push\">⚡ 极速传装</button>\n"
                + "      <button class=\"tab-btn\" id=\"tab-fs\">📁 盒子文件管理</button>\n"
                + "    </div>\n"
                + "\n"
                + "    <!-- VIEW 1: 极速传装 (Push Tab) -->\n"
                + "    <div id=\"view-push\" style=\"display:flex; flex-direction:column; gap:16px;\">\n"
                + "      <div class=\"card\">\n"
                + "        <div class=\"drop-zone\" id=\"dropZone\">\n"
                + "          <span class=\"drop-icon\">📦</span>\n"
                + "          <div class=\"drop-title\">点击或拖拽 APK / 影视文件至此处</div>\n"
                + "          <div class=\"drop-sub\">支持批量传输 · 极速局域网直连 · 0 数据损耗</div>\n"
                + "          <input type=\"file\" id=\"fileInput\" multiple style=\"display:none;\">\n"
                + "        </div>\n"
                + "        <div class=\"options-row\">\n"
                + "          <label class=\"toggle-label\">\n"
                + "            <input type=\"checkbox\" id=\"autoInstallCheck\" checked>\n"
                + "            <span>上传完成后自动静默安装 APK</span>\n"
                + "          </label>\n"
                + "          <span id=\"upload-status\" style=\"font-size:13px; color:var(--text-dim);\">就绪</span>\n"
                + "        </div>\n"
                + "        <div class=\"progress-box\" id=\"progressBox\">\n"
                + "          <div style=\"display:flex; justify-content:space-between; font-size:13px;\">\n"
                + "            <span id=\"progress-name\">正在传输...</span>\n"
                + "            <span id=\"progress-pct\">0%</span>\n"
                + "          </div>\n"
                + "          <div class=\"progress-bar-bg\"><div class=\"progress-bar-fill\" id=\"progressFill\"></div></div>\n"
                + "        </div>\n"
                + "      </div>\n"
                + "\n"
                + "      <div class=\"card\">\n"
                + "        <div class=\"stat-row\">\n"
                + "          <span>📦 存储空间</span>\n"
                + "          <span id=\"storage-text\">可用计算中...</span>\n"
                + "        </div>\n"
                + "        <div class=\"storage-bar-bg\"><div class=\"storage-bar-fill\" id=\"storageFill\"></div></div>\n"
                + "        <div style=\"margin-top:6px; font-weight:600; font-size:15px; display:flex; justify-content:space-between; align-items:center;\">\n"
                + "          <span>📂 已接收文件 (Download 目录)</span>\n"
                + "          <button class=\"btn btn-sm btn-secondary\" onclick=\"loadStatus()\">🔄 刷新列表</button>\n"
                + "        </div>\n"
                + "        <div class=\"file-list\" id=\"fileList\">加载中...</div>\n"
                + "      </div>\n"
                + "    </div>\n"
                + "\n"
                + "    <!-- VIEW 2: 文件管理 (FS Tab) -->\n"
                + "    <div id=\"view-fs\" style=\"display:none; flex-direction:column; gap:16px;\">\n"
                + "      <div class=\"card\" id=\"fs-drop-zone\">\n"
                + "        <!-- Storage Mount Quick Chips -->\n"
                + "        <div class=\"fs-storage-bar\" id=\"fs-storage-chips\">\n"
                + "          <!-- Dynamically filled: 内部存储, 下载目录, 影视目录, U盘等 -->\n"
                + "        </div>\n"
                + "\n"
                + "        <!-- Toolbar & Breadcrumb -->\n"
                + "        <div class=\"fs-toolbar\">\n"
                + "          <div class=\"fs-breadcrumb\" id=\"fs-breadcrumb\">\n"
                + "            <span class=\"bc-item\">/sdcard</span>\n"
                + "          </div>\n"
                + "          <div class=\"fs-tool-btns\">\n"
                + "            <input type=\"text\" class=\"search-input\" id=\"fs-search-input\" placeholder=\"🔍 搜索过滤...\">\n"
                + "            <button class=\"btn btn-sm btn-secondary\" onclick=\"window.NextGen.goParent()\">⬆️ 上级</button>\n"
                + "            <button class=\"btn btn-sm btn-secondary\" onclick=\"window.NextGen.refresh()\">🔄 刷新</button>\n"
                + "            <button class=\"btn btn-sm btn-secondary\" onclick=\"window.NextGen.createFolderPrompt()\">➕ 新建</button>\n"
                + "            <button class=\"btn btn-sm btn-primary\" onclick=\"window.NextGen.triggerFsUpload()\">📤 上传</button>\n"
                + "            <input type=\"file\" id=\"fs-upload-input\" multiple style=\"display:none;\">\n"
                + "          </div>\n"
                + "        </div>\n"
                + "\n"
                + "        <!-- Storage Bar for Current Path -->\n"
                + "        <div class=\"stat-row\">\n"
                + "          <span>💾 当前卷容量</span>\n"
                + "          <span id=\"fs-storage-text\">计算中...</span>\n"
                + "        </div>\n"
                + "        <div class=\"storage-bar-bg\"><div class=\"storage-bar-fill\" id=\"fs-storage-fill\"></div></div>\n"
                + "\n"
                + "        <!-- File Table -->\n"
                + "        <div class=\"fs-table-wrap\">\n"
                + "          <table class=\"fs-table\">\n"
                + "            <thead>\n"
                + "              <tr>\n"
                + "                <th>文件名</th>\n"
                + "                <th>大小</th>\n"
                + "                <th>修改时间</th>\n"
                + "                <th style=\"text-align:right;\">操作</th>\n"
                + "              </tr>\n"
                + "            </thead>\n"
                + "            <tbody id=\"fs-table-body\">\n"
                + "              <tr><td colspan=\"4\" style=\"text-align:center; padding:24px; color:var(--text-dim);\">加载中...</td></tr>\n"
                + "            </tbody>\n"
                + "          </table>\n"
                + "        </div>\n"
                + "      </div>\n"
                + "    </div>\n"
                + "  </div>\n"
                + "\n"
                + "  <!-- Modal Dialog -->\n"
                + "  <div class=\"modal-overlay\" id=\"modalOverlay\">\n"
                + "    <div class=\"modal-card\">\n"
                + "      <div class=\"modal-title\" id=\"modalTitle\">输入</div>\n"
                + "      <input type=\"text\" class=\"modal-input\" id=\"modalInput\">\n"
                + "      <div class=\"modal-actions\">\n"
                + "        <button class=\"btn btn-secondary\" id=\"modalBtnCancel\">取消</button>\n"
                + "        <button class=\"btn btn-primary\" id=\"modalBtnConfirm\">确定</button>\n"
                + "      </div>\n"
                + "    </div>\n"
                + "  </div>\n"
                + "\n"
                + "  <!-- Toast Container -->\n"
                + "  <div class=\"toast-container\" id=\"toastContainer\"></div>\n"
                + "\n"
                + "  <!-- Embedded Logic -->\n"
                + "  <script>\n"
                + "// NextGen 隔空传装 & 文件管理器 Web 控制台\n"
                + "(function() {\n"
                + "  'use strict';\n"
                + "\n"
                + "  // DOM Elements - Tabs\n"
                + "  const tabPush = document.getElementById('tab-push');\n"
                + "  const tabFs = document.getElementById('tab-fs');\n"
                + "  const viewPush = document.getElementById('view-push');\n"
                + "  const viewFs = document.getElementById('view-fs');\n"
                + "\n"
                + "  // Push Tab Elements\n"
                + "  const dropZone = document.getElementById('dropZone');\n"
                + "  const fileInput = document.getElementById('fileInput');\n"
                + "  const autoInstallCheck = document.getElementById('autoInstallCheck');\n"
                + "  const progressBox = document.getElementById('progressBox');\n"
                + "  const progressFill = document.getElementById('progressFill');\n"
                + "  const progressPct = document.getElementById('progress-pct');\n"
                + "  const progressName = document.getElementById('progress-name');\n"
                + "  const fileList = document.getElementById('fileList');\n"
                + "  const storageText = document.getElementById('storage-text');\n"
                + "  const storageFill = document.getElementById('storageFill');\n"
                + "  const uploadStatus = document.getElementById('upload-status');\n"
                + "\n"
                + "  // FS Tab Elements\n"
                + "  const fsBreadcrumb = document.getElementById('fs-breadcrumb');\n"
                + "  const fsStorageChips = document.getElementById('fs-storage-chips');\n"
                + "  const fsStorageText = document.getElementById('fs-storage-text');\n"
                + "  const fsStorageFill = document.getElementById('fs-storage-fill');\n"
                + "  const fsTableBody = document.getElementById('fs-table-body');\n"
                + "  const fsSearchInput = document.getElementById('fs-search-input');\n"
                + "  const fsUploadInput = document.getElementById('fs-upload-input');\n"
                + "  const fsDropZone = document.getElementById('fs-drop-zone');\n"
                + "\n"
                + "  // Modal Elements\n"
                + "  const modalOverlay = document.getElementById('modalOverlay');\n"
                + "  const modalTitle = document.getElementById('modalTitle');\n"
                + "  const modalInput = document.getElementById('modalInput');\n"
                + "  const modalBtnConfirm = document.getElementById('modalBtnConfirm');\n"
                + "  const modalBtnCancel = document.getElementById('modalBtnCancel');\n"
                + "\n"
                + "  // Toast Container\n"
                + "  const toastContainer = document.getElementById('toastContainer');\n"
                + "\n"
                + "  // State\n"
                + "  let currentPath = '/sdcard';\n"
                + "  let parentPath = '';\n"
                + "  let fsItems = [];\n"
                + "  let modalCallback = null;\n"
                + "\n"
                + "  // Tab switching\n"
                + "  function switchTab(tab) {\n"
                + "    if (tab === 'push') {\n"
                + "      tabPush.classList.add('active');\n"
                + "      tabFs.classList.remove('active');\n"
                + "      viewPush.style.display = 'flex';\n"
                + "      viewFs.style.display = 'none';\n"
                + "      loadStatus();\n"
                + "    } else {\n"
                + "      tabFs.classList.add('active');\n"
                + "      tabPush.classList.remove('active');\n"
                + "      viewFs.style.display = 'flex';\n"
                + "      viewPush.style.display = 'none';\n"
                + "      loadFs(currentPath);\n"
                + "    }\n"
                + "  }\n"
                + "\n"
                + "  if (tabPush && tabFs) {\n"
                + "    tabPush.onclick = () => switchTab('push');\n"
                + "    tabFs.onclick = () => switchTab('fs');\n"
                + "  }\n"
                + "\n"
                + "  // Toast Notification\n"
                + "  function showToast(msg, type = 'info') {\n"
                + "    if (!toastContainer) return;\n"
                + "    const toast = document.createElement('div');\n"
                + "    toast.className = `toast toast-${type}`;\n"
                + "    toast.innerText = msg;\n"
                + "    toastContainer.appendChild(toast);\n"
                + "    setTimeout(() => {\n"
                + "      toast.style.opacity = '0';\n"
                + "      toast.style.transform = 'translateY(-10px)';\n"
                + "      setTimeout(() => toast.remove(), 300);\n"
                + "    }, 3200);\n"
                + "  }\n"
                + "\n"
                + "  // Modal helper\n"
                + "  function openModal(title, defaultValue, onConfirm) {\n"
                + "    if (!modalOverlay || !modalInput || !modalTitle) return;\n"
                + "    modalTitle.innerText = title;\n"
                + "    modalInput.value = defaultValue || '';\n"
                + "    modalOverlay.style.display = 'flex';\n"
                + "    modalInput.focus();\n"
                + "    modalCallback = onConfirm;\n"
                + "  }\n"
                + "\n"
                + "  function closeModal() {\n"
                + "    if (!modalOverlay) return;\n"
                + "    modalOverlay.style.display = 'none';\n"
                + "    modalCallback = null;\n"
                + "  }\n"
                + "\n"
                + "  if (modalBtnCancel) modalBtnCancel.onclick = closeModal;\n"
                + "  if (modalBtnConfirm) {\n"
                + "    modalBtnConfirm.onclick = () => {\n"
                + "      if (modalCallback) {\n"
                + "        const val = modalInput.value.trim();\n"
                + "        modalCallback(val);\n"
                + "      }\n"
                + "      closeModal();\n"
                + "    };\n"
                + "  }\n"
                + "  if (modalInput) {\n"
                + "    modalInput.onkeydown = (e) => {\n"
                + "      if (e.key === 'Enter') {\n"
                + "        if (modalCallback) {\n"
                + "          modalCallback(modalInput.value.trim());\n"
                + "        }\n"
                + "        closeModal();\n"
                + "      } else if (e.key === 'Escape') {\n"
                + "        closeModal();\n"
                + "      }\n"
                + "    };\n"
                + "  }\n"
                + "\n"
                + "  // --- Push Tab Logic ---\n"
                + "  if (dropZone && fileInput) {\n"
                + "    dropZone.onclick = () => fileInput.click();\n"
                + "    dropZone.ondragover = e => { e.preventDefault(); dropZone.classList.add('dragover'); };\n"
                + "    dropZone.ondragleave = () => dropZone.classList.remove('dragover');\n"
                + "    dropZone.ondrop = e => {\n"
                + "      e.preventDefault();\n"
                + "      dropZone.classList.remove('dragover');\n"
                + "      if (e.dataTransfer && e.dataTransfer.files.length) uploadFiles(e.dataTransfer.files, null, true);\n"
                + "    };\n"
                + "    fileInput.onchange = () => {\n"
                + "      if (fileInput.files.length) uploadFiles(fileInput.files, null, true);\n"
                + "    };\n"
                + "  }\n"
                + "\n"
                + "  async function loadStatus() {\n"
                + "    try {\n"
                + "      const res = await fetch('/api/status');\n"
                + "      const data = await res.json();\n"
                + "      if (storageText) storageText.innerText = `${data.storageFree} 可用 / ${data.storageTotal} 总计`;\n"
                + "      if (storageFill) storageFill.style.width = `${data.storagePercent}%`;\n"
                + "      renderPushFiles(data.files);\n"
                + "    } catch (e) {}\n"
                + "  }\n"
                + "\n"
                + "  function renderPushFiles(files) {\n"
                + "    if (!fileList) return;\n"
                + "    if (!files || files.length === 0) {\n"
                + "      fileList.innerHTML = '<div style=\"color:var(--text-dim); text-align:center; padding:24px;\">暂无已接收文件</div>';\n"
                + "      return;\n"
                + "    }\n"
                + "    fileList.innerHTML = files.map(f => `\n"
                + "      <div class=\"file-item\">\n"
                + "        <div class=\"file-info\">\n"
                + "          <div class=\"file-name\">${escapeHtml(f.name)}</div>\n"
                + "          <div class=\"file-meta\">${f.size} · ${f.date}</div>\n"
                + "        </div>\n"
                + "        <div class=\"btn-group\">\n"
                + "          ${f.isApk ? `<button class=\"btn btn-install\" onclick=\"window.NextGen.installApk('${escapeJs(f.name)}')\">一键安装</button>` : ''}\n"
                + "          <a class=\"btn btn-down\" href=\"/download/${encodeURIComponent(f.name)}\" download=\"${escapeHtml(f.name)}\">下载</a>\n"
                + "          <button class=\"btn btn-del\" onclick=\"window.NextGen.deletePushFile('${escapeJs(f.name)}')\">删除</button>\n"
                + "        </div>\n"
                + "      </div>\n"
                + "    `).join('');\n"
                + "  }\n"
                + "\n"
                + "  // --- File Manager (FS) Logic ---\n"
                + "  async function loadFs(path) {\n"
                + "    try {\n"
                + "      const target = path || currentPath || '/sdcard';\n"
                + "      const res = await fetch(`/api/fs/list?path=${encodeURIComponent(target)}`);\n"
                + "      const data = await res.json();\n"
                + "\n"
                + "      currentPath ";
    private static final String HTML_PART_2 = "= data.currentPath;\n"
                + "      parentPath = data.parentPath;\n"
                + "      fsItems = data.items || [];\n"
                + "\n"
                + "      // Render Storages\n"
                + "      renderFsStorages(data.storages || []);\n"
                + "\n"
                + "      // Render Breadcrumb\n"
                + "      renderFsBreadcrumb(data.currentPath);\n"
                + "\n"
                + "      // Render Capacity\n"
                + "      if (fsStorageText) fsStorageText.innerText = `${data.storageFree} 可用 / ${data.storageTotal} 总计 (${data.storagePercent}% 已用)`;\n"
                + "      if (fsStorageFill) fsStorageFill.style.width = `${data.storagePercent}%`;\n"
                + "\n"
                + "      // Render Table\n"
                + "      filterAndRenderFsTable();\n"
                + "    } catch (e) {\n"
                + "      showToast('加载目录失败: ' + e.message, 'error');\n"
                + "    }\n"
                + "  }\n"
                + "\n"
                + "  function renderFsStorages(storages) {\n"
                + "    if (!fsStorageChips) return;\n"
                + "    fsStorageChips.innerHTML = storages.map(s => {\n"
                + "      const activeClass = currentPath.startsWith(s.path) ? 'storage-chip-active' : '';\n"
                + "      let icon = '📱';\n"
                + "      if (s.name.includes('U盘') || s.name.includes('外接') || s.path.includes('/storage/')) icon = '💾';\n"
                + "      else if (s.name.includes('下载')) icon = '📥';\n"
                + "      else if (s.name.includes('影视')) icon = '🎬';\n"
                + "      return `<button class=\"storage-chip ${activeClass}\" onclick=\"window.NextGen.navigateTo('${escapeJs(s.path)}')\">${icon} ${escapeHtml(s.name)}</button>`;\n"
                + "    }).join('');\n"
                + "  }\n"
                + "\n"
                + "  function renderFsBreadcrumb(path) {\n"
                + "    if (!fsBreadcrumb) return;\n"
                + "    const parts = path.split('/').filter(Boolean);\n"
                + "    let accumulated = '';\n"
                + "    let html = `<span class=\"bc-item\" onclick=\"window.NextGen.navigateTo('/')\">根目录</span>`;\n"
                + "    for (let i = 0; i < parts.length; i++) {\n"
                + "      accumulated += '/' + parts[i];\n"
                + "      const p = accumulated;\n"
                + "      html += `<span class=\"bc-sep\">/</span><span class=\"bc-item\" onclick=\"window.NextGen.navigateTo('${escapeJs(p)}')\">${escapeHtml(parts[i])}</span>`;\n"
                + "    }\n"
                + "    fsBreadcrumb.innerHTML = html;\n"
                + "  }\n"
                + "\n"
                + "  function filterAndRenderFsTable() {\n"
                + "    if (!fsTableBody) return;\n"
                + "    const query = fsSearchInput ? fsSearchInput.value.trim().toLowerCase() : '';\n"
                + "    const filtered = query ? fsItems.filter(item => item.name.toLowerCase().includes(query)) : fsItems;\n"
                + "\n"
                + "    if (filtered.length === 0) {\n"
                + "      fsTableBody.innerHTML = `<tr><td colspan=\"4\" style=\"text-align:center; padding:32px; color:var(--text-dim);\">当前目录为空或无匹配项</td></tr>`;\n"
                + "      return;\n"
                + "    }\n"
                + "\n"
                + "    fsTableBody.innerHTML = filtered.map(item => {\n"
                + "      const icon = getFileIcon(item.type, item.isDir);\n"
                + "      const nameClick = item.isDir \n"
                + "        ? `onclick=\"window.NextGen.navigateTo('${escapeJs(item.path)}')\"` \n"
                + "        : '';\n"
                + "      const nameStyle = item.isDir ? 'cursor:pointer; font-weight:600; color:#38bdf8;' : '';\n"
                + "\n"
                + "      return `\n"
                + "        <tr class=\"fs-row\">\n"
                + "          <td class=\"fs-td-name\" ${nameClick} style=\"${nameStyle}\">\n"
                + "            <span class=\"fs-icon\">${icon}</span>\n"
                + "            <span class=\"fs-name-text\" title=\"${escapeHtml(item.name)}\">${escapeHtml(item.name)}</span>\n"
                + "          </td>\n"
                + "          <td class=\"fs-td-size\">${item.size}</td>\n"
                + "          <td class=\"fs-td-date\">${item.date}</td>\n"
                + "          <td class=\"fs-td-actions\">\n"
                + "            ${item.isApk ? `<button class=\"btn btn-sm btn-install\" onclick=\"window.NextGen.installFsApk('${escapeJs(item.path)}')\">安装</button>` : ''}\n"
                + "            ${!item.isDir ? `<a class=\"btn btn-sm btn-down\" href=\"/api/fs/download?path=${encodeURIComponent(item.path)}\" download=\"${escapeHtml(item.name)}\">下载</a>` : ''}\n"
                + "            <button class=\"btn btn-sm btn-edit\" onclick=\"window.NextGen.renameFsItem('${escapeJs(item.path)}', '${escapeJs(item.name)}')\">重命名</button>\n"
                + "            <button class=\"btn btn-sm btn-del\" onclick=\"window.NextGen.deleteFsItem('${escapeJs(item.path)}', '${escapeJs(item.name)}', ${item.isDir})\">删除</button>\n"
                + "          </td>\n"
                + "        </tr>\n"
                + "      `;\n"
                + "    }).join('');\n"
                + "  }\n"
                + "\n"
                + "  function getFileIcon(type, isDir) {\n"
                + "    if (isDir) return '📁';\n"
                + "    switch (type) {\n"
                + "      case 'apk': return '📦';\n"
                + "      case 'video': return '🎬';\n"
                + "      case 'audio': return '🎵';\n"
                + "      case 'image': return '🖼️';\n"
                + "      case 'archive': return '🗜️';\n"
                + "      case 'text': return '📄';\n"
                + "      default: return '📄';\n"
                + "    }\n"
                + "  }\n"
                + "\n"
                + "  if (fsSearchInput) {\n"
                + "    fsSearchInput.oninput = () => filterAndRenderFsTable();\n"
                + "  }\n"
                + "\n"
                + "  // FS Drag and drop upload\n"
                + "  if (fsDropZone && fsUploadInput) {\n"
                + "    fsDropZone.ondragover = e => { e.preventDefault(); fsDropZone.classList.add('dragover'); };\n"
                + "    fsDropZone.ondragleave = () => fsDropZone.classList.remove('dragover');\n"
                + "    fsDropZone.ondrop = e => {\n"
                + "      e.preventDefault();\n"
                + "      fsDropZone.classList.remove('dragover');\n"
                + "      if (e.dataTransfer && e.dataTransfer.files.length) uploadFiles(e.dataTransfer.files, currentPath, false);\n"
                + "    };\n"
                + "    fsUploadInput.onchange = () => {\n"
                + "      if (fsUploadInput.files.length) uploadFiles(fsUploadInput.files, currentPath, false);\n"
                + "    };\n"
                + "  }\n"
                + "\n"
                + "  // Upload Engine\n"
                + "  async function uploadFiles(files, targetDir, isPushTab) {\n"
                + "    for (let i = 0; i < files.length; i++) {\n"
                + "      await uploadSingle(files[i], targetDir, isPushTab);\n"
                + "    }\n"
                + "    if (isPushTab) {\n"
                + "      loadStatus();\n"
                + "    } else {\n"
                + "      loadFs(currentPath);\n"
                + "    }\n"
                + "  }\n"
                + "\n"
                + "  function uploadSingle(file, targetDir, isPushTab) {\n"
                + "    return new Promise((resolve) => {\n"
                + "      if (progressBox) progressBox.style.display = 'block';\n"
                + "      if (progressName) progressName.innerText = `正在传输: ${file.name}`;\n"
                + "      if (uploadStatus) uploadStatus.innerText = '传输中...';\n"
                + "\n"
                + "      const xhr = new XMLHttpRequest();\n"
                + "      const fd = new FormData();\n"
                + "      fd.append('file', file);\n"
                + "\n"
                + "      xhr.upload.onprogress = e => {\n"
                + "        if (e.lengthComputable) {\n"
                + "          const pct = Math.round((e.loaded / e.total) * 100);\n"
                + "          if (progressFill) progressFill.style.width = pct + '%';\n"
                + "          if (progressPct) progressPct.innerText = pct + '%';\n"
                + "        }\n"
                + "      };\n"
                + "\n"
                + "      xhr.onload = () => {\n"
                + "        if (progressBox) progressBox.style.display = 'none';\n"
                + "        if (uploadStatus) {\n"
                + "          uploadStatus.innerText = '传输完成！';\n"
                + "          setTimeout(() => uploadStatus.innerText = '就绪', 3000);\n"
                + "        }\n"
                + "        showToast(`文件 ${file.name} 传输成功！`, 'success');\n"
                + "        resolve();\n"
                + "      };\n"
                + "\n"
                + "      xhr.onerror = () => {\n"
                + "        if (uploadStatus) uploadStatus.innerText = '传输失败';\n"
                + "        showToast(`文件 ${file.name} 传输失败`, 'error');\n"
                + "        resolve();\n"
                + "      };\n"
                + "\n"
                + "      const url = targetDir ? `/api/fs/upload?path=${encodeURIComponent(targetDir)}` : '/api/upload';\n"
                + "      xhr.open('POST', url);\n"
                + "      if (isPushTab && autoInstallCheck && autoInstallCheck.checked) {\n"
                + "        xhr.setRequestHeader('X-Auto-Install', '1');\n"
                + "      }\n"
                + "      xhr.send(fd);\n"
                + "    });\n"
                + "  }\n"
                + "\n"
                + "  // Global actions for onclick\n"
                + "  window.NextGen = {\n"
                + "    navigateTo(path) {\n"
                + "      loadFs(path);\n"
                + "    },\n"
                + "    goParent() {\n"
                + "      if (parentPath) loadFs(parentPath);\n"
                + "      else showToast('已经是顶层目录', 'info');\n"
                + "    },\n"
                + "    refresh() {\n"
                + "      loadFs(currentPath);\n"
                + "      showToast('目录已刷新', 'info');\n"
                + "    },\n"
                + "    createFolderPrompt() {\n"
                + "      openModal('新建文件夹', '新建文件夹', async (name) => {\n"
                + "        if (!name) return;\n"
                + "        try {\n"
                + "          const res = await fetch('/api/fs/mkdir', {\n"
                + "            method: 'POST',\n"
                + "            headers: { 'Content-Type': 'application/json' },\n"
                + "            body: JSON.stringify({ path: currentPath, name })\n"
                + "          });\n"
                + "          const data = await res.json();\n"
                + "          if (data.status === 'ok') {\n"
                + "            showToast(`文件夹 \"${name}\" 创建成功！`, 'success');\n"
                + "            loadFs(currentPath);\n"
                + "          } else {\n"
                + "            showToast('创建失败: ' + (data.error || '未知错误'), 'error');\n"
                + "          }\n"
                + "        } catch (e) {\n"
                + "          showToast('创建异常: ' + e.message, 'error');\n"
                + "        }\n"
                + "      });\n"
                + "    },\n"
                + "    triggerFsUpload() {\n"
                + "      if (fsUploadInput) fsUploadInput.click();\n"
                + "    },\n"
                + "    renameFsItem(path, oldName) {\n"
                + "      openModal(`重命名 \"${oldName}\"`, oldName, async (newName) => {\n"
                + "        if (!newName || newName === oldName) return;\n"
                + "        try {\n"
                + "          const res = await fetch('/api/fs/rename', {\n"
                + "            method: 'POST',\n"
                + "            headers: { 'Content-Type': 'application/json' },\n"
                + "            body: JSON.stringify({ path, newName })\n"
                + "          });\n"
                + "          const data = await res.json();\n"
                + "          if (data.status === 'ok') {\n"
                + "            showToast(`已重命名为 \"${newName}\"`, 'success');\n"
                + "            loadFs(currentPath);\n"
                + "          } else {\n"
                + "            showToast('重命名失败', 'error');\n"
                + "          }\n"
                + "        } catch (e) {\n"
                + "          showToast('重命名异常: ' + e.message, 'error');\n"
                + "        }\n"
                + "      });\n"
                + "    },\n"
                + "    async deleteFsItem(path, name, isDir) {\n"
                + "      const typeText = isDir ? '文件夹及其所有内容' : '文件';\n"
                + "      if (!confirm(`确定要永久删除 ${typeText} \"${name}\" 吗？此操作无法撤销！`)) return;\n"
                + "      try {\n"
                + "        const res = await fetch('/api/fs/delete', {\n"
                + "          method: 'POST',\n"
                + "          headers: { 'Content-Type': 'application/json' },\n"
                + "          body: JSON.stringify({ path })\n"
                + "        });\n"
                + "        const data = await res.json();\n"
                + "        if (data.status === 'ok') {\n"
                + "          showToast(`已删除 \"${name}\"`, 'success');\n"
                + "          loadFs(currentPath);\n"
                + "        } else {\n"
                + "          showToast('删除失败', 'error');\n"
                + "        }\n"
                + "      } catch (e) {\n"
                + "        showToast('删除异常: ' + e.message, 'error');\n"
                + "      }\n"
                + "    },\n"
                + "    async installFsApk(path) {\n"
                + "      showToast('正在静默安装 APK，请稍候...', 'info');\n"
                + "      try {\n"
                + "        const res = await fetch('/api/fs/install', {\n"
                + "          method: 'POST',\n"
                + "          headers: { 'Content-Type': 'application/json' },\n"
                + "          body: JSON.stringify({ path })\n"
                + "        });\n"
                + "        const data = await res.json();\n"
                + "        if (data.status === 'ok') {\n"
                + "          showToast('APK 静默安装成功！已可在桌面打开', 'success');\n"
                + "        } else {\n"
                + "          showToast('已下发系统安装请求，请在电视画面确认', 'info');\n"
                + "        }\n"
                + "      } catch (e) {\n"
                + "        showToast('安装触发异常: ' + e.message, 'error');\n"
                + "      }\n"
                + "    },\n"
                + "    async installApk(name) {\n"
                + "      if (uploadStatus) uploadStatus.innerText = `正在安装 ${name}...`;\n"
                + "      showToast(`正在安装 ${name}...`, 'info');\n"
                + "      try {\n"
                + "        const res = await fetch('/api/install', {\n"
                + "          method: 'POST',\n"
                + "          headers: { 'Content-Type': 'application/json' },\n"
                + "          body: JSON.stringify({ fileName: name })\n"
                + "        });\n"
                + "        const data = await res.json();\n"
                + "        const msg = data.status === 'ok' ? '安装成功！' : '已弹出安装向导';\n"
                + "        if (uploadStatus) uploadStatus.innerText = msg;\n"
                + "        showToast(msg, 'success');\n"
                + "      } catch (e) {\n"
                + "        showToast('安装已触发', 'info');\n"
                + "      }\n"
                + "      setTimeout(() => { if (uploadStatus) uploadStatus.innerText = '就绪'; }, 3000);\n"
                + "    },\n"
                + "    async deletePushFile(name) {\n"
                + "      if (!confirm(`确定删除 ${name} 吗？`)) return;\n"
                + "      await fetch('/api/delete', {\n"
                + "        method: 'POST',\n"
                + "        headers: { 'Content-Type': 'application/json' },\n"
                + "        body: JSON.stringify({ fileName: name })\n"
                + "      });\n"
                + "      showToast(`已删除 ${name}`, 'success');\n"
                + "      loadStatus();\n"
                + "    }\n"
                + "  };\n"
                + "\n"
                + "  function escapeHtml(str) {\n"
                + "    if (!str) return '';\n"
                + "    return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/\"/g, '&quot;');\n"
                + "  }\n"
                + "\n"
                + "  function escapeJs(str) {\n"
                + "    if (!str) return '';\n"
                + "    return String(str).replace(/\\\\/g, '\\\\\\\\').replace(/'/g, \"\\\\'\").replace(/\"/g, '\\\\\"');\n"
                + "  }\n"
                + "\n"
                + "  // Initial loads\n"
                + "  loadStatus();\n"
                + "  setInterval(() => {\n"
                + "    if (tabPush && tabPush.classList.contains('active')) {\n"
                + "      loadStatus();\n"
                + "    }\n"
                + "  }, 6000);\n"
                + "\n"
                + "})();\n"
                + "\n"
                + "</script>\n"
                + "</body>\n"
                + "</html>\n"
                + "";

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
        } else if ("/api/fs/download".equals(path)) {
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
        return HTML_PART_0 + HTML_PART_1 + HTML_PART_2;
    }
}
