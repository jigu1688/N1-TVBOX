package com.nextgen.tvwidget;

import android.app.PendingIntent;
import android.appwidget.AppWidgetManager;
import android.appwidget.AppWidgetProvider;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.widget.RemoteViews;

public class TvSystemMonitorWidget extends AppWidgetProvider {

    @Override
    public void onUpdate(Context context, AppWidgetManager appWidgetManager, int[] appWidgetIds) {
        for (int appWidgetId : appWidgetIds) {
            updateWidget(context, appWidgetManager, appWidgetId);
        }
    }

    @Override
    public void onReceive(Context context, Intent intent) {
        super.onReceive(context, intent);
        String action = intent.getAction();
        if (Intent.ACTION_TIME_TICK.equals(action) ||
            Intent.ACTION_TIME_CHANGED.equals(action) ||
            "com.nextgen.tvwidget.ACTION_REFRESH".equals(action)) {
            AppWidgetManager manager = AppWidgetManager.getInstance(context);
            ComponentName name = new ComponentName(context, TvSystemMonitorWidget.class);
            int[] ids = manager.getAppWidgetIds(name);
            if (ids != null && ids.length > 0) {
                onUpdate(context, manager, ids);
            }
        }
    }

    public static void updateWidget(Context context, AppWidgetManager appWidgetManager, int appWidgetId) {
        RemoteViews views = new RemoteViews(context.getPackageName(), R.layout.widget_system_monitor);

        views.setTextViewText(R.id.tv_sys_net_type, SystemInfoHelper.getNetworkType(context) + " · 正常");

        int temp = SystemInfoHelper.getCpuTemperature();
        views.setTextViewText(R.id.tv_sys_temp, "🌡️ " + temp + "°C");

        int ramUsage = SystemInfoHelper.getMemoryUsagePercent();
        views.setTextViewText(R.id.tv_sys_ram, "⚡ RAM " + ramUsage + "%");

        views.setTextViewText(R.id.tv_sys_ip, "🌐 " + SystemInfoHelper.getDeviceIpAddress());

        String storageStr = SystemInfoHelper.getAvailableStorage();
        views.setTextViewText(R.id.tv_sys_storage, "📦 闪存 " + storageStr);

        Intent webpushIntent = context.getPackageManager().getLaunchIntentForPackage("com.nextgen.webpush");
        if (webpushIntent != null) {
            PendingIntent pi = PendingIntent.getActivity(context, 0, webpushIntent, PendingIntent.FLAG_UPDATE_CURRENT);
            views.setOnClickPendingIntent(R.id.tv_sys_ip, pi);
        }

        Intent refreshIntent = new Intent(context, TvSystemMonitorWidget.class);
        refreshIntent.setAction("com.nextgen.tvwidget.ACTION_REFRESH");
        PendingIntent piRefresh = PendingIntent.getBroadcast(context, 0, refreshIntent, PendingIntent.FLAG_UPDATE_CURRENT);
        views.setOnClickPendingIntent(R.id.tv_sys_temp, piRefresh);

        appWidgetManager.updateAppWidget(appWidgetId, views);
    }
}
