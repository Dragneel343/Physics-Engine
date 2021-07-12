# Shape Class
from point import Point
from velocity import Velocity
from acceleration import Acceleration
import random
from globals import IDs

class Shape:
	def __init__(self, x=0, y=0, color=(255,255,255), mass=None):
		self.center = Point(x,y)
		self.velocity = Velocity(0,0)
		self.acceleration = Acceleration()
		self.set_id()
		self.has_collided = False


		self.angle_degrees = 0 # orientation (NOT direction)
		# maybe implement static vs dynamic coeff_friction later on
		self.coeff_friction = .5
		
		self._mass = mass # measured in kg (for now at least)
		self.infinite_mass = False
		# (b,g,r)
		self.color = color

	def set_id(self):
		id = 100
		while id in IDs:
			id = random.randint(100,999)
			
		self.id = id
		IDs.add(id)

	def draw(self):
		print("Error: draw method not over-ridden!")

	
	def on_collision(self):
		# print("on_collision needs to be implemented!")
		if self.color == (255,255,255):
			self.color = (200,100,100)
		else:
			self.color = (255,255,255)

	def on_wall_collision(self, col_type, wall):
		if self.center.y >= wall.height:
			self.center.y -= self.velocity.dy
		if col_type == 'v':
			# prevent rolling objects from sinking into floor
			if abs(self.velocity.dy) <=.25:
				self.velocity.dy = 0
				# self.acceleration.ddy = 0 
			else:
				self.velocity.dy *= -.9
		elif col_type == 'h':
			if abs(self.velocity.dx) <= .25:
				self.velocity.dx = 0
				# self.acceleration.ddx = 0 
			else:
				self.velocity.dx *= -.9
		else:
			print("ERROR: Invalid collision type (col_type) for on_wall_collision")

	def advance(self):
		self.has_collided = False
		self.velocity += self.acceleration
	

	
