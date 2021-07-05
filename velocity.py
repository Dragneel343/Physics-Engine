from acceleration import Acceleration
class Velocity:
	def __init__(self, dx, dy):
		self.dx = dx
		self.dy = dy

	def __iadd__(self, accel):
		if isinstance(accel, Acceleration):
			self.dx += accel.ddx
			self.dy += accel.ddy
			return self
		else:
			raise ValueError