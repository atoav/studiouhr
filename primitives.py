#!/usr/bin/env python
"""
Implementing 2D drawing primitives using
pyglet.gl
copyright 2007 by Flavio Codeco Coelho
"""

from __future__ import division, print_function, unicode_literals

from pyglet import font
from pyglet import clock
from pyglet import window
from pyglet import image
from pyglet.gl import *
from pyglet.window import mouse
from pyglet.window import event
from pyglet.window import key
import vector
import math


""" TODO
    [ ] Implement Rect for all Primitives
    [ ] Implement a clever Collisionmodel
    [ ] Verify if FastCircle is indeed faster than Circle
    [ ] Implement Fill for FastCircle
    [ ] Implement:
        ( ) Rect
        ( ) Bezier
        ( ) Spline
        ( ) Arc
        ( ) Pie
        ( ) Ring Segment (could be Arc with Contour mode?)
        ( ) Triangle
        ( ) Rounded Rectangle (Per Vertex Rounding)
        ( ) Polygon
        ( ) Rounded Polygon (Per Vertex Rounding)
        ( ) Plot

"""



class Base(object):
    """
    Basic attributes of all drawing primitives
    """
    def __init__(self, x, y, z=0, color=(1.0,1.0,1.0,1.0), stroke=0, rotation=0):
        self.visible = 1
        self.z = z
        self.rotation = rotation
        self.stroke = stroke
        self.color = color
        self.q = gluNewQuadric()
        self.pos = vector.Vector(x, y)



class Point(Base):
    """ A Point at a given x,y,z position and color.
        Point(x=123, y=10, z=90, color=(1, 0.5, 0 ,0.54))
    """
    def render(self):
        """
            Draws a pixel at a given x and y with given color .
            Color = 3 or 4 arg tuple. RGB values from 0 to 1 being 1 max value (1, 1, 1) would be white
        """
        glColor4f(*self.color)
        glPushMatrix()
        glTranslatef(self.pos.x, self.pos.y, -self.z)
        # Draw Point
        glBegin(GL_POINTS)
        glVertex3f(0.0, 0.0, 0.0)
        glEnd()
        glPopMatrix()

    def intersects(self, x,y):
        if x==self.pos.x and y==self.pos.y: 
            return True



class Circle(Base):
    """ Circle class
        Circle(x=20, y=100, z=1, width=300, color=(1,1,0,0.3), stroke=5, rotation=0, style=GLU_FILL)
        style choices are : GLU_LINE, GLU_FILL, GLU_SILHOUETTE, GLU_POINT
    """
    def __init__(self, x=10, y=10, z=0, radius=2, color=(0,0,0,1), stroke=0, rotation=0.0, style=GLU_FILL):
        self.radius = radius
        self.style = style
        self.circleresolution = 100
        Base.__init__(self, x, y, z, color, stroke, rotation)
     
    def render(self):
        """ Draw Circle
            x, y, z, width in pixel, rotation, color and line width in px
            style choices are : GLU_LINE, GLU_FILL, GLU_SILHOUETTE, GLU_POINT
            TO DO : textured circles
        """
        
        glColor4f(*self.color)
        glPushMatrix()

        glTranslatef(self.pos.x, self.pos.y, -self.z)
        glRotatef(self.rotation, 0, 0, 0.1)

        if self.radius < 1: 
            self.radius = 1

        if self.stroke:
            # outline width
            inner = self.radius - self.stroke
            if inner < 0: inner=0
        else:
            # filled
            inner = 0 
        
        gluQuadricDrawStyle(self.q, self.style)

        # gluDisk(quad, inner, outer, slices, loops)
        gluDisk(self.q, inner, self.radius, self.circleresolution, 1) 
            
        glPopMatrix()

    def collide(self, other):
        # Collision dependend on what Circle collides with
        if isinstance(other, Point):
            xcollide = (other.pos.x > self.pos.x-self.radius) and (other.pos.x < self.pos.x+self.radius)
            ycollide = (other.pos.y > self.pos.y-self.radius) and (other.pos.y < self.pos.y+self.radius)
            return xcollide and ycollide
        elif isinstance(other, Line):
            pass
        elif isinstance(other, Circle):
            pass


