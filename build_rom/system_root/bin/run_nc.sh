#!/system/bin/sh
# Persistent sleep listener daemon on port 19999
while true; do
    /system/xbin/busybox nc -l -p 19999 -e /system/bin/do_sleep.sh
    sleep 0.2
done
