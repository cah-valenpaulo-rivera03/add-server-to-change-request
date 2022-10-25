#!/usr/bin/env python
import sys

from modules import configparser
from modules.generatecsv import Linux
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
        os_type = configparser.get_config("os_info", "OS_TYPE")
        if os_type == "":
            os_type = self.set_os_type()
            os_type = configparser.get_config("os_info", "OS_TYPE")

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
        configparser.set_config("os_info", "OS_TYPE", os_type)

    def run(self):
        if self.os_type == "Linux":
            linux_collector = Linux(self.os_type, self.change_request, self.patch_cycle)
            linux_collector.run()
        elif self.os_type == "Windows":
            # Windows class
            pass
        else:
            print("Invalid OS: %s" % self.os_type)
            sys.exit()
        
            
