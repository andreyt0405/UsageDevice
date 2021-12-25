import json
import sys
from uiAutomation import uiAutomation
import argparse as argparse
from adbutils import AdbClient, errors
import re


def remove_log():
    pass


def android_ui_operation():
    release = re.search(r"^([^.]*).*", adb.device(serial=serialno).getprop('ro.build.version.release')).group(1)
    vendor = adb.device(serial=serialno).getprop('ro.product.brand')
    print(f"[Vendor: {vendor} System Operation: {release} Serial:{serialno}]")
    usage_intent = open(r'usage_intent.json')
    data = json.load(usage_intent)
    try:
        google_usage = f"{data['Google_Usage']}" \
                       f"{data[vendor][release]['Google_Usage']}"

        usage_os = f"{data['Operation_Usage']}" \
                   f"{data[vendor][release]['Operation_Usage']}" \
                   f"{data['ReportDiagnostic']}"

    except KeyError as Except:
        print(f"{Except}")
        google_usage, usage_os = "Google_Usage", "Operation_Usage"
        exit(1)

    uiAutomationObject.disable_operation_diagnostic(usage_os)
    uiAutomationObject.disable_google_diagnostic(google_usage)
    remove_log()
    uiAutomationObject.reboot_device()


def wait_for_offline():
    try:
        adb.wait_for(serial=serialno, state='disconnect', timeout=60)
        return True
    except errors.AdbTimeout:
        return False


def wait_for_device():
    try:
        adb.wait_for(serial=serialno, state='device', timeout=60)
        return True
    except errors.AdbTimeout:
        return False


def main():
    """
        parse arguments, validate them
        """
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', required=True,
                        help="file path")

    arguments = parser.parse_args()
    if arguments.path:
        sys.argv = [sys.argv[0]]
        return wait_for_device()


if __name__ == '__main__':
    adb = AdbClient(host="127.0.0.1", port=5037)
    tmp_sys_arg = sys.argv
    for device in adb.device_list():
        sys.argv = tmp_sys_arg
        serialno = device.get_serialno()
        if main():
            uiAutomationObject = uiAutomation(serialno)
            android_ui_operation()
