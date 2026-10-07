import android.content.Context;
import android.os.PowerManager;
import android.os.SystemClock;
import android.os.IBinder;
import java.lang.reflect.Method;

public class TestSleep {
    public static void main(String[] args) {
        try {
            System.out.println("[*] Testing PowerManager.goToSleep...");
            Class<?> smClass = Class.forName("android.os.ServiceManager");
            Method getService = smClass.getMethod("getService", String.class);
            IBinder powerBinder = (IBinder) getService.invoke(null, "power");
            
            Class<?> stubClass = Class.forName("android.os.IPowerManager$Stub");
            Method asInterface = stubClass.getMethod("asInterface", IBinder.class);
            Object ipower = asInterface.invoke(null, powerBinder);
            
            long time = SystemClock.uptimeMillis();
            // IPowerManager.goToSleep(long time, int reason, int flags)
            Method goToSleepMethod = ipower.getClass().getMethod("goToSleep", long.class, int.class, int.class);
            goToSleepMethod.invoke(ipower, time, 0, 0);
            System.out.println("[+] goToSleep invoked successfully!");
        } catch (Throwable t) {
            t.printStackTrace();
        }
    }
}
