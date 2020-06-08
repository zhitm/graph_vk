import numpy

""" 
Класс для преобразования систем координат
"""

class View:
	def __init__(self, x_tl, y_tl, win_dx, win_dy, view_dx):  # tl = top_left, v_tl - вектор верхнего левого угла
		self.v_tl = numpy.array([x_tl, y_tl])
		# размеры окна:
		self.win_dx = win_dx
		self.win_dy = win_dy
		self.x_to_y = win_dx / win_dy

		# размеры захвата декартовой плоскости
		self.dx = view_dx
		self.dy = self.dx / self.x_to_y

	def set_dx(self, new_dx):
		self.dx = new_dx
		self.dy = self.dx / self.x_to_y

	def set_dy(self, new_dy):
		self.dy = new_dy
		self.dx = self.dy * self.x_to_y

	def set_v_tl(self, pos):
		self.v_tl = numpy.asarray(pos)

	def transform(self, x, y): # трансформация из декартовой системы координат в систему координат экрана (int - для рисования)
		return [int((x - self.v_tl[0]) * self.win_dx / self.dx), int((self.v_tl[1] - y) * self.win_dx / self.dx)]

	def antitransform(self, x, y): # трансформация из системы координат экрана в декартову
		return [(x * self.dx / self.win_dx + self.v_tl[0]), (-y * self.dx / self.win_dx + self.v_tl[1])]
