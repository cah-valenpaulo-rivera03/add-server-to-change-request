import calendar

import datetime
from datetime import timedelta

def get_patch_cycle():
    # get current date
    today = datetime.datetime.now()
    month = today.month
    day = today.day
    year = today.year

    patch_tuesday = get_patch_tuesday(month, year)

    if day > patch_tuesday.day:
        patch_cycle = month
        patch_cycle_year = year
    else:
        patch_cycle, patch_cycle_year = get_previous_patch_cycle(month, year)

    month_name = calendar.month_name[patch_cycle]
    return "%s %s" % (month_name, patch_cycle_year)
    
def get_previous_patch_cycle(month, year):
    if month == 1:
        prev_month = 12 
        year -= 1
    else:
        prev_month = month - 1 
    
    return prev_month, year

def get_patch_tuesday(month, year):
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