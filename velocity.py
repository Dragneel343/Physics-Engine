class Velocity:
	def __init__(self, dx, dy):
		self.dx = dx
		self.dy = dy

	def __iadd__(self, accel):
		self.dx += accel.ddx
		self.dy += accel.ddy
		return self