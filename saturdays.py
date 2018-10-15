# import dependencies
import numpy as np
import datetime

# define a function to generate the closest saturday of our desired date
def getsaturday(date):
    "@date: given date, in format '2013-05-25'"
    d1 = datetime.datetime.strptime(date, '%Y-%m-%d')
    t = datetime.timedelta((7 + 5 - d1.weekday()) % 7) # 5 is saturday
    next_saturday = d1 + t
    return next_saturday

# function to calculate the range for the for loop to generate list
def getdaterange(startdate, lastdate):
    "@startdate & lastdate: given date, in format '2013-05-25'"
    d1 = getsaturday(startdate)
    d2 = datetime.datetime.strptime(lastdate,'%Y-%m-%d')
    date_range = (d2 - d1).days/7
    return int(date_range)+1

def getdatelist(startdate, lastdate):
    "@startdate & lastdate: given date, in format '2013-05-25'"
    "@generate a list of saturday between the date range"
    # Create a list to store all saturdays
    date_list = []
    #date1 = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    #date2 = datetime.datetime.strptime(last_date, '%Y-%m-%d')
    d1 = getsaturday(start_date)
    d2 = getsaturday(last_date)
    n = getdaterange(start_date, last_date)
    aweekago = datetime.timedelta(days=7)
    date_list.append(d2)
    date = d2 # define date as the last saturday of the datelist
    for i in range(n):
        new_date = date - aweekago
        date_list.append(new_date)
        date = new_date
    return date_list