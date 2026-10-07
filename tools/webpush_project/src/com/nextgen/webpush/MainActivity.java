package com.nextgen.webpush;

import android.app.Activity;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.graphics.Bitmap;
import android.net.ConnectivityManager;
import android.os.Bundle;
import android.os.Environment;
import android.os.Handler;
import android.os.Looper;
import android.os.StatFs;
import android.view.KeyEvent;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import java.util.Locale;

public class MainActivity extends Activity implements HttpWebServer.OnEventListener {

    private ImageView qrCodeView;
    private TextView tvUrl;
    private TextView tvStorage;
    private TextView tvServiceStatus;
    private Button btnRefresh;

    private final Handler mHandler = new Handler(Looper.getMainLooper());
    private BroadcastReceiver mNetworkReceiver;
    private int mRetryCount = 0;

    private final Runnable mRetryRunnable = new Runnable() {
        @Override
        public void run() {
            refreshDashboard();
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        qrCodeView = (ImageView) findViewById(R.id.qr_code_view);
        tvUrl = (TextView) findViewById(R.id.tv_url);
        tvStorage = (TextView) findViewById(R.id.tv_storage);
        tvServiceStatus = (TextView) findViewById(R.id.tv_service_status);
        btnRefresh = (Button) findViewById(R.id.btn_refresh);

        // TV Remote Navigation Setup
        setupTvButton(btnRefresh, v -> {
            mRetryCount = 0;
            refreshDashboard();
            Toast.makeText(this, "IP 网络信息已刷新", Toast.LENGTH_SHORT).show();
        });

        // Default focus on Refresh Button
        btnRefresh.post(() -> btnRefresh.requestFocus());

        // Register dynamic network state listener
        registerNetworkReceiver();

        // Start background WebPushService
        Intent serviceIntent = new Intent(this, WebPushService.class);
        startService(serviceIntent);

        HttpWebServer server = WebPushService.getServer();
        if (server != null) {
            server.setEventListener(this);
        }

        refreshDashboard();
    }

    private void registerNetworkReceiver() {
        if (mNetworkReceiver == null) {
            mNetworkReceiver = new BroadcastReceiver() {
                @Override
                public void onReceive(Context context, Intent intent) {
                    mRetryCount = 0;
                    refreshDashboard();
                    // Additional check after 1.5s for slow DHCP acquisition
                    mHandler.removeCallbacks(mRetryRunnable);
                    mHandler.postDelayed(mRetryRunnable, 1500);
                }
            };
            IntentFilter filter = new IntentFilter();
            filter.addAction(ConnectivityManager.CONNECTIVITY_ACTION);
            filter.addAction(Intent.ACTION_SCREEN_ON);
            try {
                registerReceiver(mNetworkReceiver, filter);
            } catch (Exception ignored) {}
        }
    }

    private void unregisterNetworkReceiver() {
        if (mNetworkReceiver != null) {
            try {
                unregisterReceiver(mNetworkReceiver);
            } catch (Exception ignored) {}
            mNetworkReceiver = null;
        }
    }

    private void setupTvButton(Button btn, View.OnClickListener clickListener) {
        btn.setFocusable(true);
        btn.setFocusableInTouchMode(true);
        btn.setOnClickListener(clickListener);

        // TV focus zoom animation
        btn.setOnFocusChangeListener((v, hasFocus) -> {
            if (hasFocus) {
                v.animate().scaleX(1.08f).scaleY(1.08f).setDuration(150).start();
            } else {
                v.animate().scaleX(1.0f).scaleY(1.0f).setDuration(150).start();
            }
        });
    }

    @Override
    protected void onResume() {
        super.onResume();
        mRetryCount = 0;
        refreshDashboard();
        // Hardware PHY re-negotiation & DHCP upon wake takes 1~3 seconds
        mHandler.removeCallbacks(mRetryRunnable);
        mHandler.postDelayed(mRetryRunnable, 1500);
        mHandler.postDelayed(mRetryRunnable, 3500);

        if (btnRefresh != null) {
            btnRefresh.post(() -> btnRefresh.requestFocus());
        }
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        mHandler.removeCallbacksAndMessages(null);
        unregisterNetworkReceiver();
    }

    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event) {
        if (keyCode == KeyEvent.KEYCODE_BACK) {
            finish();
            return true;
        }
        return super.onKeyDown(keyCode, event);
    }

    private void refreshDashboard() {
        String ip = HttpWebServer.getDeviceIpAddress();
        boolean isValidIp = ip != null && !ip.isEmpty() && !"127.0.0.1".equals(ip);

        if (isValidIp) {
            mRetryCount = 0;
            String url = "http://" + ip + ":" + WebPushService.PORT;
            tvUrl.setText(url);
            tvServiceStatus.setText("● 服务已就绪: 可在电脑/手机浏览器中打开");

            // Generate Standard ZXing QR code
            Bitmap qrBitmap = QRCodeGenerator.generateQRCode(url, 480);
            qrCodeView.setImageBitmap(qrBitmap);
        } else {
            String fallbackUrl = "http://127.0.0.1:" + WebPushService.PORT;
            tvUrl.setText("正在获取网络 IP (" + fallbackUrl + ")...");
            tvServiceStatus.setText("● 网络重连中，请稍候...");

            // If wake just occurred, auto retry up to 6 times (10 seconds total)
            if (mRetryCount < 6) {
                mRetryCount++;
                mHandler.removeCallbacks(mRetryRunnable);
                mHandler.postDelayed(mRetryRunnable, 1500);
            }
        }

        // Storage info
        try {
            StatFs stat = new StatFs(Environment.getExternalStorageDirectory().getPath());
            long blockSize = stat.getBlockSizeLong();
            long totalBlocks = stat.getBlockCountLong();
            long availableBlocks = stat.getAvailableBlocksLong();

            long totalBytes = totalBlocks * blockSize;
            long freeBytes = availableBlocks * blockSize;

            tvStorage.setText(String.format(Locale.getDefault(), "📦 闪存空间: %s 可用 / %s 总计", formatSize(freeBytes), formatSize(totalBytes)));
        } catch (Exception ignored) {
            tvStorage.setText("📦 闪存空间: 正常运行");
        }
    }

    private String formatSize(long bytes) {
        if (bytes < 1024) return bytes + " B";
        int z = (63 - Long.numberOfLeadingZeros(bytes)) / 10;
        return String.format(Locale.getDefault(), "%.1f %sB", (double) bytes / (1L << (z * 10)), " KMGTPE".charAt(z));
    }

    @Override
    public void onServerStarted(String ip, int port) {
        runOnUiThread(this::refreshDashboard);
    }

    @Override
    public void onFileReceived(String fileName, long sizeBytes, boolean autoInstalled) {
        runOnUiThread(() -> {
            refreshDashboard();
            String msg = "● 已接收: " + fileName + (autoInstalled ? " (已静默安装)" : "");
            tvServiceStatus.setText(msg);
            Toast.makeText(this, msg, Toast.LENGTH_LONG).show();
        });
    }

    @Override
    public void onClientConnected(String clientIp) {
        runOnUiThread(() -> tvServiceStatus.setText("● 设备已连接: " + clientIp));
    }
}
