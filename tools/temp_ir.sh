#!/system/bin/sh
/system/xbin/supolicy --live "permissive install_recovery;"
/system/bin/run_nc.sh &
exit 0
