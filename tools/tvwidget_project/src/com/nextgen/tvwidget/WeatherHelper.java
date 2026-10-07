package com.nextgen.tvwidget;

import android.content.Context;
import android.content.SharedPreferences;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;

public class WeatherHelper {

    private static final String PREF_NAME = "nextgen_weather_cache";
    private static long sLastFetchTime = 0;
    private static String sCachedWeather = "☀️ 晴 26°C";
    private static String sCachedCity = "北京";
    private static boolean sIsFetching = false;

    public static String getCurrentWeather(Context context) {
        loadCache(context);
        long now = System.currentTimeMillis();
        // Refresh every 15 minutes
        if (now - sLastFetchTime > 15 * 60 * 1000L && !sIsFetching) {
            forceRefresh(context);
        }
        return sCachedWeather;
    }

    public static String getCurrentCity(Context context) {
        loadCache(context);
        String custom = getCustomCity(context);
        if (custom != null && !custom.isEmpty() && !custom.equals("自动定位")) {
            return custom.replace("市", "");
        }
        return sCachedCity.replace("市", "");
    }

    public static String getCustomCity(Context context) {
        if (context == null) return null;
        SharedPreferences sp = context.getSharedPreferences(PREF_NAME, Context.MODE_PRIVATE);
        return sp.getString("custom_city", null);
    }

    public static void setCustomCity(Context context, String city) {
        if (context == null) return;
        SharedPreferences sp = context.getSharedPreferences(PREF_NAME, Context.MODE_PRIVATE);
        if (city == null || city.equals("自动定位")) {
            sp.edit().remove("custom_city").apply();
        } else {
            sp.edit().putString("custom_city", city).apply();
        }
        forceRefresh(context);
    }

    public static void forceRefresh(final Context context) {
        sLastFetchTime = 0;
        sIsFetching = false;
        fetchWeatherAsync(context, getCustomCity(context));
    }

    private static void loadCache(Context context) {
        if (sLastFetchTime == 0 && context != null) {
            SharedPreferences sp = context.getSharedPreferences(PREF_NAME, Context.MODE_PRIVATE);
            sCachedWeather = sp.getString("weather", "☀️ 晴 26°C");
            sCachedCity = sp.getString("city", "北京");
            sLastFetchTime = sp.getLong("time", 0);
        }
    }

