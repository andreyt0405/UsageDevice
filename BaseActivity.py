from com.dtmilano.android.viewclient import ViewClient
from adbutils import AdbClient, errors
import re
import ast


class BaseActivity:
    def __init__(self, serialno, adb):
        self.__adb = adb
        self.__serialno = serialno
        self.init_device()
        self.__device, self.__serialno = ViewClient.connectToDeviceOrExit(serialno=self.__serialno)
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

    def init_device(self, pincode='1111'):
        self.__adb.device(serial=self.__serialno).shell('input keyevent POWER')
        self.__adb.device(serial=self.__serialno).shell('input touchscreen swipe 300 1000 300 300')
        isKeyguardShowing = self.__adb.device(serial=self.__serialno).shell("dumpsys window | grep mStatusBar")
        lockScreenRE = re.compile('(isStatusBarKeyguard=(true|false)|isKeyguardShowing=(true|false))')
        statusBarKeyguard = lockScreenRE.search(isKeyguardShowing).group(0)
        x = re.search("true|false", lockScreenRE.search(isKeyguardShowing).group(0)).group(0)
        if ast.literal_eval(str(x).capitalize()):
            self.__adb.device(serial=self.__serialno).shell(f"input text {pincode}")
            self.__adb.device(serial=self.__serialno).shell('input keyevent 66')
        else:
            print(f"[{statusBarKeyguard}]")

    def _reboot_device(self):
        self.__device.shell('reboot')
