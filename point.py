class Point:
	def __init__(self,x=0,y=0):
		self._x = x
		self._y = y

	@property
	def x(self):
		return self._x
	@x.setter
	def x(self,x):
		self._x = int(x)

	@property
	def y(self):
		return self._y
	@y.setter
	def y(self,y):
		self._y = int(y)

	