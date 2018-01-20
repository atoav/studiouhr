import math

"""
A helper class for all sorts of Vector-related calculations
"""
def lerp(start, end, percent):
	return (start + percent*(end - start));

def map(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)
    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

class Vector(object):
	def __init__(self, x=0.0, y=0.0):
		self.x = x
		self.y = y

	def __str__(self):
		return "Vector(%s, %s)"%(self.x, self.y)

	def __repr__(self):
		return "%s(%r)" % (self.__class__, self.__dict__)

	def __add__(self, rhs):
		return Vector(self.x+rhs.x, self.y+rhs.y)

	def __sub__(self, rhs):
		return Vector(self.x-rhs.x, self.y-rhs.y)

	def __neg__(self):
		return Vector(-self.x, -self.y)

	def __mul__(self, scalar):
		return Vector(self.x*scalar, self.y*scalar)

	def __div__(self, scalar):
		return Vector(self.x/scalar, self.y/scalar)

	def __abs__(self):
		return self.mag()


	@classmethod
	def from_points(cls, P1, P2):
		return cls( P2[0]-P1[0], P2[1]-P1[1] )

	def rotate(self, degree):
		mag = self.mag()
		ang = self.get_angle(0.0, 0.0)
		ang += degree
		x,y = self.get_xy(mag, ang)
		return Vector(x,y)

	def dot(self, other):
		dot = (self.x*other.x + self.y*other.y)
		if not (self.mag()*other.mag())==0:
			return dot/(self.mag()*other.mag())
		else:
			return dot

	def mag(self):
		return math.sqrt( self.x**2 + self.y**2 )

	def norm(self):
		magnitude = self.mag()
		self.x /= magnitude
		self.y /= magnitude

	def constrain(self, bottom, top):
		self.x = max(min(self.x, top), bottom)
		self.y = max(min(self.y, top), bottom)

	def get_angle(self, x1, y1):
		# returns the angle of one point to another point
		# where 0 degree is x+
		x2 = self.x
		y2 = self.y
		if (y1 == y2):
			if (x1 < x2): return 0.
			else: return 180.
		elif (x1 == x2):
			if (y1 < y2): return 90.
			else: return 270.

		# compute the degrees in radians, using tan = opp/adj
		# and arctan(tan) to get the actual angle
		rad_tan = (y2 - y1) / (x2 - x1)
		rad_angle = math.atan(rad_tan)

		# now convert the angle to degrees 
		deg_angle = math.degrees(rad_angle)
		# note that deg_angle will be in the range -90 to +90,
		# and we have to convert to a 0-360 degree value based
		# on which quadrant (x2,y2) falls into relative to (x1,y1)               |
		if (x1 < x2):
			if (y1 < y2): return deg_angle
			else: return 360. + deg_angle
		elif (y1 < y2): return 180. + deg_angle
		else: return 180. + deg_angle

	def get_xy(self, length, angle):
		if length == 0:
			return (0,0)

		if angle < 90:
			angle = math.radians(angle)
			xpos = length * math.cos(angle)
			ypos = length * math.sin(angle)
			return (xpos, ypos)
		elif angle < 180:
			angle = math.radians(angle-90)
			xpos = -length * math.sin(angle)
			ypos = length * math.cos(angle)
			return (xpos, ypos)
		elif angle < 270:
			angle = math.radians(angle-180)
			xpos = -length * math.cos(angle)
			ypos = -length * math.sin(angle)
			return (xpos, ypos)
		else:
			angle = math.radians(angle-270)
			xpos = length * math.sin(angle)
			ypos = -length * math.cos(angle)
			return (xpos, ypos)

	def tuple(self):
		return (self.x, self.y)


class Easer():
	def __init__(self, value, goal, easing=0.1):
		self.value = value
		self.goal = goal
		self.easing = easing
		self.delta = self.goal-self.value

	def get(self):
		self.delta = self.goal-self.value
		if abs(self.delta) >0.01:
			self.value += self.delta * self.easing
		return  self.value

	def set(self, goal):
		self.goal = goal



class EaserColor():
	def __init__(self, (value0, value1, value2, value3), (goal0, goal1, goal2, goal3), easing=0.1):
		self.values = [value0, value1, value2, value3]
		self.goals = [goal0, goal1, goal2, goal3]
		self.easing = easing
		self.deltas = [
				self.goals[0]-self.values[0],
				self.goals[1]-self.values[1], 
				self.goals[2]-self.values[2],
				self.goals[3]-self.values[3]
				]

	def get(self):
		self.deltas = [
				self.goals[0]-self.values[0],
				self.goals[1]-self.values[1], 
				self.goals[2]-self.values[2],
				self.goals[3]-self.values[3]
				]
		for i,delta in enumerate(self.deltas):
			#if abs(delta) > 0.1:
			self.values[i] += self.deltas[i]*self.easing
		return self.values[0], self.values[1], self.values[2], self.values[3]

	def set(self, (goal0, goal1, goal2, goal3)):
		self.goals = [goal0, goal1, goal2, goal3]


if __name__ == "__main__":
	ease = EaserColor((255,255,255,255), (0,0,0,0), 0.1)
	import time
	while True:
		time.sleep(0.1)
		print ease.get()
