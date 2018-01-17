#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import *
import pyglet
from primitives_bak import *
from vector import *

textformat = '%H:%M'

pyglet.font.add_directory('fonts/')

try:
    window = pyglet.window.Window(fullscreen=True, caption='Studiouhr')
except NoSuchDisplayException:
    raise Exception("Tried to create a Display, but there is no display connected?! ಠ_ಠ")


def updatetime(value):
    """Updates the time for the textlabel"""
    now = datetime.now()
    label.document.text = now.strftime(textformat)


class Dot():
    """A single Dot in Dots. Only renders when active."""
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
    """A collection of radial dots updating over the course of a minute"""
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
            v = v.rotate((self.n-i-1)*360/float(self.n))
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
            dot.render()


class StillDots(Dots):
    """A collection of radial non-updating dots, for 5 second ticks"""
    def __init__(self, x, y, radius, n=60, dotradius=2, dotstroke=1, dotcolor=(255,255,255,1)):
        Dots.__init__(self, x, y, radius, n, dotradius, dotstroke, dotcolor)
        self.actives = [True]*(self.n+1)

    def update(self, value):
        for i, c in enumerate(self.coordinates):
            self.dots[i] = Dot(c+self.pos, True, self.dotradius, self.dotstroke, self.dotcolor)


class TimeArc():
    """Updating Arc"""
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

# Declaration of Renderobjects
label = pyglet.text.Label('??:??:??:', font_name="DIN Next W1G UltraLight", font_size=window.height//5, x=window.width//2, y=window.height//2, anchor_x='center', anchor_y='center', color=(255,0,0,255))

arc = TimeArc(window.width//2, window.height//2, window.height//2-window.height//20, 1, (255,0,0,0.3))

dotsfive = StillDots(window.width//2, window.height//2, window.height//2-window.height//50, 12, window.height//50, window.height//50, (255,0,0,1))

dots = Dots(window.width//2, window.height//2, window.height//2-window.height//20, 60, window.height//50, window.height//50, (255,0,0,1))


@window.event
def on_draw():
    window.clear()
    updatetime(None)
    dotsfive.update(None)
    dots.update(None)
    arc.update(None)

    arc.render()
    label.draw()
    dots.render()
    dotsfive.render()

pyglet.clock.schedule_interval(updatetime, 0.01)
pyglet.clock.schedule_interval(dots.update, 0.1)
pyglet.clock.schedule_interval(arc.update, 0.02)
pyglet.clock.schedule_interval(dotsfive.update, 0.1)

pyglet.app.run()