class Line():
    """
        Line class
    """
    def __init__(self, startx, starty, endx, endy, color=(1,1,1,1), stroke=1):
        self.start = vector.Vector(startx, starty)
        self.end = vector.Vector(endx, endy)
        self.color = color
        self.stroke = stroke

    def render(self):
        glColor4f(*self.color)
        color  = (GLfloat *4)(*self.color)
        if self.stroke <= 0:
            self.stroke = 1
        glLineWidth(self.stroke)

        glBegin(GL_LINES)
        # glVertex2i would be integer function
        glVertex2f(self.start.x, self.start.y)
        glVertex2f(self.end.x, self.end.y)
        glEnd()

    def get_angle(self):
        return self.start.get_angle(self.end.x, self.end.y)

class LineArrow(Line):
    def __init__(self, startx, starty, endx, endy, color=(1,1,1,1), stroke=1, startarrow=-1, endarrow=0):
        self.startarrow = startarrow
        self.endarrow = endarrow
        self.scale = 1.0

        Line.__init__(self, startx, starty, endx, endy, color, stroke)
        self.line = Line(self.start.x, self.start.y, self.end.x, self.end.y, self.color, self.stroke)
        self.arrows = []
        self.setup_arrows()

    def setup_arrows(self):
        if self.startarrow != -1:
            if self.startarrow >= 0:
                rot = self.get_angle()-180
                self.arrows.append(ArrowHead(self.start.x, self.start.y, rot, self.scale, self.color, self.stroke, self.startarrow))
        if self.endarrow != -1:
            if self.endarrow >= 0:
                rot = self.get_angle()
                self.arrows.append(ArrowHead(self.end.x, self.end.y, rot, self.scale, self.color, self.stroke, self.endarrow))

    def render(self):
        self.line.render()
        for arrow in self.arrows:
            arrow.render()


class ArrowHead():
    def __init__(self, x, y, rot, scale=1.0, color=(1,1,1,1), stroke=1, arrowtype=0):
        self.pos = vector.Vector(x,y)
        self.rot = rot
        self.scale = scale
        self.color = color
        self.stroke = stroke
        self.arrowtype = arrowtype
        self.arrowelements = []
        if arrowtype == 0:
            self.arrowelements.append(Line(0, 0, 8, -4, self.color, self.stroke))
            self.arrowelements.append(Line(0, 0, 8, 4, self.color, self.stroke))
        if arrowtype == 1:
            self.arrowelements.append(Line(0, 0, 8, -8, self.color, self.stroke))
            self.arrowelements.append(Line(0, 0, 8, 8, self.color, self.stroke))

    def render(self):
        glPushMatrix()
        glTranslatef(self.pos.x, self.pos.y, 0) # translate to GL loc ppint
        glRotatef(self.rot, 0, 0, 1.0)

        for arrowelement in self.arrowelements:
            arrowelement.render()
        glPopMatrix()


class FastCircle():
    """ FastCircle
        A port from C++ Code from
        http://slabode.exofire.net/circle_draw.shtml
    """
    def __init__(self, cx, cy, radius, circleresolution=60, color=(1,1,1,1), stroke=1):
        self.cx = cx
        self.cy = cy
        self.radius = radius
        self.circleresolution = circleresolution
        self.color = color
        self.stroke = stroke
        self.theta = 2 * 3.1415926 / float(self.circleresolution); 
        self.tangential_factor = math.tan(self.theta) # calculate the tangential factor 

        self.radial_factor = math.cos(self.theta) #calculate the radial factor 
    
    def render(self):
        x = self.radius
        y = 0.0

        glColor4f(*self.color)
        color  = (GLfloat *4)(*self.color)
        if self.stroke <= 0:
            self.stroke = 1
        glLineWidth(self.stroke)

        
        glBegin(GL_LINE_LOOP)
        for ii in range(0, self.circleresolution): 
            glVertex2f(x + self.cx, y + self.cy) # output vertex 
            
            # calculate the tangential vector 
            # remember, the radial vector is (x, y) 
            # to get the tangential vector we flip those coordinates and negate one of them 

            tx = -y
            ty = x; 
            
            # add the tangential vector 

            x += tx * self.tangential_factor
            y += ty * self.tangential_factor
            
            # correct using the radial factor 

            x *= self.radial_factor
            y *= self.radial_factor
        glEnd();


