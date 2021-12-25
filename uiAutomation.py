from BaseActivity import BaseActivity


class uiAutomation(BaseActivity):
    def __init__(self, serialno):
        super().__init__(serialno)

    def disable_operation_diagnostic(self, component):
        print(f"[{'State Disable Usage & Diagnostics'}]")
        self.unlock_device()
        self.start_activity(component)
        send_usage = self.find_by_text("I agree to send diagnostic data.(optional)")
        if send_usage['checked'] == 'true':
            self.touch(send_usage)
            print(f"[{'Disabled Usage & Diagnostics'}]")
        else:
            print(f"[{'Usage & Diagnostics is already Off'}]")
        self.touch(self.find_by_text("OK"))

    def disable_google_diagnostic(self, component):
        print(f"[{'State Disable Google Diagnostics'}]")
        self.unlock_device()
        self.start_root_activity(component)
        google_usage = self.find_by_text("On")
        if google_usage:
            print(f"[{'Disabled Google Diagnostics'}]")
            self.touch(google_usage)
        else:
            print(f"[{'Google Diagnostics is already Off'}]")
        self.pressHome()

    def reset_device(self):
        print(f"[{'Rebooting device..'}]")
        self.reboot_device()


