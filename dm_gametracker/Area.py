'''
Class that represents an area on a planet.
'''

from Mission import Mission
from Store import Store
import static

class Area(object):
	def __init__(self, name=None, level=None, difficulty=None, description=None, gmdescription=None):
		self.name = str(name)
		self.level = int(level)
		self.difficulty = int(difficulty)
		self.description = str(description)
		self.gmdescription = str(gmdescription)

		self.missions = []
		self.stores = []
	# end __init__

	def add_mission(self, name=None, level=None, difficulty=None, rewards=None, description=None):
		new_mission = Mission(name=name, level=level, difficulty=difficulty, description=description, rewards=rewards)
		self.missions.append(new_mission)
		return new_mission
	# end add_mission

	def update(self, name=None, level=None, difficulty=None, description=None, gmdescription=None):
		self.name = str(name)
		self.level = int(level)
		self.difficulty = int(difficulty)
		self.description = str(description)
		self.gmdescription = str(gmdescription)
	# end update