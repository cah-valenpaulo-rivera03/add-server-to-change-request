import os
import glob
import shutil

from datetime import datetime

def cleanup(change_request):
    # create parent archive folder
    parent_archive_dir = "archive"
    try:
        os.mkdir(parent_archive_dir)
    except FileExistsError:
        pass

    # create change archive folder
    now = datetime.now()
    date_time = now.strftime("%Y%m%dT%H%M%S")
    dir_name = "%s - Archive - %s" % (change_request, date_time)
    try:
        os.mkdir(dir_name)
    except FileExistsError:
        print("Directory already exists.")

    # get all csv files
    csv_files = glob.glob('./' + '*.csv')

    # Archive csv files
    for csv in csv_files:
        shutil.move(csv, dir_name)

    # Archive folder
    shutil.move(dir_name, parent_archive_dir)

    