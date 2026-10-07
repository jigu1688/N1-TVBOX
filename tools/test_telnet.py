import subprocess

adb = r"C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe"
dev = "192.168.31.115:5555"

subprocess.run([adb, "connect", dev], check=True)
cmd = """python -c "import socket; s = socket.socket(); s.connect(('127.0.0.1', 2323)); s.sendall(b'id\\n'); print(s.recv(1024).decode())" """
r = subprocess.run([adb, "-s", dev, "shell", "echo 'id' | nc 127.0.0.1 2323 || echo 'id' | busybox nc 127.0.0.1 2323"], capture_output=True, text=True)
print("Telnet output:\n", r.stdout, r.stderr)