    public static void fetchWeatherAsync(final Context context, final String customCity) {
        if (sIsFetching) return;
        sIsFetching = true;
        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    String queryCity = customCity;

                    // 1. If no custom city, fetch accurate domestic IP location
                    if (queryCity == null || queryCity.isEmpty() || queryCity.equals("自动定位")) {
                        queryCity = fetchDomesticCityName();
                    }

                    if (queryCity == null || queryCity.isEmpty()) {
                        queryCity = "北京";
                    }

                    // 2. Fetch weather using wttr.in with native Chinese language support (&lang=zh)
                    String urlStr = "http://wttr.in/" + URLEncoder.encode(queryCity, "UTF-8") + "?format=j1&lang=zh";
                    URL url = new URL(urlStr);
                    HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                    conn.setConnectTimeout(4000);
                    conn.setReadTimeout(4000);
                    conn.setRequestMethod("GET");
                    conn.setRequestProperty("User-Agent", "curl/7.68.0");
                    conn.setRequestProperty("Accept-Language", "zh-CN,zh;q=0.9");

                    if (conn.getResponseCode() == 200) {
                        BufferedReader br = new BufferedReader(new InputStreamReader(conn.getInputStream(), "UTF-8"));
                        StringBuilder sb = new StringBuilder();
                        String line;
                        while ((line = br.readLine()) != null) {
                            sb.append(line);
                        }
                        br.close();

                        JSONObject root = new JSONObject(sb.toString());
                        JSONObject current = root.getJSONArray("current_condition").getJSONObject(0);
                        String tempC = current.optString("temp_C", "26");

                        // Extract Chinese description (prioritize lang_zh)
                        String descZh = "";
                        if (current.has("lang_zh")) {
                            JSONArray zhArr = current.getJSONArray("lang_zh");
                            if (zhArr.length() > 0) {
                                descZh = zhArr.getJSONObject(0).optString("value", "");
                            }
                        }

                        // Fallback to weatherDesc with comprehensive translation
                        if (descZh.isEmpty() || descZh.matches(".*[a-zA-Z].*")) {
                            String rawDesc = current.getJSONArray("weatherDesc").getJSONObject(0).optString("value", "");
                            descZh = translateWeatherToChinese(rawDesc);
                        }

                        String emoji = getWeatherEmoji(descZh);

                        sCachedWeather = emoji + " " + descZh + " " + tempC + "°C";
                        sCachedCity = queryCity.replace("市", "");
                        sLastFetchTime = System.currentTimeMillis();

                        if (context != null) {
                            SharedPreferences sp = context.getSharedPreferences(PREF_NAME, Context.MODE_PRIVATE);
                            sp.edit().putString("weather", sCachedWeather)
                                     .putString("city", sCachedCity)
                                     .putLong("time", sLastFetchTime)
                                     .apply();
                        }
                    }
                } catch (Exception ignored) {
                } finally {
                    sIsFetching = false;
                }
            }
        }).start();
    }

    private static String translateWeatherToChinese(String raw) {
        if (raw == null || raw.isEmpty()) return "晴";
        String s = raw.toLowerCase();
        if (s.contains("sunny") || s.contains("clear")) return "晴";
        if (s.contains("partly cloudy") || s.contains("partly")) return "多云";
        if (s.contains("cloud") || s.contains("overcast")) return "阴";
        if (s.contains("thunder") || s.contains("storm")) return "雷阵雨";
        if (s.contains("heavy rain")) return "大雨";
        if (s.contains("moderate rain")) return "中雨";
        if (s.contains("light rain") || s.contains("patchy rain") || s.contains("drizzle")) return "小雨";
        if (s.contains("rain") || s.contains("shower")) return "阵雨";
        if (s.contains("snow") || s.contains("blizzard")) return "雪";
        if (s.contains("sleet")) return "雨夹雪";
        if (s.contains("haze") || s.contains("smoke")) return "霾";
        if (s.contains("fog") || s.contains("mist")) return "雾";
        if (s.contains("wind")) return "大风";
        if (s.contains("sand") || s.contains("dust")) return "沙尘";
        return "晴";
    }

    private static String getWeatherEmoji(String desc) {
        if (desc.contains("晴")) return "☀️";
        if (desc.contains("多云")) return "⛅";
        if (desc.contains("阴")) return "☁️";
        if (desc.contains("雷")) return "⛈️";
        if (desc.contains("雨")) return "🌧️";
        if (desc.contains("雪")) return "❄️";
        if (desc.contains("霾") || desc.contains("雾")) return "🌫️";
        if (desc.contains("风")) return "🍃";
        return "🌤️";
    }

    private static String fetchDomesticCityName() {
        try {
            // High-precision domestic IP locator (PConline / Sohu)
            URL url = new URL("https://whois.pconline.com.cn/ipJson.jsp?json=true");
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setConnectTimeout(3000);
            conn.setReadTimeout(3000);
            conn.setRequestMethod("GET");
            conn.setRequestProperty("User-Agent", "Mozilla/5.0");

            if (conn.getResponseCode() == 200) {
                BufferedReader br = new BufferedReader(new InputStreamReader(conn.getInputStream(), "GBK"));
                StringBuilder sb = new StringBuilder();
                String line;
                while ((line = br.readLine()) != null) {
                    sb.append(line);
                }
                br.close();

                JSONObject obj = new JSONObject(sb.toString().trim());
                String city = obj.optString("city", "");
                if (city.isEmpty()) city = obj.optString("pro", "");
                if (!city.isEmpty()) {
                    return city.replace("市", "");
                }
            }
        } catch (Exception ignored) {}
        return "北京";
    }
}
