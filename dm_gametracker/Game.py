'''
Game.py
This is a class container that houses many pointers to Mission objects.
It has no inherent properties.
'''

import static
from Planet import Planet
from Mission import Mission
from PowerHandler import PowerHandler
from ClassHandler import ClassHandler
from ItemHandler import Item

class Game(object):
	def __init__(self, name=None, date_started=None):
		self.name = str(name)
		self.date_started = str(date_started)

		#self.PowerHandler = PowerHandler()
		#self.ClassHandler = ClassHandler()

		self.planets = []
		self.raids = []
		self.missions = []
		self.items = []
	# end __init__

	def add_planet(self, name=None, level=None, difficulty=None, description=None):
		new_planet = Planet(name=name, level=level, difficulty=difficulty, description=description)
		self.planets.append(new_planet)
		return new_planet
	# end add_planet

	def add_priority_mission(self, name=None, level=None, difficulty=None, description=None):
		new_pri_mission = Mission(name=name, level=level, difficulty=difficulty, description=description)
		self.missions.append(new_pri_mission)
		return new_pri_mission
	# end add_priority_mission

	def get_next_priority_mission(self):
		for index, primission in enumerate(self.missions):
			if primission.is_complete:
				continue
			else:
				print index, self.missions[index].is_complete
				return (index, self.missions[index])
		return (-1, None)

	def add_raid(self, ):
		pass
	# end add_raid

	def add_item(self, name=None):
		new_item = Item(name=name)
		self.items.append(new_item)
		return new_item
	# end add_item
