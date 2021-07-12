from acceleration import Acceleration
from globals import GRAVITY

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
		return f"({self.dx}, {self.dy})"


	