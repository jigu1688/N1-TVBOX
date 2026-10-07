# 斐讯 N1 NextGen TV OS - 开发者架构与工程手册

> **文档版本**：v19.0  
> **适用硬件**：斐讯 Phicomm N1 (Amlogic S905D, 2GB RAM, 8GB eMMC)  
> **系统基线**：Android 7.1.2 Nougat (Linux Kernel 3.14.29)  
> **核心维护者**：恩山无线论坛 `@jigu`

---

## 目录
1. [系统总体架构与分区布局](#1-系统总体架构与分区布局)
2. [自动化流水线原理 (Debugfs 注入机制)](#2-自动化流水线原理-debugfs-注入机制)
3. [核心定制模块逆向与优化](#3-核心定制模块逆向与优化)
   - 3.1 开机动画流水线 (bootanimation.zip)
   - 3.2 电视关机菜单无界化 (PhiTvSettings.apk)
   - 3.3 隔空传送服务 (WebPush TV)
   - 3.4 完美睡眠与遥控自愈机制
   - 3.5 国际版 microG 生态集成
4. [SELinux 权限体系与启动信任链](#4-selinux-权限体系与启动信任链)
5. [Git 仓库管理规范与大文件治理](#5-git-仓库管理规范与大文件治理)
6. [一键打包脚本指令集](#6-一键打包脚本指令集)

---

## 1. 系统总体架构与分区布局

斐讯 N1 采用 Amlogic 标准 eMMC 分区布局，线刷包由 `aml_pack.py` 打包为包含分区块与校验表的单镜像文件：

```
N1_NextGen_TV_v19_*.img (Amlogic Upgrade Image)
├── usb_DDR.bin / usb_UBOOT.bin       (USB 阶段引导 Loader)
├── _aml_dtb.PARTITION                (设备树 Device Tree Blob)
├── bootloader.PARTITION              (U-Boot 引导器)
├── boot.PARTITION                    (Linux Kernel 3.14 + Ramdisk)
├── recovery.PARTITION                (TWRP / 官方恢复分区)
├── logo.PARTITION                    (第一阶段芯片 Logo 显存原始帧)
├── system.PARTITION                  (Android 7.1.2 系统分区，Sparse Ext4 格式)
└── data.PARTITION                    (默认预置用户数据分区)
```

---

## 2. 自动化流水线原理 (Debugfs 注入机制)

传统 Android 固件打包通常需要挂载 ext4 分区或对整个系统重压缩，容易丢失特殊的 Linux 文件权限、所有者和 SELinux 扩展属性（xattr）。

本项目采用 **WSL `debugfs` 离线注入 + Inode 级 xattr 修补** 流水线：

```
[extracted_aml/system.raw.img (官方底包镜像)]
                    │
                    ▼
          [build_rom/system.raw.img]
                    │
                    ▼  (wsl debugfs -w -f debugfs_commands)
          [注入定制组件、Smali 修改 APK、配置脚本]
                    │
                    ▼  (tools/patch_selinux.py)
          [自动扫描并修补所有丢失的 SELinux 标签]
                    │
                    ▼  (wsl e2fsck -f -y)
          [文件系统完整性无损校验]
                    │
                    ▼  (python tools/img2simg.py)
          [生成 Android Sparse 紧凑镜像 (system.PARTITION)]
                    │
                    ▼  (python tools/aml_pack.py)
          [写入 AmlCRC 校验码并打包最终线刷 .img]
```

---

## 3. 核心定制模块逆向与优化

### 3.1 开机动画流水线 (`bootanimation.zip`)
- **存储路径**：`/system/media/bootanimation.zip` (权限 `644`, 所有者 `root:root`)
- **生成脚本**：`tools/make_bootanimation.py`
- **技术规范**：
  - 格式：无压缩存储（ZIP_STORED / `store` 模式，Android 底层 `bootanimation` 二进制硬性要求）；
  - `desc.txt` 规范：`1920 1080 20 \n c 0 0 part1`；
  - 视觉设计：24 帧 20fps 极简科技地平线激光呼吸律动，融合 N1 轴测透视机身，底部印制 `恩山无线论坛 @jigu • AMLOGIC S905D 64-BIT • NEXTGEN TV OS v19`。

### 3.2 电视关机菜单无界化 (`PhiTvSettings.apk`)
- **源码工程**：`tools/re_tools/tvsettings_decompiled/`
- **生成脚本**：`tools/make_seamless_shutdown.py`
- **重编译与签名**：`tools/rebuild_tvsettings_ascii.py`
- **关键逆向技术**：
  - `ShutdownActivity` 布局 (`shutdown_layout.xml`) 仅包含三个按键控件（`FrameLayot(arcView)`, `reboot`, `sleep`），中央坐标位于 `x=957, y=471`；
  - 背景画面 `shutdown_bg.jpg` 承担了界面所有的文字排版（“电源选项 / SYSTEM POWER CONTROL”）、发光电源徽标及底部签名；
  - v19 彻底移除了生硬的深色圆角矩形盒子，贯穿全屏的 1700px 变形宽银幕激光移至按钮正下方（`y=566`）作为承托导轨，三颗功能球悬浮其上；
  - 按键未选态 `select_not_bg.png` 升级为半透深空微晶圆盘，选中态 `selected_bg.png` 升级为电光青蓝外发光环。

### 3.3 隔空传送服务 (`WebPush TV`)
- **轻量独立**：纯原生 Java 编写，编译后体积仅约 100KB，无第三方框架依赖；
- **端口常驻**：开机自启 HTTP Daemon 监听 `8888` 端口；
- **功能特性**：支持全平台浏览器拖拽文件/APK 直传，支持 `POST /install` 静默安装。

### 3.4 完美睡眠与遥控自愈机制
- **脚本路径**：`/system/bin/do_sleep.sh` 与 `run_nc.sh`；
- **唤醒链路**：
  - 深度关断 HDMI 信号与显示管线，规避原厂伪睡眠导致的待机发热与漏光；
  - 唤醒时执行网络接口与遥控器键值映射刷新，确保唤醒后局域网 IP、ADB 以及蓝牙遥控器秒级恢复。

### 3.5 国际版 microG 生态集成
- **组件集成**：
  - GmsCore (`com.google.android.gms`) 仿冒官方签名；
  - GsfProxy (`com.google.android.gsf`)；
  - FakeStore 框架；
- **系统层适配**：
  - `/system/etc/security/mac_permissions.xml` 注入签名仿冒特权；
  - `/system/framework/framework-res.apk` 打补丁开启全局签名欺骗开关。

---

## 4. SELinux 权限体系与启动信任链

Android 7.1.2 强制启用了 SELinux 严格策略。在固件注入过程中，新增的二进制和守护进程必须具备对应的 Security Context，否则会被 Kernel 直接 `avc: denied` 拦截：

| 文件路径 | 必需权限 | 必需所有者 | SELinux Security Context | 作用 |
| :--- | :--- | :--- | :--- | :--- |
| `/xbin/su` | `0104755` (SetUID) | `root:shell` | `u:object_r:shell_exec:s0` | Root 执行入口 |
| `/xbin/daemonsu` | `0100755` | `root:shell` | `u:object_r:rootfs:s0` | Root 守护进程 |
| `/xbin/busybox` | `0100755` | `root:shell` | `u:object_r:system_file:s0` | 常用 Linux 工具箱 |
| `/bin/webpad` | `0100755` | `root:shell` | `u:object_r:rootfs:s0` | 初始化启动引导脚本 |
| `/bin/do_sleep.sh` | `0100755` | `root:root` | `u:object_r:system_file:s0` | 睡眠控制链路 |
| `/priv-app/PhiTvSettings/*`| `0100644` | `root:root` | `u:object_r:system_file:s0` | 系统特权级设置应用 |

---

## 5. Git 仓库管理规范与大文件治理

由于 Android ROM 编译体系会产生巨量的二进制固件，**严禁将固件镜像与全分区解包缓存直接提交至 Git 仓库**。

### 5.1 治理原则
1. **源码仓只管代码**：仅追踪 Python 脚本、Smali 逆向源码、定制资源、文档以及打包工具；
2. **大文件走 Release**：打包后的 `N1_NextGen_TV_v19_*.img`（1.35GB ~ 1.41GB）发布至 GitHub Releases 或网盘；
3. **单文件限额**：GitHub 限制单文件严禁超过 100MB。大型第三方独立安装包（如 `open_gapps.zip`、`webview.apk`）建议由构建脚本动态获取或存入网盘。

### 5.2 核心 `.gitignore` 配置要点
```gitignore
# 过滤固件大镜像
*.img
*.7z
*.PARTITION
*.raw.img

# 过滤解包目录与编译缓存
extracted_aml/
extracted_webpad/
verify_output/
build_rom/*.raw.img
build_rom/package/
```

---

## 6. 一键打包脚本指令集

| 脚本文件 | 编码规范 | 输出目标 | 适用版本 |
| :--- | :--- | :--- | :--- |
| `一键打包固件.bat` | **GBK (CP936)** | `N1_NextGen_TV_v19_Domestic_Release.img` | 国内极简纯净版 |
| `一键打包固件_国内纯净版.bat` | **GBK (CP936)** | `N1_NextGen_TV_v19_Domestic_Release.img` | 国内极简纯净版 |
| `一键打包固件_国际纯净版.bat` | **GBK (CP936)** | `N1_NextGen_TV_v19_Global_Release.img` | 国际 microG 纯净版 |

*注：Windows 批处理文件铁律：严禁以 UTF-8 编码保存 `.bat`，必须使用 GBK 编码以避免命令连接符语法崩溃。*
