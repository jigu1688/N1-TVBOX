import subprocess
import time

def deploy():
    adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
    dev = '192.168.31.114:5555'

    print('[*] Connecting ADB...')
    subprocess.run([adb, 'connect', dev])
    subprocess.run([adb, '-s', dev, 'shell', 'mount', '-o', 'remount,rw', '/system'])

    # 1. Remove XiaoBai from system & data
    print('[*] Removing XiaoBaiFile from system...')
    subprocess.run([adb, '-s', dev, 'shell', 'rm', '-rf', '/system/app/XiaoBaiFile'])
    subprocess.run([adb, '-s', dev, 'shell', 'pm', 'uninstall', 'com.xiaobaifile.tv'])

    # 2. Push WebPush APK into /system/app/WebPush
    print('[*] Pushing WebPush.apk into /system/app/WebPush/...')
    subprocess.run([adb, '-s', dev, 'shell', 'mkdir', '-p', '/system/app/WebPush'])
    subprocess.run([adb, '-s', dev, 'push', 'tools/WebPush.apk', '/system/app/WebPush/WebPush.apk'])
    subprocess.run([adb, '-s', dev, 'shell', 'chmod', '644', '/system/app/WebPush/WebPush.apk'])

    # 3. Disable BtSnoop logging in bt_stack.conf
    print('[*] Disabling BtSnoop logging...')
    bt_conf = """BtSnoopLogOutput=false
BtSnoopFileName=/sdcard/btsnoop_hci.log
BtSnoopSaveLog=false
TraceConf=true
TRC_BTM=1
TRC_HCI=1
TRC_L2CAP=1
TRC_GATT=1
TRC_BTIF=1
"""
    with open('tools/bt_stack_opt.conf', 'w', encoding='utf-8', newline='\n') as f:
        f.write(bt_conf)
    subprocess.run([adb, '-s', dev, 'push', 'tools/bt_stack_opt.conf', '/system/etc/bluetooth/bt_stack.conf'])
    subprocess.run([adb, '-s', dev, 'shell', 'chmod', '644', '/system/etc/bluetooth/bt_stack.conf'])

    # 4. Start NextGen WebPush TV App
    print('[*] Starting NextGen WebPush TV App...')
    subprocess.run([adb, '-s', dev, 'shell', 'am', 'start', '-n', 'com.nextgen.webpush/.MainActivity'])
    time.sleep(2)

    # 5. Capture Live TV Screen
    print('[*] Capturing live TV screenshot...')
    subprocess.run([adb, '-s', dev, 'shell', 'screencap', '-p', '/sdcard/webpush_tv_live.png'])
    subprocess.run([adb, '-s', dev, 'pull', '/sdcard/webpush_tv_live.png', r'C:\Users\jigu\.gemini\antigravity-ide\brain\59392cea-4993-4618-813e-365af128b445\webpush_tv_live.png'])
    print('[+] Live screen captured successfully!')

if __name__ == '__main__':
    deploy()
