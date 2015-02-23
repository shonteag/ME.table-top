'''
Class that represents a planet.
'''

from Area import Area
import static

class Planet(object):
	def __init__(self, name=None, level=None, difficulty=None, description=None, gmdescription=None):
		self.name = str(name)
		self.level = int(level)
		self.difficulty = int(difficulty)
		self.description = str(description)
		self.gmdescription = str(gmdescription)

		self.areas = []
	# end __init__

	def add_area(self, name=None, level=None, difficulty=None, description=None):
		new_area = Area(name=name, level=level, difficulty=difficulty, description=description)
		self.areas.append(new_area)
		return new_area
	# end add_area

	def update(self, name=None, level=None, difficulty=None, description=None, gmdescription=None):
		self.name = str(name)
		self.level = int(level)
		self.difficulty = int(difficulty)
		self.description = str(description)
		self.gmdescription = str(gmdescription)
	# end update