from com.dtmilano.android.viewclient import ViewClient
import re
import ast


class BaseActivity:
    def __init__(self, serialno):
        self.__device, self.__serialno = ViewClient.connectToDeviceOrExit(serialno=serialno)
        self.__vc = ViewClient(device=self.__device, serialno=self.__serialno)

    def _start_activity(self, component):
        self.__device.startActivity(component=component)

    def _start_root_activity(self, component):
        self.__device.shell(f"data/local/tmp/cs -c {component} '1000'")

    def _find_by_text(self, text):
        self.__vc.dump()
        return self.__vc.findViewWithText(text)

    def _pressHome(self):
        self.__device.shell("input keyevent KEYCODE_HOME")

    def _touch(self, element):
        if element:
            element.touch()

    def _unlock_device(self,pincode):
        self.__device.unlock()
        lockScreenRE = re.compile('(isStatusBarKeyguard=(true|false)|isKeyguardShowing=(true|false))')
        self.__device.wake()
        self.__vc.swipe(300, 1000, 300, 300)
        self.__vc.sleep(1)
        isKeyguardShowing = self.__device.shell("dumpsys window | grep mStatusBar")
        statusBarKeyguard = lockScreenRE.search(isKeyguardShowing).group(0)
        x = re.search("true|false", lockScreenRE.search(isKeyguardShowing).group(0)).group(0)
        if ast.literal_eval(str(x).capitalize()):
            self.__device.shell(f"input text {pincode}")
            self.touch(self.find_by_text("OK"))
        else:
            print(f"[{statusBarKeyguard}]")

    def _reboot_device(self):
        self.__device.shell('reboot')
