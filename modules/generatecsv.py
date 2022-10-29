import os
import sys

import csv
import glob
import shutil
import openpyxl

from datetime import datetime

from modules.garbagecollector import cleanup


class Linux:
    def __init__(self, os_type, change_request, patch_cycle):
        self.server_details = []
        self.os_type = os_type
        self.change_request = change_request
        self.patch_list_name = "%s Compliance Patch List" % patch_cycle

    def get_server_data(self):
        csv_files = glob.glob('./' + '*.csv')
        
        # format csv files to get needed details
        for csv_file in csv_files:
            with open(csv_file,"r") as file:
                no_header = file.read().split('\n', 1)[1]
                formatted_file = no_header.split(',1\n')

                for data in formatted_file:
                    details = data.replace('\n', ' ').split(',')
                    
                    if len(details) == 12:
                        self.server_details.append([
                            details[0],
                            self.patch_list_name,
                            "Compliant",
                            self.os_type,
                            details[8],
                            details[9],
                            details[10],
                            details[11],
                            "1",
                            self.change_request
                        ])

    def create_csv_out(self):
        now = datetime.now()
        date_time = now.strftime("%Y%m%dT%H%M%S")
        csv_file_name = '%s - Compliance Report-%s.csv' % (self.change_request, date_time)
        header = [
            "Computer Name",
            "Patch List Name",
            "Compliance Status",
            "OS Type",
            "CAH - Patch Tags",
            "Custom Tags",
            "Operating System",
            "Cloud Provider",
            "Count",
            "Change Number"
        ]

        with open(csv_file_name, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(self.server_details)

        # create output folder
        output_dir = "output"
        try:
            os.mkdir(output_dir)
        except FileExistsError:
            pass

        shutil.move(csv_file_name, output_dir)

    def run(self):
        self.get_server_data()
        cleanup(self.change_request)
        self.create_csv_out()


class Windows:
    def __init__(self, os_type, change_request, patch_cycle):
        self.server_details = []
        self.os_type = os_type
        self.change_request = change_request
        self.patch_list_name = "%s Compliance Patch List" % patch_cycle
        self.compliance_tracker = self.get_compliance_tracker()

    def ask_question(self, question):
        answer = input(question)
        return answer

    def get_compliance_tracker(self):
        # get all xlsx files
        workbooks = glob.glob('./' + '*.xlsx')
        question = "Excel Files:\n"
        for id, workbook in enumerate(workbooks):
            question += "(%s) - %s\n" % (id + 1, workbook)

        question += "\nChoose file: "

        answer = self.ask_question(question)

        try:
            answer = int(answer) - 1
        except ValueError:
            printer("Not a valid option.")
            sys.exit()

        if answer < 0:
            print("Not a valid option")
            sys.exit()

        if answer >= len(workbooks):
            print("Not a valid option")
            sys.exit()

        return workbooks[answer]

    def get_active_workbook(self):
        wb = openpyxl.load_workbook(self.compliance_tracker)

        question = "%s Sheet Names:\n" % (self.compliance_tracker)
        sheetname_id = 1
        for sheetname in wb.sheetnames:
            question += "(%s) - %s\n" % (sheetname_id, sheetname)
            sheetname_id += 1

        question += "\nChoose Sheet Name: "

        answer = self.ask_question(question)

        try:
            answer = int(answer) - 1
        except ValueError:
            printer("Not a valid option.")
            sys.exit()

        if answer < 0:
            print("Not a valid option")
            sys.exit()

        if answer >= len(wb.sheetnames):
            print("Not a valid option")
            sys.exit()

        return wb[wb.sheetnames[answer]]

    def get_server_data(self):
        # get sheetname
        active_workbook = self.get_active_workbook()
        index = 0
        cn_index = None
        cpt_index = None
        ct_index = None
        os_index = None
        cp_index = None
        filter_index = None
        
        for header in active_workbook.iter_cols(min_row=1, max_row=1, values_only=True):
            if header[0] is None:
                continue

            if header[0].lower() == "Computer Name".lower():
                cn_index = index
            elif header[0].lower() == "CAH - Patch Tags".lower():
                cpt_index = index
            elif header[0].lower() == "Custom Tags".lower():
                ct_index = index
            elif header[0].lower() == "Operating System".lower():
                os_index = index
            elif header[0].lower() == "Cloud Provider - CAH".lower():
                cp_index = index
            elif "sensor" in header[0].lower():
                filter_index = index

            index += 1
        
        for details in active_workbook.iter_rows(min_row=2, values_only=True):
            if all(elem is None for elem in details):
                continue

            if details[filter_index].lower() != "compliant":
                continue

            self.server_details.append([
                    details[cn_index],
                    self.patch_list_name,
                    "Compliant",
                    self.os_type,
                    details[cpt_index],
                    details[ct_index],
                    details[os_index],
                    details[cp_index],
                    "1",
                    self.change_request
                ])

    def create_csv_out(self):
        now = datetime.now()
        date_time = now.strftime("%Y%m%dT%H%M%S")
        csv_file_name = '%s - Compliance Report-%s.csv' % (self.change_request, date_time)
        header = [
            "Computer Name",
            "Patch List Name",
            "Compliance Status",
            "OS Type",
            "CAH - Patch Tags",
            "Custom Tags",
            "Operating System",
            "Cloud Provider",
            "Count",
            "Change Number"
        ]

        with open(csv_file_name, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(self.server_details)

        # create output folder
        output_dir = "output"
        try:
            os.mkdir(output_dir)
        except FileExistsError:
            pass

        shutil.move(csv_file_name, output_dir)

    def run(self):
        self.get_server_data()
        self.create_csv_out()
        