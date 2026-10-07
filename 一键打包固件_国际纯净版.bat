@echo off
chcp 936 >nul
title 斐讯 N1 NextGen TV - 一键打包固件 (v19 国际版)

echo ========================================================
echo   斐讯 N1 NextGen TV 旗舰固件 (v19 国际纯净版)
echo   [极简科技开机动效 + 全景无界关机菜单 + microG/Google生态]
echo ========================================================
echo.

python tools/build_v18_6_global.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [!] 固件打包失败，请检查上方日志！
    pause
    exit /b 1
)

echo.
echo ========================================================
echo [成功] 固件打包完成！目标文件: N1_NextGen_TV_v19_Global_Release.img
echo ========================================================
pause
