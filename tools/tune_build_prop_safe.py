import os

def generate_clean_tuned_build_prop():
    print("[*] Generating safe, ultra-performant build.prop...")
    
    # Start from webpad's base build.prop
    base_bp = 'extracted_webpad/system_root/build.prop'
    with open(base_bp, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    lines = [l.strip() for l in content.splitlines()]
    
    # Keys to replace/ensure
    props = {
        # TV & Setup Wizard Bypass
        'ro.setupwizard.mode': 'DISABLED',
        'ro.setupwizard.require_network': 'none',
        'ro.setupwizard.user_req': '0',
        'ro.config.headless': 'false',
        'persist.sys.cibn.auth_disabled': '1',
        
        # Network ADB & Root
        'persist.sys.usb.config': 'adb',
        'service.adb.tcp.port': '5555',
        'service.phiadb.root': '1',
        
        # GPU / UI Rendering Acceleration (Safe for Mali-450 HWC)
        'debug.sf.hw': '1',
        'debug.egl.hw': '1',
        'video.accelerate.hw': '1',
        'ro.hwui.render_dirty_regions': 'false',
        'ro.hwui.layer_cache_size': '48.0f',
        'ro.hwui.r_buffer_cache_size': '8.0f',
        'ro.hwui.path_cache_size': '32.0f',
        
        # RAM & ART Memory Management (Optimal for 2GB DDR3)
        'dalvik.vm.heapstartsize': '16m',
        'dalvik.vm.heapgrowthlimit': '192m',
        'dalvik.vm.heapsize': '512m',
        'dalvik.vm.heaptargetutilization': '0.75',
        'dalvik.vm.heapminfree': '512k',
        'dalvik.vm.heapmaxfree': '8m',
        
        # Gigabit Ethernet Buffer Optimization
        'net.tcp.buffersize.default': '262144,524288,1048576,262144,524288,1048576',
        'net.tcp.buffersize.wifi': '524288,1048576,2097152,262144,524288,1048576',
        'net.tcp.buffersize.ethernet': '524288,1048576,4194304,262144,524288,2097152',
        
        # Disable Error Reporting & Telemetry
        'ro.config.nocheckin': '1',
        'profiler.force_disable_err_rpt': '1',
        'profiler.force_disable_ulog': '1'
    }
    
    # Remove any existing keys that we are setting
    cleaned_lines = []
    for l in lines:
        if not l or l.startswith('#'):
            cleaned_lines.append(l)
            continue
        k = l.split('=')[0].strip()
        if k not in props:
            # Also filter out bad experimental props
            if k in ['debug.composition.type', 'dalvik.vm.dex2oat-filter', 'dalvik.vm.image-dex2oat-filter', 'dalvik.vm.dex2oat-threads']:
                continue
            cleaned_lines.append(l)
            
    cleaned_lines.append('\n# ========================================')
    cleaned_lines.append('# Ultra Performance & Tuning Configurations')
    cleaned_lines.append('# ========================================')
    for k, v in props.items():
        cleaned_lines.append(f"{k}={v}")
        
    out_bp = 'build_rom/system_root/build.prop'
    with open(out_bp, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(cleaned_lines) + '\n')
        
    print(f"[+] Written tuned build.prop to {out_bp}")

if __name__ == '__main__':
    generate_clean_tuned_build_prop()
