#!/usr/bin/env python
# -*- coding: utf-8 -*-

def next_weekday(d, weekday):
    # Returns the next weekday for a datetime
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

def newyear(datetime):
    if datetime.month == 1 and datetime.day < 4:
        return "Happy New "+str(datetime.year)
    else:
        return False

def christmas(datetime):
    if datetime.month == 12 and datetime.day == 24:
        return "Merry Christmas"
    else:
        return False

def erstermai(datetime):
    if datetime.month == 5 and datetime.day == 1:
        return "Protest!"
    else:
        return False

def towelday(datetime):
    if datetime.month == 5 and datetime.day == 25:
        return "Towel Day"
    else:
        return False

def jazzday(datetime):
    if datetime.month == 4 and datetime.day == 30:
        return "Jazz?"
    else:
        return False

def worldmusicday(datetime):
    if datetime.month == 10 and datetime.day == 1:
        return "World Music Day"
    else:
        return False

def beerday(datetime):
    if datetime.month == 8 and (datetime.weekday()==4) == (datetime.day < 7):
        return "Beer"
    else:
        return False

def check_special(datetime):
    """
    Check if any special day is occuring and return special string
    """
    functions = [
    newyear(datetime),
    christmas(datetime),
    erstermai(datetime),
    towelday(datetime),
    jazzday(datetime),
    worldmusicday(datetime),
    beerday(datetime)
    ]
    functions = filter(bool, functions)
    if len(functions) > 0:
        return functions[0]
    else:
        return ""



if __name__ == "__main__":
    from datetime import *
    print check_special(datetime(2018, 8, 3, 18, 00))
