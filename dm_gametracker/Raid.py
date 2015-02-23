'''
Raid.py
Extension of Mission object that represents a "raid".
'''

from Encounter import Encounter
from RaidEncounter import RaidEncounter
from Mission import Mission
import static

class Raid(Mission):
	def __init__(self, name=None, description=None):
		if name == None:
			name = "Unnamed Raid"
		if description == None:
			description = "No description available."

		self.name = str(name)
		self.level = int(20)
		self.difficulty = int(4)
		self.description = str(description)
		self.is_complete = False

		# list of pointers to encounters. empty on init,
		# populated later by calling "add_encounter()"
		self.encounters = []

	# end __init__

	def add_encounter(self, name=None, description=None, is_boss=None):
		newencounter = RaidEncounter(name=name, description=description, is_boss=is_boss)
		self.encounters.append(newencounter)
		return newencounter
	# end add_encounter