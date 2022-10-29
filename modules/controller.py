#!/usr/bin/env python
import sys

from config.settings import *

from modules.generatecsv import Linux, Windows
from modules.patchtuesday import get_patch_cycle

class AddServerToChangeRequestController:
    def __init__(self):
        self.os_type = self.get_os_type()
        self.change_request = self.get_change_request()
        self.patch_cycle = get_patch_cycle()

    def ask_question(self, question):
        answer = input(question)
        return answer

    def get_change_request(self):
        question = "Input Change Request: "
        change_request = self.ask_question(question)
        
        # validation
        if change_request.startswith("CHG") and len(change_request) == 10:
            return change_request
        else:
            print("Invalid Change Number.")
            sys.exit(0)

    def get_os_type(self):
        os_type = OS_TYPE
        if os_type == "":
            self.set_os_type()
            os_type = OS_TYPE

        return os_type
            
    def set_os_type(self):
        os_option = [
            "Linux",
            "Windows"
        ]

        question = "OS Type: \n(1) - Linux\n(2) - Windows\nChoose OS: "
        answer = self.ask_question(question)
        
        # validation
        try:
            os_index = int(answer) - 1
        except ValueError:
            print("Not a valid option.")
            sys.exit()

        if os_index < 0:
            print("Not a valid option")
            sys.exit()

        if os_index > 1:
            print("Not a valid option")
            sys.exit()

        os_type = os_option[os_index]
        set_env_variable("OS_TYPE", os_type)

    def run(self):
        if self.os_type == "Linux":
            linux_collector = Linux(self.os_type, self.change_request, self.patch_cycle)
            linux_collector.run()
        elif self.os_type == "Windows":
            windows_collector = Windows(self.os_type, self.change_request, self.patch_cycle)
            windows_collector.run()
        else:
            print("Invalid OS: %s" % self.os_type)
            sys.exit()
        
            
