# 斐讯 N1 NextGen TV OS (v19 现代极客旗舰固件)

[![Platform](https://img.shields.io/badge/Platform-Amlogic%20S905D%2064--bit-blue.svg)](https://github.com)
[![Android Version](https://img.shields.io/badge/Android-7.1.2%20Nougat%20(API%2025)-green.svg)](https://github.com)
[![Version](https://img.shields.io/badge/Release-v19.0-purple.svg)](https://github.com)
[![Community](https://img.shields.io/badge/Author-恩山无线论坛%20%40jigu-orange.svg)](https://www.right.com.cn/)

> **专为斐讯 Phicomm N1 深度定制的次世代智能电视操作系统。**  
> 告别 2018 原厂卡顿与臃肿废弃云盘，重塑现代大屏极简交互、极客科技动效与丝滑流畅体验。

---

## 🌟 核心特色与 v19 重磅升级

### 1. 极简科技地平线开机动效 (Minimalist Horizon Boot Animation)
- **告别历史包袱**：彻底移除原厂管家/NAS云盘动画；
- **20fps 呼吸流光**：24 帧平滑激光地平线呼吸律动，融合 N1 轴测透视机身与晶晨 S905D 架构标识；
- **专属个性烙印**：底部内嵌高清晰 `恩山无线论坛 @jigu • AMLOGIC S905D 64-BIT • NEXTGEN TV OS v19` 签名。

### 2. 全景无界融入式关机菜单 (Seamless Borderless Power Menu)
- **16:9 全画幅深空极光**：摒弃传统局部“椭圆蓝蛋”的局促感，采用全景午夜深蓝流光贯穿屏幕两端；
- **地平线光轨承托**：贯穿式激光光带下移至按钮正下方（y=566），三颗圆形功能球（关机、重启、U盘启动）自然悬浮于光轨之上；
- **半透深空微晶材质**：按钮全面升级为高通透暗夜微晶圆盘，文字通透纯净，焦点切换丝滑融入；
- **原生 10-bit 防断层抖动**：数学微抖动算法杜绝大屏电视面板渐变水波纹。

### 3. 次世代极速无线隔空传送 (NextGen WebPush TV)
- 仅 **100KB** 极致纯净常驻引擎，局域网任意手机、平板、电脑直接扫码或在浏览器输入 `http://<盒子IP>:8888`；
- 支持大文件/APK 无线拖拽直传，支持网页端一键静默自动安装，彻底无需插拔 U 盘。

### 4. 完美睡眠与遥控自愈守护 (Deep Sleep & Remote Healing)
- 独家开发 `do_sleep.sh` 与 `PhiTvSettings` 睡眠闭环链路；
- 按电源键即刻进入超低功耗深层睡眠（关断 HDMI 显示与音视频输出），唤醒后网络与遥控即时满血恢复；
- 解决斐讯原厂遥控器断连、按键失灵等历史顽疾。

### 5. 双版本发行矩阵
- **国内纯净版**：集成极致精简无广告桌面（ATV Launcher Pro）、现代 Google WebView 119 内核、高清文件管理器、状态小组件与必备播放解码套件；
- **国际纯净版**：内嵌完整的 **microG 全套开源 Google 生态**（支持 Google 账号登录、FCM 实时推送通知、Google Play 框架支持），告别耗电发热的原生 GApps。

---

## 📦 固件下载与刷机指南

### 1. 固件镜像下载 (v19)
| 固件版本 | 推荐场景 | 镜像文件名 | 下载链接 |
| :--- | :--- | :--- | :--- |
| **国内纯净版** | 国内日常观影、轻量流畅、极速启动 | `N1_NextGen_TV_v19_Domestic_Release.img` | [Releases / 网盘] |
| **国际纯净版** | 需要 Google 账号登录、YouTube/Netflix/Emby 联动 | `N1_NextGen_TV_v19_Global_Release.img` | [Releases / 网盘] |

### 2. 线刷烧录步骤 (USB_Burning_Tool)
1. 打开晶晨官方线刷工具 `USB_Burning_Tool`；
2. 菜单点击 **文件 -> 导入烧录包**，载入 `N1_NextGen_TV_v19_*.img`；
3. **重要配置项**：
   - 勾选 **擦除 Flash**（通常选择“普通擦除”保留 MAC 地址，如需彻底干净可全擦除）；
   - 取消勾选 **擦除 Bootloader**（避免破坏底层引导）；
4. 点击 **开始**；
5. 双公头 USB 线一端插入电脑，另一端插入 N1 靠近 HDMI 接口的 USB 口；
6. 盒子接通电源，工具将自动识别并开始烧录，进度达 100% 后点击“停止”并断电重启即可。

---

## 🛠️ 本地编译与固件打包

本项目自带完整的自动化打包工具链，可在 Windows 环境下一键生成线刷镜像：

1. **依赖环境**：
   - Windows 10/11 64-bit + Python 3.10+
   - WSL (Windows Subsystem for Linux，内置 `debugfs` 和 `e2fsck`)
   - Android SDK Build-Tools (zipalign / aapt2 / d8 / apksigner)
   - JDK 17+ / Adoptium OpenJDK
2. **一键生成国内纯净版**：
   ```cmd
   一键打包固件.bat
   ```
3. **一键生成国际纯净版**：
   ```cmd
   一键打包固件_国际纯净版.bat
   ```

---

## 🤝 致谢与署名

- **固件定制开发**：恩山无线论坛 `@jigu`
- **基础固件底包**：Amlogic 晶晨原厂驱动 & Webpad 早期修改精粹
- **开源组件**：microG Team, ATV Launcher Community, Apktool, Libsparse

*版权声明：本固件仅供智能盒子爱好者学习交流使用，严禁用于任何商业牟利行为。*
