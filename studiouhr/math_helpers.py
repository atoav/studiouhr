# -*- coding: utf-8 *-*


try:
    import pytweening
    import vector
except ImportError, err:
    print "Yikes! %s Failed to load Module in %s:\n%s\n" % (__name__, __file__, err)
    sys.exit(1)


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


class Easer2D():
	def __init__(self, (value0, value1), (goal0, goal1), (easing0, easing1)):
		self.values = vector.Vector(value0, value1)
		self.goals = vector.Vector(goal0, goal1)
		self.easing = vector.Vector(easing0, easing1)
		self.deltas = self.goals-self.values

	def get(self):
		self.deltas = self.goals-self.values
		if abs(self.deltas.x) >0.1 or abs(self.deltas.y) > 0.1:
			self.values.x += self.deltas.x * self.easing.x
			self.values.y += self.deltas.y * self.easing.y
		return self.values.tuple()

	def set(self, (goal0, goal1)):
		self.goals = vector.Vector(goal0, goal1)


class Easer3D():
	def __init__(self, (value0, value1, value2), (goal0, goal1, goal2), easing=0.1):
		self.values = [value0, value1, value2]
		self.goals = [goal0, goal1, goal2]
		self.easing = easing
		self.deltas = [
				self.goals[0]-self.values[0],
				self.goals[1]-self.values[1], 
				self.goals[2]-self.values[2]
				]

	def get(self):
		self.deltas = [
				self.goals[0]-self.values[0],
				self.goals[1]-self.values[1], 
				self.goals[2]-self.values[2]
				]
		for i,delta in enumerate(self.deltas):
			if abs(delta) > 0.1:
				self.values[i] += self.deltas[i]*self.easing
		return self.values.x, self.values.y

	def set(self, (goal0, goal1, goal2)):
		self.goals = [goal0, goal1, goal1]


class Easer4D():
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
	ease = Easer4D((255,255,255,255), (0,0,0,0), 0.1)
	import time
	while True:
		time.sleep(0.1)
		print ease.get()