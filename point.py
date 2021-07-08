from velocity import Velocity


class Point:
	def __init__(self,x=0,y=0):
		self._x = x
		self._y = y

	@property
	def x(self):
		return int(self._x)
	@x.setter
	def x(self,x):
		self._x = x

	@property
	def y(self):
		return int(self._y)
	@y.setter
	def y(self,y):
		self._y = y
	
	def __iter__(self):
		yield self.x
		yield self.y

	def __iadd__(self, vector):
		self._x += vector.dx
		self._y -= vector.dy # -= for accurate visual representation. (cv2 flips y-axis)
		return self

	def __add__(self, vector):
		if isinstance(vector, Point):
			return Point(self._x + vector.x, self._y - vector.y)
		elif isinstance(vector, Velocity):
			return Point(self._x + vector.x, self._y - vector.dy)
		raise TypeError

	def __repr__(self):
		return f"({self.x},{self.y})"
	
	

		
	