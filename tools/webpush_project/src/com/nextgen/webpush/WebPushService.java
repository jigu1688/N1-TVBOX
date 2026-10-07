package com.nextgen.webpush;

import android.app.Notification;
import android.app.Service;
import android.content.Intent;
import android.os.IBinder;

public class WebPushService extends Service {

    public static final int PORT = 8888;
    private static HttpWebServer server;

    @Override
    public void onCreate() {
        super.onCreate();
        startServer();
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        startServer();
        return START_STICKY;
    }

    private synchronized void startServer() {
        if (server == null) {
            server = new HttpWebServer(this, PORT);
            try {
                server.start();
            } catch (Exception ignored) {}
        }
    }

    public static HttpWebServer getServer() {
        return server;
    }

    @Override
    public void onDestroy() {
        if (server != null) {
            server.stop();
            server = null;
        }
        super.onDestroy();
    }

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }
}
