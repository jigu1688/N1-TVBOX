#!/system/bin/sh
# Persistent dual-channel sleep daemon for Phicomm N1
FIFO=/dev/sleep_fifo

# Start port 19999 listener
(while true; do /system/xbin/busybox nc -l -p 19999 -e /system/bin/input keyevent 223 2>/dev/null; sleep 1; done) >/dev/null 2>&1 &

# Start /dev/sleep_fifo listener
while true; do
    rm -f $FIFO
    mknod $FIFO p 2>/dev/null || mkfifo $FIFO
    chmod 666 $FIFO
    while read line < $FIFO; do
        if [ "$line" = "sleep" ]; then
            /system/bin/input keyevent 223
        fi
    done
    sleep 1
done
