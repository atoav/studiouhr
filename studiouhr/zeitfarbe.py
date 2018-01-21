#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import *
import colorsys

# Timedict for Debugging
timedict = {
            "06:00":(12,151,250),
            "06:30":(251,13,52),
            "12:00":(247,37,21),
            "23:30":(251,13,52),
            "00:30":(12,151,250)
        }


def timetofloat(datetimeobject, totalturn=24, minimum=0.0, maximum=1.0):
    """
    Function that returns a float between minimum
    and maximum for a moment within totalturn hours.
    """
    micro = datetimeobject.microsecond / 1000000.
    sec = datetimeobject.second
    minutes = datetimeobject.minute * 60
    hours = datetimeobject.hour%totalturn * 60 * 60
    currentsecond = hours + minutes + sec + micro
    return minimum + currentsecond/86400. * float(maximum)


def timedicttorange(timedict, minimum=0.0, maximum=1.0, pattern='%H:%M'):
    """
    Converts a dict with time indices from "00:00" to "24:00"
    to a dict with a range based index between minimum and maximum
    """
    minimum = float(minimum)
    maximum = float(maximum)
    # Create a new dict and parse each key and convert to float
    # E.g. "00:00" is 0.0, "12:00" is 0.5 and "24:00" is 1.0
    newdict = {}
    for key in timedict.keys():
        time = datetime.strptime(key, pattern)
        newkey = timetofloat(time, 24, minimum, maximum)
        newdict[newkey] = timedict[key]
    # Check if minimum or maximum exist as key value, if not
    # set to a interpolated inbetween value
    if not minimum in newdict or maximum in newdict:
        maxkey = max(newdict)
        minkey = min(newdict)
        distance = maxkey - minkey
        interpolatedvalue = lerp3d(distance, newdict[minkey], newdict[maxkey], minimum, maximum)
        newdict[minimum] = interpolatedvalue
        newdict[maximum] = interpolatedvalue
    if not minimum in newdict:
        newdict[minimum] = newdict[maximum]
    if not maximum in newdict:
        newdict[maximum] = newdict[minimum]
    return newdict



def mapvalue(value, leftMin, leftMax, rightMin=0.0, rightMax=1.0):
    """
    map a value between two ranges
    """
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)
    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)



def lerp(value, start_point, end_point, minimum=0.0, maximum=1.0):
    """
    Linear Interpolation between two points
    """
    value = float(value)
    start_point = float(start_point)
    endpoint = float(end_point)
    return minimum+((1.0-value) * start_point +value * end_point)*maximum



def lerp3d(value, (s1, s2, s3), (e1, e2, e3), minimum=0.0, maximum=1.0):
    """
    3D Linear Interpolation
    """

    r1 = lerp(value, s1, e1, minimum, maximum)
    r2 = lerp(value, s2, e2, minimum, maximum)
    r3 = lerp(value, s3, e3, minimum, maximum)

    return (r1, r2, r3)



def tableinterpolate(floatdict, value, minimum=0.0, maximum=1.0):
    """
    Select two table values based on a value and interpolate between them 
    """
    # Clip value if it overflows
    if value > maximum: value = maximum
    if value < minimum: value = minimum
    floatkeys = sorted(floatdict)
    # Find out positive and negative distances for each key
    posdistances = {}
    negdistances = {}
    for i, key in enumerate(floatkeys):
        posdistance = value-key
        negdistance = key-value
        # Discard negative distances
        if not posdistance < 0:
            posdistances[key] = posdistance
        if not negdistance < 0:
            negdistances[key] = negdistance
    # Find the float keys with the two closest values (up and down)
    closestkeydown = min(posdistances, key=posdistances.get)
    closestkeyup = min(negdistances, key=negdistances.get)
    # Only interpolate if we are not directly on a value
    if not closestkeyup == closestkeydown:
        # Return a value btw. 0.0 and 1.0 representing the distance
        inbetweenvalue = mapvalue(value, closestkeydown, closestkeyup, 0.0, 1.0)
        # Interpolate between the two closest values
        output = lerp3d(inbetweenvalue, floatdict[closestkeydown], floatdict[closestkeyup])
        blendvalue = inbetweenvalue
    else:
        output = floatdict[closestkeyup]
        blendvalue = 1.0
    # Return interpolated  last value, next value and blendvalue
    return output[0], output[1], output[2], closestkeydown, closestkeyup, blendvalue



def hsv_to_rgb(h, s, v):
    if s == 0.0: v*=255; return (v, v, v)
    i = int(h*6.) # XXX assume int() truncates!
    f = (h*6.)-i; p,q,t = int(255*(v*(1.-s))), int(255*(v*(1.-s*f))), int(255*(v*(1.-s*(1.-f)))); v*=255; i%=6
    if i == 0: return (v, t, p)
    if i == 1: return (q, v, p)
    if i == 2: return (p, v, t)
    if i == 3: return (p, q, v)
    if i == 4: return (t, p, v)
    if i == 5: return (v, p, q)



def zeitfarbe(value, timedict, minimum=0.0, maximum=1.0):
    """
    Returns a list of 3 color values for a
    value between 0.0 and 1.0, HSV interpolation
    """
    # Create a dict with float keys (0.0 to 1.0) from time based dict
    timedict = timedicttorange(timedict, minimum, maximum)
    # Convert all RGB values in dict to HSV color space for more
    # natural color interpolation
    hsvtable = {}
    for key in timedict.keys():
        r, g, b = timedict[key]
        hsvtable[key] = colorsys.rgb_to_hsv(r/255., g/255., b/255.)
    # Get the interpolated HSV value
    h, s, v, lastkey, nextkey, blendvalue = tableinterpolate(hsvtable, value)
    # Covnert it back to RGB for convinience
    r, g, b = [x*255 for x in colorsys.hsv_to_rgb(h, s, v)]
    return (r, g, b), timedict[lastkey], timedict[nextkey], blendvalue

if __name__ == "__main__":
    import colorsys
    from datetime import *
    now = datetime.now()
    value = timetofloat(now)
    zeitfarben, lastcolor, nextcolor, blendvalue = zeitfarbe(value, timedict)
    r, g, b = [channel for channel in zeitfarben]
    print r, g, b