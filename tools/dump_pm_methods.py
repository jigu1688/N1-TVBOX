import subprocess

adb = r"C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe"
dev = "192.168.31.115:5555"

subprocess.run([adb, "connect", dev], check=True)
code = """
import java.lang.reflect.Method;
public class DumpPM {
    public static void main(String[] args) throws Exception {
        Class<?> c = Class.forName("android.os.IPowerManager");
        for (Method m : c.getDeclaredMethods()) {
            System.out.println(m.getName() + " -> " + java.util.Arrays.toString(m.getParameterTypes()));
        }
    }
}
"""
with open("tools/DumpPM.java", "w") as f:
    f.write(code)

r = subprocess.run([adb, "-s", dev, "shell", "service list | grep -i power"], capture_output=True, text=True)
print("Power service:\n", r.stdout)
