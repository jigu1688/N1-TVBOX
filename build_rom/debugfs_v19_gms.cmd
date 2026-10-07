rm /app/PhiNasDMS/PhiNasDMS.apk
rmdir /app/PhiNasDMS/oat/arm
rmdir /app/PhiNasDMS/oat
rmdir /app/PhiNasDMS
rm /app/PhiNasImagePlayer/PhiNasImagePlayer.apk
rmdir /app/PhiNasImagePlayer/oat/arm
rmdir /app/PhiNasImagePlayer/oat
rmdir /app/PhiNasImagePlayer
rm /app/PhiTvMusic/PhiTvMusic.apk
rmdir /app/PhiTvMusic/oat/arm
rmdir /app/PhiTvMusic/oat
rmdir /app/PhiTvMusic
rm /app/PhiTvVideoPlayer/PhiTvVideoPlayer.apk
rmdir /app/PhiTvVideoPlayer/oat/arm
rmdir /app/PhiTvVideoPlayer/oat
rmdir /app/PhiTvVideoPlayer
rm /app/webview/webview.apk
rm /app/webview/oat/arm/webview.odex
rm /app/webview/oat/arm64/webview.odex
rmdir /app/webview/oat/arm
rmdir /app/webview/oat/arm64
rmdir /app/webview/oat
rmdir /app/webview
mkdir /priv-app/Provision
set_inode_field /priv-app/Provision mode 040755
set_inode_field /priv-app/Provision uid 0
set_inode_field /priv-app/Provision gid 0
write extracted_webpad/system_root/priv-app/Provision/Provision.apk /priv-app/Provision/Provision.apk
set_inode_field /priv-app/Provision/Provision.apk mode 0100644
set_inode_field /priv-app/Provision/Provision.apk uid 0
set_inode_field /priv-app/Provision/Provision.apk gid 0
mkdir /app/ATVLauncher
set_inode_field /app/ATVLauncher mode 040755
set_inode_field /app/ATVLauncher uid 0
set_inode_field /app/ATVLauncher gid 0
write build_rom/system_root/app/ATVLauncher/ATVLauncher.apk /app/ATVLauncher/ATVLauncher.apk
set_inode_field /app/ATVLauncher/ATVLauncher.apk mode 0100644
set_inode_field /app/ATVLauncher/ATVLauncher.apk uid 0
set_inode_field /app/ATVLauncher/ATVLauncher.apk gid 0
mkdir /app/WebViewGoogle
set_inode_field /app/WebViewGoogle mode 040755
set_inode_field /app/WebViewGoogle uid 0
set_inode_field /app/WebViewGoogle gid 0
write build_rom/system_root/app/WebViewGoogle/WebViewGoogle.apk /app/WebViewGoogle/WebViewGoogle.apk
set_inode_field /app/WebViewGoogle/WebViewGoogle.apk mode 0100644
set_inode_field /app/WebViewGoogle/WebViewGoogle.apk uid 0
set_inode_field /app/WebViewGoogle/WebViewGoogle.apk gid 0
rm /framework/framework-res.apk
write build_rom/system_root/framework/framework-res.apk /framework/framework-res.apk
set_inode_field /framework/framework-res.apk mode 0100644
set_inode_field /framework/framework-res.apk uid 0
set_inode_field /framework/framework-res.apk gid 0
mkdir /priv-app/PhiTvSettings
set_inode_field /priv-app/PhiTvSettings mode 040755
set_inode_field /priv-app/PhiTvSettings uid 0
set_inode_field /priv-app/PhiTvSettings gid 0
write build_rom/system_root/priv-app/PhiTvSettings/PhiTvSettings.apk /priv-app/PhiTvSettings/PhiTvSettings.apk
set_inode_field /priv-app/PhiTvSettings/PhiTvSettings.apk mode 0100644
set_inode_field /priv-app/PhiTvSettings/PhiTvSettings.apk uid 0
set_inode_field /priv-app/PhiTvSettings/PhiTvSettings.apk gid 0
mkdir /app/NextGenWidget
set_inode_field /app/NextGenWidget mode 040755
set_inode_field /app/NextGenWidget uid 0
set_inode_field /app/NextGenWidget gid 0
write tools/NextGen_TVWidget.apk /app/NextGenWidget/NextGenWidget.apk
set_inode_field /app/NextGenWidget/NextGenWidget.apk mode 0100644
set_inode_field /app/NextGenWidget/NextGenWidget.apk uid 0
set_inode_field /app/NextGenWidget/NextGenWidget.apk gid 0
mkdir /app/WebPush
set_inode_field /app/WebPush mode 040755
set_inode_field /app/WebPush uid 0
set_inode_field /app/WebPush gid 0
write tools/WebPush.apk /app/WebPush/WebPush.apk
set_inode_field /app/WebPush/WebPush.apk mode 0100644
set_inode_field /app/WebPush/WebPush.apk uid 0
set_inode_field /app/WebPush/WebPush.apk gid 0
rm /app/FileBrowser/FileBrowser.apk
write tools/FileBrowser_TV_HD.apk /app/FileBrowser/FileBrowser.apk
set_inode_field /app/FileBrowser/FileBrowser.apk mode 0100644
set_inode_field /app/FileBrowser/FileBrowser.apk uid 0
set_inode_field /app/FileBrowser/FileBrowser.apk gid 0
write build_rom/system_root/etc/default_wallpaper.png /etc/default_wallpaper.png
set_inode_field /etc/default_wallpaper.png mode 0100644
set_inode_field /etc/default_wallpaper.png uid 0
set_inode_field /etc/default_wallpaper.png gid 0
mkdir /etc/atvlauncher
set_inode_field /etc/atvlauncher mode 040755
set_inode_field /etc/atvlauncher uid 0
set_inode_field /etc/atvlauncher gid 0
write build_rom/system_root/etc/atvlauncher/sections.db /etc/atvlauncher/sections.db
set_inode_field /etc/atvlauncher/sections.db mode 0100644
set_inode_field /etc/atvlauncher/sections.db uid 0
set_inode_field /etc/atvlauncher/sections.db gid 0
write build_rom/system_root/xbin/su /xbin/su
set_inode_field /xbin/su mode 0104755
set_inode_field /xbin/su uid 0
set_inode_field /xbin/su gid 2000
write build_rom/system_root/xbin/daemonsu /xbin/daemonsu
set_inode_field /xbin/daemonsu mode 0100755
set_inode_field /xbin/daemonsu uid 0
set_inode_field /xbin/daemonsu gid 2000
write build_rom/system_root/xbin/supolicy /xbin/supolicy
set_inode_field /xbin/supolicy mode 0100755
set_inode_field /xbin/supolicy uid 0
set_inode_field /xbin/supolicy gid 2000
write build_rom/system_root/lib64/libsupol.so /lib64/libsupol.so
set_inode_field /lib64/libsupol.so mode 0100644
set_inode_field /lib64/libsupol.so uid 0
set_inode_field /lib64/libsupol.so gid 0
write build_rom/system_root/xbin/busybox /xbin/busybox
set_inode_field /xbin/busybox mode 0100755
set_inode_field /xbin/busybox uid 0
set_inode_field /xbin/busybox gid 2000
write build_rom/system_root/bin/webpad /bin/webpad
set_inode_field /bin/webpad mode 0100755
set_inode_field /bin/webpad uid 0
set_inode_field /bin/webpad gid 2000
write build_rom/system_root/bin/webpadinit.sh /bin/webpadinit.sh
set_inode_field /bin/webpadinit.sh mode 0100755
set_inode_field /bin/webpadinit.sh uid 0
set_inode_field /bin/webpadinit.sh gid 2000
write build_rom/system_root/etc/init/daemonsu.rc /etc/init/daemonsu.rc
set_inode_field /etc/init/daemonsu.rc mode 0100644
set_inode_field /etc/init/daemonsu.rc uid 0
set_inode_field /etc/init/daemonsu.rc gid 0
rm /etc/bluetooth/bt_stack.conf
write build_rom/system_root/etc/bluetooth/bt_stack.conf /etc/bluetooth/bt_stack.conf
set_inode_field /etc/bluetooth/bt_stack.conf mode 0100644
set_inode_field /etc/bluetooth/bt_stack.conf uid 0
set_inode_field /etc/bluetooth/bt_stack.conf gid 0
write build_rom/system_root/usr/keylayout/Generic.kl /usr/keylayout/Generic.kl
set_inode_field /usr/keylayout/Generic.kl mode 0100644
set_inode_field /usr/keylayout/Generic.kl uid 0
set_inode_field /usr/keylayout/Generic.kl gid 0
write build_rom/system_root/usr/keylayout/Vendor_0001_Product_0001.kl /usr/keylayout/Vendor_0001_Product_0001.kl
set_inode_field /usr/keylayout/Vendor_0001_Product_0001.kl mode 0100644
set_inode_field /usr/keylayout/Vendor_0001_Product_0001.kl uid 0
set_inode_field /usr/keylayout/Vendor_0001_Product_0001.kl gid 0
rm /build.prop
write build_rom/system_root/build.prop /build.prop
set_inode_field /build.prop mode 0100644
set_inode_field /build.prop uid 0
set_inode_field /build.prop gid 0
mkdir /app/GoogleCalendarSyncAdapter
set_inode_field /app/GoogleCalendarSyncAdapter mode 040755
rm /app/GoogleCalendarSyncAdapter/GoogleCalendarSyncAdapter.apk
write tools/gms_system_clean/app/GoogleCalendarSyncAdapter/GoogleCalendarSyncAdapter.apk /app/GoogleCalendarSyncAdapter/GoogleCalendarSyncAdapter.apk
set_inode_field /app/GoogleCalendarSyncAdapter/GoogleCalendarSyncAdapter.apk mode 0100644
set_inode_field /app/GoogleCalendarSyncAdapter/GoogleCalendarSyncAdapter.apk uid 0
set_inode_field /app/GoogleCalendarSyncAdapter/GoogleCalendarSyncAdapter.apk gid 0
mkdir /app/GoogleContactsSyncAdapter
set_inode_field /app/GoogleContactsSyncAdapter mode 040755
rm /app/GoogleContactsSyncAdapter/GoogleContactsSyncAdapter.apk
write tools/gms_system_clean/app/GoogleContactsSyncAdapter/GoogleContactsSyncAdapter.apk /app/GoogleContactsSyncAdapter/GoogleContactsSyncAdapter.apk
set_inode_field /app/GoogleContactsSyncAdapter/GoogleContactsSyncAdapter.apk mode 0100644
set_inode_field /app/GoogleContactsSyncAdapter/GoogleContactsSyncAdapter.apk uid 0
set_inode_field /app/GoogleContactsSyncAdapter/GoogleContactsSyncAdapter.apk gid 0
mkdir /app/GoogleExtShared
set_inode_field /app/GoogleExtShared mode 040755
rm /app/GoogleExtShared/GoogleExtShared.apk
write tools/gms_system_clean/app/GoogleExtShared/GoogleExtShared.apk /app/GoogleExtShared/GoogleExtShared.apk
set_inode_field /app/GoogleExtShared/GoogleExtShared.apk mode 0100644
set_inode_field /app/GoogleExtShared/GoogleExtShared.apk uid 0
set_inode_field /app/GoogleExtShared/GoogleExtShared.apk gid 0
mkdir /etc/default-permissions
set_inode_field /etc/default-permissions mode 040755
rm /etc/default-permissions/default-permissions.xml
write tools/gms_system_clean/etc/default-permissions/default-permissions.xml /etc/default-permissions/default-permissions.xml
set_inode_field /etc/default-permissions/default-permissions.xml mode 0100644
set_inode_field /etc/default-permissions/default-permissions.xml uid 0
set_inode_field /etc/default-permissions/default-permissions.xml gid 0
rm /etc/default-permissions/opengapps-permissions.xml
write tools/gms_system_clean/etc/default-permissions/opengapps-permissions.xml /etc/default-permissions/opengapps-permissions.xml
set_inode_field /etc/default-permissions/opengapps-permissions.xml mode 0100644
set_inode_field /etc/default-permissions/opengapps-permissions.xml uid 0
set_inode_field /etc/default-permissions/opengapps-permissions.xml gid 0
mkdir /etc/permissions
set_inode_field /etc/permissions mode 040755
rm /etc/permissions/com.google.android.dialer.support.xml
write tools/gms_system_clean/etc/permissions/com.google.android.dialer.support.xml /etc/permissions/com.google.android.dialer.support.xml
set_inode_field /etc/permissions/com.google.android.dialer.support.xml mode 0100644
set_inode_field /etc/permissions/com.google.android.dialer.support.xml uid 0
set_inode_field /etc/permissions/com.google.android.dialer.support.xml gid 0
rm /etc/permissions/com.google.android.maps.xml
write tools/gms_system_clean/etc/permissions/com.google.android.maps.xml /etc/permissions/com.google.android.maps.xml
set_inode_field /etc/permissions/com.google.android.maps.xml mode 0100644
set_inode_field /etc/permissions/com.google.android.maps.xml uid 0
set_inode_field /etc/permissions/com.google.android.maps.xml gid 0
rm /etc/permissions/com.google.android.media.effects.xml
write tools/gms_system_clean/etc/permissions/com.google.android.media.effects.xml /etc/permissions/com.google.android.media.effects.xml
set_inode_field /etc/permissions/com.google.android.media.effects.xml mode 0100644
set_inode_field /etc/permissions/com.google.android.media.effects.xml uid 0
set_inode_field /etc/permissions/com.google.android.media.effects.xml gid 0
mkdir /etc/preferred-apps
set_inode_field /etc/preferred-apps mode 040755
rm /etc/preferred-apps/google.xml
write tools/gms_system_clean/etc/preferred-apps/google.xml /etc/preferred-apps/google.xml
set_inode_field /etc/preferred-apps/google.xml mode 0100644
set_inode_field /etc/preferred-apps/google.xml uid 0
set_inode_field /etc/preferred-apps/google.xml gid 0
mkdir /etc/sysconfig
set_inode_field /etc/sysconfig mode 040755
rm /etc/sysconfig/dialer_experience.xml
write tools/gms_system_clean/etc/sysconfig/dialer_experience.xml /etc/sysconfig/dialer_experience.xml
set_inode_field /etc/sysconfig/dialer_experience.xml mode 0100644
set_inode_field /etc/sysconfig/dialer_experience.xml uid 0
set_inode_field /etc/sysconfig/dialer_experience.xml gid 0
rm /etc/sysconfig/google.xml
write tools/gms_system_clean/etc/sysconfig/google.xml /etc/sysconfig/google.xml
set_inode_field /etc/sysconfig/google.xml mode 0100644
set_inode_field /etc/sysconfig/google.xml uid 0
set_inode_field /etc/sysconfig/google.xml gid 0
rm /etc/sysconfig/google_build.xml
write tools/gms_system_clean/etc/sysconfig/google_build.xml /etc/sysconfig/google_build.xml
set_inode_field /etc/sysconfig/google_build.xml mode 0100644
set_inode_field /etc/sysconfig/google_build.xml uid 0
set_inode_field /etc/sysconfig/google_build.xml gid 0
rm /etc/sysconfig/google_exclusives_enable.xml
write tools/gms_system_clean/etc/sysconfig/google_exclusives_enable.xml /etc/sysconfig/google_exclusives_enable.xml
set_inode_field /etc/sysconfig/google_exclusives_enable.xml mode 0100644
set_inode_field /etc/sysconfig/google_exclusives_enable.xml uid 0
set_inode_field /etc/sysconfig/google_exclusives_enable.xml gid 0
rm /framework/com.google.android.dialer.support.jar
write tools/gms_system_clean/framework/com.google.android.dialer.support.jar /framework/com.google.android.dialer.support.jar
set_inode_field /framework/com.google.android.dialer.support.jar mode 0100644
set_inode_field /framework/com.google.android.dialer.support.jar uid 0
set_inode_field /framework/com.google.android.dialer.support.jar gid 0
rm /framework/com.google.android.maps.jar
write tools/gms_system_clean/framework/com.google.android.maps.jar /framework/com.google.android.maps.jar
set_inode_field /framework/com.google.android.maps.jar mode 0100644
set_inode_field /framework/com.google.android.maps.jar uid 0
set_inode_field /framework/com.google.android.maps.jar gid 0
rm /framework/com.google.android.media.effects.jar
write tools/gms_system_clean/framework/com.google.android.media.effects.jar /framework/com.google.android.media.effects.jar
set_inode_field /framework/com.google.android.media.effects.jar mode 0100644
set_inode_field /framework/com.google.android.media.effects.jar uid 0
set_inode_field /framework/com.google.android.media.effects.jar gid 0
mkdir /priv-app/ConfigUpdater
set_inode_field /priv-app/ConfigUpdater mode 040755
rm /priv-app/ConfigUpdater/ConfigUpdater.apk
write tools/gms_system_clean/priv-app/ConfigUpdater/ConfigUpdater.apk /priv-app/ConfigUpdater/ConfigUpdater.apk
set_inode_field /priv-app/ConfigUpdater/ConfigUpdater.apk mode 0100644
set_inode_field /priv-app/ConfigUpdater/ConfigUpdater.apk uid 0
set_inode_field /priv-app/ConfigUpdater/ConfigUpdater.apk gid 0
mkdir /priv-app/GoogleBackupTransport
set_inode_field /priv-app/GoogleBackupTransport mode 040755
rm /priv-app/GoogleBackupTransport/GoogleBackupTransport.apk
write tools/gms_system_clean/priv-app/GoogleBackupTransport/GoogleBackupTransport.apk /priv-app/GoogleBackupTransport/GoogleBackupTransport.apk
set_inode_field /priv-app/GoogleBackupTransport/GoogleBackupTransport.apk mode 0100644
set_inode_field /priv-app/GoogleBackupTransport/GoogleBackupTransport.apk uid 0
set_inode_field /priv-app/GoogleBackupTransport/GoogleBackupTransport.apk gid 0
mkdir /priv-app/GoogleExtServices
set_inode_field /priv-app/GoogleExtServices mode 040755
rm /priv-app/GoogleExtServices/GoogleExtServices.apk
write tools/gms_system_clean/priv-app/GoogleExtServices/GoogleExtServices.apk /priv-app/GoogleExtServices/GoogleExtServices.apk
set_inode_field /priv-app/GoogleExtServices/GoogleExtServices.apk mode 0100644
set_inode_field /priv-app/GoogleExtServices/GoogleExtServices.apk uid 0
set_inode_field /priv-app/GoogleExtServices/GoogleExtServices.apk gid 0
mkdir /priv-app/GoogleFeedback
set_inode_field /priv-app/GoogleFeedback mode 040755
rm /priv-app/GoogleFeedback/GoogleFeedback.apk
write tools/gms_system_clean/priv-app/GoogleFeedback/GoogleFeedback.apk /priv-app/GoogleFeedback/GoogleFeedback.apk
set_inode_field /priv-app/GoogleFeedback/GoogleFeedback.apk mode 0100644
set_inode_field /priv-app/GoogleFeedback/GoogleFeedback.apk uid 0
set_inode_field /priv-app/GoogleFeedback/GoogleFeedback.apk gid 0
mkdir /priv-app/GoogleLoginService
set_inode_field /priv-app/GoogleLoginService mode 040755
rm /priv-app/GoogleLoginService/GoogleLoginService.apk
write tools/gms_system_clean/priv-app/GoogleLoginService/GoogleLoginService.apk /priv-app/GoogleLoginService/GoogleLoginService.apk
set_inode_field /priv-app/GoogleLoginService/GoogleLoginService.apk mode 0100644
set_inode_field /priv-app/GoogleLoginService/GoogleLoginService.apk uid 0
set_inode_field /priv-app/GoogleLoginService/GoogleLoginService.apk gid 0
mkdir /priv-app/GooglePartnerSetup
set_inode_field /priv-app/GooglePartnerSetup mode 040755
rm /priv-app/GooglePartnerSetup/GooglePartnerSetup.apk
write tools/gms_system_clean/priv-app/GooglePartnerSetup/GooglePartnerSetup.apk /priv-app/GooglePartnerSetup/GooglePartnerSetup.apk
set_inode_field /priv-app/GooglePartnerSetup/GooglePartnerSetup.apk mode 0100644
set_inode_field /priv-app/GooglePartnerSetup/GooglePartnerSetup.apk uid 0
set_inode_field /priv-app/GooglePartnerSetup/GooglePartnerSetup.apk gid 0
mkdir /priv-app/GoogleServicesFramework
set_inode_field /priv-app/GoogleServicesFramework mode 040755
rm /priv-app/GoogleServicesFramework/GoogleServicesFramework.apk
write tools/gms_system_clean/priv-app/GoogleServicesFramework/GoogleServicesFramework.apk /priv-app/GoogleServicesFramework/GoogleServicesFramework.apk
set_inode_field /priv-app/GoogleServicesFramework/GoogleServicesFramework.apk mode 0100644
set_inode_field /priv-app/GoogleServicesFramework/GoogleServicesFramework.apk uid 0
set_inode_field /priv-app/GoogleServicesFramework/GoogleServicesFramework.apk gid 0
mkdir /priv-app/Phonesky
set_inode_field /priv-app/Phonesky mode 040755
rm /priv-app/Phonesky/Phonesky.apk
write tools/gms_system_clean/priv-app/Phonesky/Phonesky.apk /priv-app/Phonesky/Phonesky.apk
set_inode_field /priv-app/Phonesky/Phonesky.apk mode 0100644
set_inode_field /priv-app/Phonesky/Phonesky.apk uid 0
set_inode_field /priv-app/Phonesky/Phonesky.apk gid 0
mkdir /priv-app/PrebuiltGmsCore
set_inode_field /priv-app/PrebuiltGmsCore mode 040755
rm /priv-app/PrebuiltGmsCore/PrebuiltGmsCore.apk
write tools/gms_system_clean/priv-app/PrebuiltGmsCore/PrebuiltGmsCore.apk /priv-app/PrebuiltGmsCore/PrebuiltGmsCore.apk
set_inode_field /priv-app/PrebuiltGmsCore/PrebuiltGmsCore.apk mode 0100644
set_inode_field /priv-app/PrebuiltGmsCore/PrebuiltGmsCore.apk uid 0
set_inode_field /priv-app/PrebuiltGmsCore/PrebuiltGmsCore.apk gid 0
q
