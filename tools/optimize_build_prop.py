import os

def optimize_build_prop(build_prop_path):
    print(f"[*] Optimizing {build_prop_path}...")
    with open(build_prop_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        
    prop_dict = {}
    ordered_keys = []
    
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith('#') and '=' in stripped:
            k, v = stripped.split('=', 1)
            k = k.strip()
            v = v.strip()
            prop_dict[k] = v
            ordered_keys.append(k)
            
    # Apply Optimizations
    # 1. Branding & Build info
    prop_dict['ro.build.display.id'] = 'N1_NextGen_TV_v1.0_2026'
    prop_dict['ro.phicomm.inner.version'] = 'N1_NextGen_TV_v1.0'
    prop_dict['ro.phicomm.outer.version'] = 'N1_NextGen_TV_v1.0'
    
    # 2. GPU 2D/3D Hardware Acceleration
    prop_dict['debug.sf.hw'] = '1'
    prop_dict['debug.egl.hw'] = '1'
    prop_dict['debug.composition.type'] = 'gpu'
    prop_dict['video.accelerate.hw'] = '1'
    prop_dict['ro.hwui.render_dirty_regions'] = 'false'
    prop_dict['ro.hwui.texture_cache_size'] = '72.0f'
    prop_dict['ro.hwui.layer_cache_size'] = '48.0f'
    prop_dict['ro.hwui.r_buffer_cache_size'] = '8.0f'
    prop_dict['ro.hwui.path_cache_size'] = '32.0f'
    prop_dict['ro.hwui.drop_shadow_cache_size'] = '6.0f'
    prop_dict['ro.hwui.gradient_cache_size'] = '1.0f'
    
    # 3. Dalvik / ART Virtual Machine Tuning (for 2GB DDR3 RAM)
    prop_dict['dalvik.vm.heapstartsize'] = '16m'
    prop_dict['dalvik.vm.heapgrowthlimit'] = '192m'
    prop_dict['dalvik.vm.heapsize'] = '384m'
    prop_dict['dalvik.vm.heaptargetutilization'] = '0.75'
    prop_dict['dalvik.vm.heapminfree'] = '2m'
    prop_dict['dalvik.vm.heapmaxfree'] = '8m'
    prop_dict['dalvik.vm.dex2oat-filter'] = 'speed'
    prop_dict['dalvik.vm.image-dex2oat-filter'] = 'speed'
    prop_dict['dalvik.vm.dex2oat-threads'] = '4'
    prop_dict['dalvik.vm.jit.codecachesize'] = '32'
    
    # 4. Gigabit Ethernet & Wi-Fi TCP/IP Stack Expansion
    prop_dict['net.tcp.buffersize.default'] = '262144,524288,1048576,262144,524288,1048576'
    prop_dict['net.tcp.buffersize.wifi'] = '524288,1048576,2097152,262144,524288,1048576'
    prop_dict['net.tcp.buffersize.ethernet'] = '524288,1048576,4194304,262144,524288,2097152'
    
    # 5. Remote & Touch Responsiveness
    prop_dict['touch.pressure.scale'] = '0.001'
    prop_dict['windowsmgr.max_events_per_sec'] = '150'
    prop_dict['ro.min.fling_velocity'] = '8000'
    prop_dict['ro.max.fling_velocity'] = '12000'
    
    # 6. Geek Features: ADB Root, Port 5555, CIBN disabled
    prop_dict['persist.sys.usb.config'] = 'adb'
    prop_dict['service.adb.tcp.port'] = '5555'
    prop_dict['service.phiadb.root'] = '1'
    prop_dict['persist.sys.cibn.auth_disabled'] = '1'
    
    # 7. Disable Debugging Overhead & Telemetry
    prop_dict['ro.config.nocheckin'] = '1'
    prop_dict['logcat.live'] = 'disable'
    prop_dict['profiler.force_disable_err_rpt'] = '1'
    prop_dict['profiler.force_disable_ulog'] = '1'
    
    # Rebuild build.prop
    output_lines = [
        "#",
        "# Phicomm N1 Next-Gen High Performance TV ROM",
        "# Build Date: 2026",
        "# Platform: Amlogic S905D (gxl_p230) - 2GB RAM / 8GB eMMC / Gigabit Ethernet",
        "#",
        ""
    ]
    
    seen = set()
    for k in ordered_keys:
        if k in prop_dict and k not in seen:
            output_lines.append(f"{k}={prop_dict[k]}")
            seen.add(k)
            
    for k, v in prop_dict.items():
        if k not in seen:
            output_lines.append(f"{k}={v}")
            seen.add(k)
            
    with open(build_prop_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(output_lines) + '\n')
        
    print(f"[+] Successfully wrote optimized build.prop ({len(prop_dict)} properties)")

if __name__ == '__main__':
    optimize_build_prop('build_rom/system_root/build.prop')
