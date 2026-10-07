import subprocess
import sys

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.115:5555'

def run(cmd_args, timeout=10):
    subprocess.run([adb, 'connect', dev], capture_output=True, text=True)
    full_cmd = [adb, '-s', dev] + cmd_args
    r = subprocess.run(full_cmd, capture_output=True, text=True, timeout=timeout)
    return r.stdout, r.stderr

if __name__ == '__main__':
    if len(sys.argv) > 1:
        cmd = " ".join(sys.argv[1:])
        out, err = run(['shell', cmd])
        print("OUT:", out)
        if err:
            print("ERR:", err)
