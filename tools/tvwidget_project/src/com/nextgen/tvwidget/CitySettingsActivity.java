package com.nextgen.tvwidget;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

public class CitySettingsActivity extends Activity {

    private static final String[] POPULAR_CITIES = new String[]{
            "自动定位 (国内精准IP)",
            "北京", "上海", "广州", "深圳",
            "杭州", "成都", "武汉", "南京",
            "重庆", "天津", "西安", "苏州",
            "长沙", "郑州", "济南", "合肥",
            "福州", "青岛", "厦门", "沈阳",
            "大连", "昆明", "南宁", "自定义输入城市..."
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        ListView listView = new ListView(this);
        listView.setBackgroundColor(0xFF0F172A);
        listView.setDividerHeight(1);
        listView.setPadding(40, 20, 40, 20);

        TextView header = new TextView(this);
        header.setText("📍 选择天气所在城市 / 地区");
        header.setTextSize(22);
        header.setTextColor(0xFFFFFFFF);
        header.setPadding(20, 30, 20, 30);
        header.setGravity(Gravity.CENTER);
        listView.addHeaderView(header);

        ArrayAdapter<String> adapter = new ArrayAdapter<String>(this,
                android.R.layout.simple_list_item_1, POPULAR_CITIES) {
            @Override
            public View getView(int position, View convertView, ViewGroup parent) {
                TextView tv = (TextView) super.getView(position, convertView, parent);
                tv.setTextColor(0xFFE2E8F0);
                tv.setTextSize(18);
                tv.setPadding(24, 20, 24, 20);
                return tv;
            }
        };

        listView.setAdapter(adapter);
        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                if (position == 0) return; // Header
                String selected = POPULAR_CITIES[position - 1];
                if (selected.startsWith("自定义")) {
                    showCustomInputDialog();
                } else if (selected.startsWith("自动定位")) {
                    applyCity("自动定位");
                } else {
                    applyCity(selected);
                }
            }
        });

        setContentView(listView);
    }

    private void showCustomInputDialog() {
        final EditText input = new EditText(this);
        input.setHint("输入城市中文名 (如: 珠海 / 宁波)");
        input.setTextColor(0xFFFFFFFF);
        input.setPadding(30, 30, 30, 30);

        new AlertDialog.Builder(this)
                .setTitle("📍 输入自定义城市")
                .setView(input)
                .setPositiveButton("确定", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        String txt = input.getText().toString().trim();
                        if (!txt.isEmpty()) {
                            applyCity(txt);
                        }
                    }
                })
                .setNegativeButton("取消", null)
                .show();
    }

    private void applyCity(String city) {
        WeatherHelper.setCustomCity(this, city);
        Toast.makeText(this, "城市已设置为: " + city + "，正在刷新天气...", Toast.LENGTH_SHORT).show();

        // Broadcast to widgets
        Intent refreshDashboard = new Intent(this, TvDashboardWidget.class);
        refreshDashboard.setAction("com.nextgen.tvwidget.ACTION_REFRESH");
        sendBroadcast(refreshDashboard);

        Intent refreshClockWeather = new Intent(this, TvClockWeatherWidget.class);
        refreshClockWeather.setAction("com.nextgen.tvwidget.ACTION_REFRESH");
        sendBroadcast(refreshClockWeather);

        finish();
    }
}
