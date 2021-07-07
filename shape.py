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
		print("Error: draw method not over-ridden!")

	
	def on_collision(self):
		# print("on_collision needs to be implemented!")
		self.color = (255,255,255)

	def on_wall_collision(self, col_type):
		
		if col_type == 'v':
			if abs(self.velocity.dy) <=.1:
				self.velocity.dy = 0
				self.acceleration.ddy = 0 
			else:
				self.velocity.dy *= -.85
		elif col_type == 'h':
			if abs(self.velocity.dx) <= .1:
				self.velocity.dx = 0
				self.acceleration.ddx = 0 
			else:
				self.velocity.dx *= -.85
		else:
			print("ERROR: Invalid collision type (col_type) for on_wall_collision")

	def advance(self):
		self.velocity += self.acceleration
		

	

	
