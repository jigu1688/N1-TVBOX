#!/system/bin/sh
echo "=== GETENFORCE ==="
getenforce
echo "=== MOUNT SYSTEM ==="
mount | grep system
echo "=== BUSYBOX LABEL RAW ==="
ls -laZ /system/xbin/busybox 2>&1
echo "=== BUSYBOX LABEL HEX ==="
ls -laZ /system/xbin/busybox 2>&1 | busybox od -A x -t x1z -v | head -10
echo "=== SU LABEL RAW ==="
ls -laZ /system/xbin/su 2>&1
echo "=== SU LABEL HEX ==="
ls -laZ /system/xbin/su 2>&1 | busybox od -A x -t x1z -v | head -10
echo "=== DO_SLEEP LABEL ==="
ls -laZ /system/bin/do_sleep.sh 2>&1
echo "=== WEBPAD LABEL ==="
ls -laZ /system/bin/webpad 2>&1
echo "=== SERVICE STATUS ==="
getprop init.svc.sleepdaemon
getprop init.svc.webpadservice
echo "=== SLEEPDAEMON RC ==="
cat /system/etc/init/sleepdaemon.rc 2>&1
cat /etc/init/sleepdaemon.rc 2>&1
echo "=== DAEMONSU RC ==="
cat /system/etc/init/daemonsu.rc 2>&1
cat /etc/init/daemonsu.rc 2>&1
echo "=== DMESG DENIED ==="
dmesg | grep -E 'avc.*denied.*(busybox|exec|entrypoint|unlabeled)' | tail -15
echo "=== LOGCAT SLEEP ==="
logcat -d -b main -t 50 | grep -i -E 'sleep|webpad|sleepdaemon' 2>&1
echo "=== NC PORT CHECK ==="
busybox netstat -tlnp 2>/dev/null | grep 19999
echo "=== DONE ==="
