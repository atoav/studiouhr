#!/usr/bin/env python
# -*- coding: utf-8 -*-
from primitives import *
from vector import *
from specialtext import *
from zeitfarbe import *
from config import *
from datetime import *
import pyglet
import colorsys
import ast
from ConfigParser import ConfigParser
import os.path, sys
from socket import gethostname



def update_time_string(value):
    """
    Updates the text/time for the textlabel
    """
    global label
    now = datetime.now()
    label.document.text = now.strftime(textformat)



def update_special_string(value):
    """
    Updates the text for the textlabel
    """
    global labelspecial
    now = datetime.now()
    labelspecial.document.text = check_special(now)

def formatdelta(s):
    s = s.total_seconds()
    days, dremainder = divmod(s, 86400)
    hours, hremainder = divmod(dremainder, 3600)
    minutes, seconds = divmod(hremainder, 60)

    if days > 0:
        if days == 1:
            daysstring = "One Day"
        else:
            daysstring = str(days)+" Days"
    else:
        daysstring = ""
    if days > 0 and days <= 14:
        string = daysstring+" and "+str(hours)+" Hours"
    elif days > 14:
        string = daysstring
    elif hours > 0:
        if hours == 1:
            string = "One Hour and "+str(minutes)+" Minutes"
        else:
            string = str(hours)+" Hours and "+str(minutes)+" Minutes"
    elif minutes > 0:
        if minutes == 1:
            string = "One Minute and "+str(seconds)+" Seconds"
        else:
            string = str(minutes)+" Minutes and "+str(seconds)+" Seconds"
    elif seconds > 0:
        string = str(seconds)+" Seconds"
    else:
        string = ""
    return string


class Dot():
    """
    A single Dot in Dots.
    """
    def __init__(self, pos, active, radius=2, linewidth=1, color=(255,255,255,1)):
        self.pos = pos
        self.active = active
        self.radius = radius
        self.linewidth = linewidth
        self.color = color

    def update(self):
        pass

    def render(self):
        if self.active:
            circle = Circle(self.pos.x, self.pos.y, 0, self.radius, self.color, self.linewidth, style=GLU_FILL)
            circle.render()




class Dots():
    """
    A collection of radial dots updating over the course of a minute
    """
    def __init__(self, x, y, radius, n=60, dotradius=2, dotstroke=1, dotcolor=(255,255,255,1)):
        self.x, self.y = x, y
        self.pos = Vector(self.x, self.y)
        self.radius = radius
        self.n = n
        self.dotradius = dotradius
        self.dotstroke = dotstroke
        self.dotcolor = dotcolor
        self.coordinates = [self.pos]*(self.n+1)
        self.getcoordinates()
        self.actives = [False]*(self.n+1)
        self.dots = [None]*(self.n+1)

    def getcoordinates(self):
        for i in range(0, self.n):
            v = Vector(0, self.radius)
            v = v.rotate((self.n-i)*360.0/float(self.n))
            self.coordinates[i] = v

    def update(self, value):
        self.getcoordinates()
        for i, c in enumerate(self.coordinates):
            if i<= datetime.now().second:
                self.actives[i] = True
            else:
                self.actives[i] = False
        for i, c in enumerate(self.coordinates):
            if self.actives[i]:
                self.dots[i] = Dot(c+self.pos, True, self.dotradius, self.dotstroke, self.dotcolor)
            else:
                self.dots[i] = Dot(c+self.pos, False)

    def render(self):
        for dot in self.dots:
            if dot.active:
                dot.render()




class StillDots(Dots):
    """
    A collection of radial non-updating dots, for 5 second ticks
    """
    def __init__(self, x, y, radius, n=60, dotradius=2, dotstroke=1, dotcolor=(255,255,255,1)):
        Dots.__init__(self, x, y, radius, n, dotradius, dotstroke, dotcolor)

    def update(self, value):
        for i, c in enumerate(self.coordinates):
            if i < len(self.coordinates)-1:
                self.dots[i] = Dot(c+self.pos, True, self.dotradius, self.dotstroke, self.dotcolor)
            else:
                self.dots[i] = Dot(c+self.pos, False, self.dotradius, self.dotstroke, self.dotcolor)



class TimeArc():
    """
    Updating Arc
    """
    def __init__(self, x, y, radius, linewidth, color):
        self.x = x
        self.y = y
        self.pos = Vector(self.x, self.y)
        self.radius = radius
        self.linewidth = linewidth
        self.color = color
        self.sweep = 0

    def update(self, value):
        now = datetime.now()
        self.sweep = (now.second*0.0166666666666666+now.microsecond/60000000.)*360.

    def render(self):
        arc = Arc(self.pos.x, self.pos.y, 0, self.radius, 0, self.sweep, self.color, self.linewidth, 180.)
        arc.render()


def get_zeitfarbe(value):
    value = timetofloat(datetime.now())
    zeitfarben, lastcolor, nextcolor, blendvalue = zeitfarbe(value, timedict)
    r, g, b = [int(channel) for channel in zeitfarben]
    return r, g, b

