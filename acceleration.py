from globals import GRAVITY

class Acceleration:
	def __init__(self, ddx=0, ddy=0):
		self.ddx = ddx
		self.ddy = ddy
		self.ddy -= GRAVITY
	