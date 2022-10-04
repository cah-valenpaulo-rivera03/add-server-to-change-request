#!/usr/bin/env python

import os
import sys

import csv
import glob
import shutil
import calendar

import datetime
from datetime import timedelta


class AddServerToChangeRequest:
    
    def __init__(self):
        self.server_details = []
        os_option = ['Linux', 'Windows']
        os_question = "OS Type: \n(1) - Linux\n(2) - Windows\nChoose OS: "
        # get_os_type_answer = self.ask_os_type(os_question)
        # self.os_type = os_option[get_os_type_answer]
        self.change_request = self.ask_change_request("Input Change Request: ")
        self.patch_cycle = "%s Compliance Patch List" % self.get_patch_cycle()

    def ask_question(self, question):
        answer = input(question)
        return answer

    def ask_change_request(self, question):
        change_request = self.ask_question(question)
        
        # validation
        if change_request.startswith("CHG") and len(change_request) == 10:
            return change_request
        else:
            print("Invalid Change Number.")
            sys.exit(0)

    def ask_os_type(self, question):
        os_type = self.ask_question(question)
        
        # validation
        try:
            answer = int(os_type) - 1
        except ValueError:
            print("Not a valid option.")
            sys.exit()

        if answer < 0:
            print("Not a valid option")
            sys.exit()

        if answer > 1:
            print("Not a valid option")
            sys.exit()

        return answer

    def get_patch_cycle(self):
        # get current date
        today = datetime.datetime.now()
        month = today.month
        day = today.day
        year = today.year

        patch_tuesday = self.get_patch_tuesday(month, year)

        if day > patch_tuesday.day:
            patch_cycle = month
            patch_cycle_year = year
        else:
            patch_cycle, patch_cycle_year = self.get_previous_patch_cycle(month, year)

        month_name = calendar.month_name[patch_cycle]
        return "%s %s" % (month_name, patch_cycle_year)
        
    def get_previous_patch_cycle(self, month, year):
        if month == 1:
            prev_month = 12 
            year -= 1
        else:
            prev_month = month - 1 
        
        return prev_month, year
    
    def get_patch_tuesday(self, month, year):
        # set basedate to the 12th day of the month
        # 12th day of the month always falls on 2nd week 
        basedate = datetime.datetime.strptime(
            '{} 12 {} 12:00AM'.format(month, year),
            '%m %d %Y %I:%M%p'
        )

        dayoftheweek = basedate.weekday() + 1

        if dayoftheweek > 6:
            dayoftheweek = 0

        return basedate - timedelta(days=dayoftheweek) + timedelta(days=2)

    def get_server_data(self):
        csv_files = glob.glob('./' + '*.csv')
        # patch_list_name = 
        
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
                            self.patch_cycle,
                            "Compliant",
                            "Linux",
                            details[8],
                            details[9],
                            details[10],
                            details[11],
                            "1",
                            self.change_request
                        ])

    def create_csv_out(self):
        csv_file_name = '%s - Compliance Report.csv' % self.change_request
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

    def cleanup(self):
        # create archive folder
        dir_name = "%s - Archive" % self.change_request
        try:
            os.mkdir(dir_name)
        except FileExistsError:
            print("Directory already exists.")

        # get all csv files
        csv_files = glob.glob('./' + '*.csv')

        # Archive csv files
        for csv in csv_files:
            shutil.move(csv, dir_name)
    
    def run(self):
        self.get_server_data()
        self.cleanup()
        self.create_csv_out()
        
                       
if __name__ == "__main__":
    cls = AddServerToChangeRequest()
    cls.run()
