# Shape Class
from point import Point
from velocity import Velocity
from acceleration import Acceleration

class Shape:
	def __init__(self, x=0, y=0, color=(255,255,255)):
		self.center = Point(x,y)
		self.velocity = Velocity(0,0)
		self.acceleration = Acceleration()

		self.angle_degrees = 0 # orientation (NOT direction)
		# maybe implement static vs dynamic coeff_friction later on
		self.coeff_friction = .5
		
		self.mass = .2 # measured in kg (for now at least)
		self.infinite_mass = False
		# (b,g,r)
		self.color = color


	def draw(self):
		print("Draw needs to be implemented!")

	# def check_collision(self):
	# 	# print("check_collision needs to be implemented!")
	# 	pass

	def on_collision(self):
		# print("on_collision needs to be implemented!")
		pass

	def advance(self):
		self.velocity += self.acceleration
		

	

	