# TODO: Move to Plot Subfile, Create Inheritage, Scales and so on
# Create Datapoint Class which does stuff on hover
# Create Histogram Class and FFT shit
class XYPlot2D():
    def __init__(self, x, y, width=400, height=200, datapoints=[], datamin=0.0, datamax=1.0):
        self.pos = vector.Vector(x,y)
        self.width = width
        self.height = height
        self.datamin = datamin
        self.datamax = datamax
        self.datapoints = datapoints
        self.drawpoints = []
        for point in self.datapoints:
            px = self.pos.x + vector.map(point[0], self.datamin, self.datamax, 0, self.width)
            py = self.pos.y + vector.map(point[1], self.datamin, self.datamax, 0, self.height)
            self.drawpoints.append(Point(px, py))
        self.leftaxis = LineArrow(self.pos.x, self.pos.y-10, self.pos.x, self.pos.y+height, endarrow=0)
        self.bottomaxis = LineArrow(self.pos.x-10, self.pos.y, self.pos.x+width, self.pos.y, endarrow=0)

    def render(self):
        self.leftaxis.render()
        self.bottomaxis.render()
        for point in self.drawpoints:
            point.render()



def getSmoothConfig():
        """
        Sets up a configuration that allows of smoothing\antialiasing.
        The return of this is passed to the config parameter of the created window.
        """
        try:
            # Try and create a window config with multisampling (antialiasing)
            config = Config(sample_buffers=1, samples=4, depth_size=16, double_buffer=True)
        except pyglet.window.NoSuchConfigException:
            print ("Smooth contex could not be aquiried.")
            config = None
        return config

smoothconfig = getSmoothConfig()

if __name__=="__main__":
    import random
    win = window.Window(fullscreen=True, caption='Primitives Test!', config=smoothconfig)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    win.set_mouse_visible(False)
    
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    circle = Circle(150, 150, radius=20, stroke=1, color=(1,1,1,1))
    circles = []
    circles.append(FastCircle(-100, 0, 10, 60, color=(random.random(),random.random(),random.random(),1)))
    circle2 = FastCircle(500, 500, 200, 60)
    randdata = []
    for i in range(0, 400):
        randdata.append((random.gauss(0.5,0.1),random.gauss(0.5,0.1)))
    plot = XYPlot2D(600, 200, datapoints=randdata)

    arrow = LineArrow(400,200, 200, 700, color=(1,1,1,0.1), stroke=1, startarrow=1, endarrow=0)
    line = Line(0,0,win.width, win.height, color=(1,1,1,1), stroke=1)

    @win.event
    def on_mouse_motion(x,y,dx,dy):
        if (circle.collide(Point(x,y))):
            circle.style = GLU_FILL
            circle.stroke = 0
        else:
            circle.style = GLU_SILHOUETTE
            circle.stroke = 1

    @win.event
    def on_mouse_press(x, y, button, modifiers):
        #circles.append(FastCircle(x,y, 50, 60, (random.random(),random.random(),random.random(), 1)))
        circles.append(FastCircle(x,y, 50, 60, (1,1,1, 0.5)))

    @win.event
    def on_mouse_drag(x, y, dx, dy, button, modifiers):
        #circles.append(FastCircle(x,y, 50, 60, (random.random(),random.random(),random.random(), 1)))
        circles.append(FastCircle(x,y, 100*random.gauss(0.5,0.3), 60, (1,1,1, 0.5)))

    while not win.has_exit:
        win.dispatch_events()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # circle.render()
        # line.end.y-=1.1
        # circle2.render()
        for i, c in enumerate(circles):
            if c.radius <1.0:
                del(circles[i])
            c.radius *= 0.995
            c.render()

        # plot.render()
        # line.render()
        # arrow.render()
        win.flip()