def printstats(value):
    global r
    global g
    global b
    global hostname
    global starttime
    now = datetime.now()
    uptime = now-starttime
    os.system('cls' if os.name == 'nt' else 'clear')
    headerstring = "-"*15+" studiouhr.py running @"+str(hostname)+" "+"-"*15
    sys.stdout.write(headerstring+"\n")
    sys.stdout.write("\r"+("Time:").ljust(30)+now.strftime("%H:%M:%S.%f"+"\n"))
    sys.stdout.write("\r"+"FPS:".ljust(30)+str(pyglet.clock.get_fps())+"\n")
    colorstring = "Current Color:".ljust(30)+str((r,g,b))
    sys.stdout.write("\r"+colorstring+"\n")
    sys.stdout.write("Uptime:".ljust(30)+formatdelta(uptime)+"\n")
    sys.stdout.write("-"*len(headerstring))
    sys.stdout.flush()



def main():
    # Get hostname with help of socket
    global hostname
    hostname = gethostname()
    print "------ Studiouhr started on host "+str(hostname)+" ------"

    global starttime
    starttime = datetime.now()

    # Load Configs
    config = Config("settings.ini")

    # Resolves to '%H:%M' on default
    global textformat
    global r
    global g
    global b
    textformat = config.textformat

    # Load Fonts
    fontpath = os.path.join(os.path.dirname(__file__), 'fonts/')
    if os.path.exists(fontpath):
        print "Load fonts from "+str(fontpath)
    else:
        print "Fontfolder "+str(fontpath)+" does not exist"
    pyglet.font.add_directory(fontpath)
    pyglet.font.load(config.fontname)

    # Initialize Window
    window = pyglet.window.Window(fullscreen=config.fullscreen, caption='Studiouhr')
    window.set_mouse_visible(False)

    # Calculate half width and half height
    hw = window.width//2
    hh = window.height//2
    
    # Construct Variables from Config
    fontsize = int(window.height/100.*config.fontsize)
    xoffset = int(hw/1000.*config.xoffset)
    yoffset = int(hh/1000.*config.yoffset)
    dotdiameter = int(hh/1000.*config.dotdiameter)
    secondradius = int(hh-(window.height/1000.)*config.secondmargin)
    indicatorradius = int(hh-(window.height/1000.)*config.indicatormargin)
    r,g,b = get_zeitfarbe(None)

    # Declaration of Renderobjects
    global label
    global labelspecial
    label = pyglet.text.Label('??:??', font_name=config.fontname, font_size=fontsize, x=hw+xoffset, y=hh+yoffset, anchor_x='center', anchor_y='center', color=(r,g,b,255))
    labelspecial = pyglet.text.Label('', font_name=config.fontname, font_size=fontsize//4, x=hw+xoffset, y=hh+hh//3, anchor_x='center', anchor_y='center', color=(r,g,b,255))
    if config.displayarc: arc = TimeArc(hw, hh, secondradius, config.arcwidth, (r,g,b,0.3))
    if config.displayfivemarks: dotsfive = StillDots(hw, hh, indicatorradius, 12, dotdiameter, dotdiameter, (r,g,b,1))
    if config.displayseconddots: dots = Dots(hw, hh, secondradius, 60, dotdiameter, dotdiameter, (r,g,b,1))
    background = Polygon([(0,0), (0, window.width), (window.width, window.height), (window.width, 0)], 0, (0,0,0,1))
    

    # On Draw Function Calls
    @window.event
    def on_draw():
        window.clear()
        update_time_string(None)
        update_special_string(None)

        # Get color from zeitfarbe
        r,g,b = get_zeitfarbe(None)
        label.color = (r,g,b,255)
        labelspecial.color = (r,g,b,255)
        printstats(None)
        # Convert 8bit color to float
        r,g,b = r/255., g/255., b/255.
        dotsfive.dotcolor = (r,g,b,1)
        dots.dotcolor = (r,g,b,1)
        arc.color = (r,g,b,0.3)
        if config.displayfivemarks: dotsfive.update(None)
        if config.displayseconddots: dots.update(None)
        if config.displayarc: arc.update(None)
        background.render()
        if config.displayarc: arc.render()

        
        label.draw()
        labelspecial.draw()

        if config.displayseconddots: dots.render()
        if config.displayfivemarks: dotsfive.render()

    # Schedule Intervals
    pyglet.clock.schedule_interval(update_time_string, config.clockinterval)
    pyglet.clock.schedule_interval(update_special_string, 1000)
    pyglet.clock.schedule_interval(printstats, 25)
    pyglet.clock.schedule_interval(get_zeitfarbe, 0.02)
    if config.displayseconddots: pyglet.clock.schedule_interval(dots.update, config.dotinterval)
    if config.displayarc: pyglet.clock.schedule_interval(arc.update, config.arcinterval)
    if config.displayfivemarks: pyglet.clock.schedule_interval(dotsfive.update, config.indicatorinterval)

    print
    print "Clock is running now."
    pyglet.app.run()



if __name__ == "__main__":
    # Declare some global variables
    r = None
    g = None
    b = None
    hostname = None
    textformat = None
    label = None
    labelspecial = None
    starttime = None
    main()