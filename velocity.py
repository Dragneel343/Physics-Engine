from acceleration import Acceleration
from globals import GRAVITY

TERMINAL_VELOCITY = 15

class Velocity:
	def __init__(self, dx, dy):
		self._dx = dx
		self._dy = dy

	@property
	def dx(self):
		return self._dx

	@dx.setter
	def dx(self,dx):
		if dx > TERMINAL_VELOCITY:
			self._dx = TERMINAL_VELOCITY
		elif dx < -TERMINAL_VELOCITY:
			self._dx = -TERMINAL_VELOCITY
		else:
			self._dx = dx

	@property
	def dy(self):
		return self._dy

	@dy.setter
	def dy(self,dy):
		if dy > TERMINAL_VELOCITY:
			self._dy = TERMINAL_VELOCITY
		elif dy < -TERMINAL_VELOCITY:
			self._dy = -TERMINAL_VELOCITY
		else:
			self._dy = dy

	def __iadd__(self, accel):
		if isinstance(accel, Acceleration):
			self.dx += accel.ddx
			self.dy += accel.ddy
			return self
		else:
			raise ValueError

	def __imul__(self, scalar):
		"""
		Scalar Multiply
		"""
		if isinstance(scalar, (int, float)):
			self.dx *= scalar
			self.dy *= scalar
		return self

	def __mul__(self, scalar):
		"""
		Scalar Multiply
		"""
		if isinstance(scalar, (int, float)):
			return Velocity(self.dx * scalar, self.dy * scalar)
	
	def __repr__(self):
		return f"({round(self.dx,1)}, {round(self.dy,1)})"


	