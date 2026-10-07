import os

bat_path = '一键打包固件_谷歌国际版.bat'
bat_content = """@echo off
chcp 936 >nul
title 斐讯 N1 NextGen TV - 一键打包谷歌国际版 (GMS)

echo ========================================================
echo   斐讯 N1 NextGen TV 谷歌国际版固件打包工具 (v19.4)
echo   内置完整 GMS / Google Play 商店 / YouTube / 独立签名驱动
echo ========================================================
echo.

python tools\\build_v19_gms.py

echo.
echo ========================================================
echo   打包流程执行完毕！
echo   目标镜像: N1_NextGen_TV_v19.4_GMS_Global_Flawless.img
echo ========================================================
pause
"""

with open(bat_path, 'wb') as f:
    f.write(bat_content.encode('gbk'))

print("[+] Updated 一键打包固件_谷歌国际版.bat in GBK encoding!")
