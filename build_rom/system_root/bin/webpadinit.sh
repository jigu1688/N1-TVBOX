#!/system/bin/sh
# NextGen TV Initialization Script for Phicomm N1

# 1. SELinux Policies (Global Permissive & Per-domain Permissive)
setenforce 0 2>/dev/null
/system/xbin/supolicy --live --sdk=25
/system/xbin/supolicy --live "permissive init;permissive kernel;permissive untrusted_app;permissive toolbox;permissive shell;permissive priv_app;permissive bluetooth;permissive zygote;permissive system_server;"

# 2. Fix SU Root Binary Permissions & SELinux Contexts
mount -o remount,rw /system
chmod 4755 /system/xbin/su
chown root:shell /system/xbin/su
restorecon -Rv /system/etc/bluetooth 2>/dev/null
restorecon -Rv /system/app/WebPush 2>/dev/null
restorecon -Rv /system/app/NextGenWidget 2>/dev/null

# 3. Disable Lockscreen
settings put secure lockscreen.disabled 1
wm dismiss-keyguard

# 4. Enable Telnet Debugging Daemon (Port 2323)
/system/xbin/busybox telnetd -p 2323 -l /system/bin/sh &

# 5. Disable Phicomm smbd if present
stop smbd 2>/dev/null
killall smbd 2>/dev/null

# 6. Auto-grant Widget & Storage permissions
appops set ca.dstudio.atvlauncher.pro BIND_APPWIDGET allow 2>/dev/null
pm grant ca.dstudio.atvlauncher.pro android.permission.BIND_APPWIDGET 2>/dev/null
pm grant com.nextgen.webpush android.permission.WRITE_EXTERNAL_STORAGE 2>/dev/null
pm grant com.nextgen.webpush android.permission.READ_EXTERNAL_STORAGE 2>/dev/null
pm grant com.nextgen.tvwidget android.permission.WRITE_EXTERNAL_STORAGE 2>/dev/null
pm grant com.nextgen.tvwidget android.permission.READ_EXTERNAL_STORAGE 2>/dev/null
pm grant com.nextgen.tvwidget android.permission.ACCESS_NETWORK_STATE 2>/dev/null
pm grant com.nextgen.tvwidget android.permission.ACCESS_WIFI_STATE 2>/dev/null
pm grant com.nextgen.tvwidget android.permission.INTERNET 2>/dev/null

# 7. Initialize default wallpaper for ATV Launcher if needed
if [ ! -f /data/local/tmp/.atv_wp_init ]; then
    touch /data/local/tmp/.atv_wp_init
    mkdir -p /data/data/ca.dstudio.atvlauncher.pro/files
    cp /system/etc/default_wallpaper.png /data/data/ca.dstudio.atvlauncher.pro/files/wallpaper-source.png 2>/dev/null
    chmod 666 /data/data/ca.dstudio.atvlauncher.pro/files/wallpaper-source.png 2>/dev/null
fi

# 8. Ensure ATV Launcher directory permissions are always fully accessible (prevents missing icons bug)
if [ -d /data/data/ca.dstudio.atvlauncher.pro ]; then
    chmod -R 777 /data/data/ca.dstudio.atvlauncher.pro 2>/dev/null
fi

# Run background permission enforcer for first boot race condition
(
    for i in 1 2 3 4 5 6 7 8 9 10; do
        if [ -d /data/data/ca.dstudio.atvlauncher.pro ]; then
            chmod -R 777 /data/data/ca.dstudio.atvlauncher.pro 2>/dev/null
        fi
        sleep 2
    done
) >/dev/null 2>&1 &

# 9. Sleep Helper Daemon on localhost port 19999
chmod 755 /system/bin/do_sleep.sh 2>/dev/null
chmod 755 /system/bin/run_nc.sh 2>/dev/null
/system/bin/run_nc.sh >/dev/null 2>&1 &

# 10. Hardware Video Picture Quality Enhancement (VPP Brightness & Contrast Boost for SurfaceView)
settings put system screen_brightness 255 2>/dev/null
echo 15 > /sys/class/amvecm/brightness 2>/dev/null
echo 20 > /sys/class/amvecm/brightness1 2>/dev/null
echo 10 > /sys/class/amvecm/contrast1 2>/dev/null

exit 0
