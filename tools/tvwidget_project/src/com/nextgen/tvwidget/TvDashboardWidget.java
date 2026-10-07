package com.nextgen.tvwidget;

import android.app.PendingIntent;
import android.appwidget.AppWidgetManager;
import android.appwidget.AppWidgetProvider;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.widget.RemoteViews;

import java.util.Calendar;
import java.util.Date;

public class TvDashboardWidget extends AppWidgetProvider {

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
        if ("com.nextgen.tvwidget.ACTION_REFRESH".equals(action) ||
            Intent.ACTION_TIME_CHANGED.equals(action) ||
            Intent.ACTION_TIMEZONE_CHANGED.equals(action) ||
            Intent.ACTION_DATE_CHANGED.equals(action)) {
            WeatherHelper.forceRefresh(context);
            AppWidgetManager manager = AppWidgetManager.getInstance(context);
            ComponentName name = new ComponentName(context, TvDashboardWidget.class);
            int[] ids = manager.getAppWidgetIds(name);
            if (ids != null && ids.length > 0) {
                onUpdate(context, manager, ids);
            }
        }
    }

    public static void updateWidget(Context context, AppWidgetManager appWidgetManager, int appWidgetId) {
        RemoteViews views = new RemoteViews(context.getPackageName(), R.layout.widget_dashboard);

        // 1. Lunar Calendar
        Calendar cal = Calendar.getInstance();
        cal.setTime(new Date());
        String lunarStr = LunarCalendar.getLunarDateString(cal);
        views.setTextViewText(R.id.tv_widget_lunar, "·  " + lunarStr);

        // 2. Weather & City
        String weatherStr = WeatherHelper.getCurrentWeather(context);
        String cityStr = WeatherHelper.getCurrentCity(context);
        views.setTextViewText(R.id.tv_widget_weather, weatherStr);
        views.setTextViewText(R.id.tv_widget_city, "📍 " + cityStr);

        // 3. Network IP
        views.setTextViewText(R.id.tv_widget_ip, "🌐 " + SystemInfoHelper.getDeviceIpAddress());

        // 4. Hardware Monitor (Temp, RAM, Storage)
        int temp = SystemInfoHelper.getCpuTemperature();
        views.setTextViewText(R.id.tv_widget_temp, "🌡️ CPU " + temp + "°C");

        int ramUsage = SystemInfoHelper.getMemoryUsagePercent();
        views.setTextViewText(R.id.tv_widget_ram, "⚡ 内存 " + ramUsage + "%");

        String storageStr = SystemInfoHelper.getAvailableStorage();
        views.setTextViewText(R.id.tv_widget_storage, "📦 闪存 " + storageStr);

        // 5. Interactive Clicks
        // (1) Click Weather / City -> Open City Settings Dialog
        Intent cityIntent = new Intent(context, CitySettingsActivity.class);
        cityIntent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
        PendingIntent piCity = PendingIntent.getActivity(context, 101, cityIntent, PendingIntent.FLAG_UPDATE_CURRENT);
        views.setOnClickPendingIntent(R.id.tv_widget_city, piCity);
        views.setOnClickPendingIntent(R.id.tv_widget_weather, piCity);

        // (2) Click IP / Storage -> Open WebPush
        Intent webpushIntent = context.getPackageManager().getLaunchIntentForPackage("com.nextgen.webpush");
        if (webpushIntent != null) {
            PendingIntent piWebpush = PendingIntent.getActivity(context, 102, webpushIntent, PendingIntent.FLAG_UPDATE_CURRENT);
            views.setOnClickPendingIntent(R.id.tv_widget_ip, piWebpush);
            views.setOnClickPendingIntent(R.id.tv_widget_storage, piWebpush);
        }

        // (3) Click CPU Temp -> Refresh
        Intent refreshIntent = new Intent(context, TvDashboardWidget.class);
        refreshIntent.setAction("com.nextgen.tvwidget.ACTION_REFRESH");
        PendingIntent piRefresh = PendingIntent.getBroadcast(context, 103, refreshIntent, PendingIntent.FLAG_UPDATE_CURRENT);
        views.setOnClickPendingIntent(R.id.tv_widget_temp, piRefresh);

        appWidgetManager.updateAppWidget(appWidgetId, views);
    }
}
