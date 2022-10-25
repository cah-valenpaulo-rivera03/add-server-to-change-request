import os
import sys

import csv
import glob
import shutil

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
        
                       