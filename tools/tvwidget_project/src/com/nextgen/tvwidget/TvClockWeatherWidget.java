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

public class TvClockWeatherWidget extends AppWidgetProvider {

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
            AppWidgetManager manager = AppWidgetManager.getInstance(context);
            ComponentName name = new ComponentName(context, TvClockWeatherWidget.class);
            int[] ids = manager.getAppWidgetIds(name);
            if (ids != null && ids.length > 0) {
                onUpdate(context, manager, ids);
            }
        }
    }

    public static void updateWidget(Context context, AppWidgetManager appWidgetManager, int appWidgetId) {
        RemoteViews views = new RemoteViews(context.getPackageName(), R.layout.widget_clock_weather);

        // 1. Lunar Calendar
        Calendar cal = Calendar.getInstance();
        cal.setTime(new Date());
        String lunarStr = LunarCalendar.getLunarDateString(cal);
        views.setTextViewText(R.id.tv_cw_lunar, "·  " + lunarStr);

        // 2. Weather & City
        String weatherStr = WeatherHelper.getCurrentWeather(context);
        String cityStr = WeatherHelper.getCurrentCity(context);
        views.setTextViewText(R.id.tv_cw_weather, weatherStr);
        views.setTextViewText(R.id.tv_cw_city, "📍 " + cityStr);

        // 3. Interactive Clicks
        Intent cityIntent = new Intent(context, CitySettingsActivity.class);
        cityIntent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
        PendingIntent piCity = PendingIntent.getActivity(context, 201, cityIntent, PendingIntent.FLAG_UPDATE_CURRENT);
        views.setOnClickPendingIntent(R.id.tv_cw_city, piCity);
        views.setOnClickPendingIntent(R.id.tv_cw_weather, piCity);

        appWidgetManager.updateAppWidget(appWidgetId, views);
    }
}
