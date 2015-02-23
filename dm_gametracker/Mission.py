'''
Mission.py
Class container for a collection of encounters.
'''

from Encounter import Encounter
import static

class Mission(object):
	def __init__(self, level=None, difficulty=None, name=None, rewards=None, description=None, gmdescription=None):
		if level == None:
			level = 0
		if difficulty == None:
			difficulty = 2 #average
		if name == None:
			name = "Unnamed Mission"
		if description == None:
			description = "No description available."
		if gmdescription == None:
			gmdescription = "No GM description available."
		if rewards == None:
			rewards = "NO REWARD"

		self.name = str(name)
		self.level = int(level)
		self.difficulty = int(difficulty)
		self.description = str(description)
		self.gmdescription = str(gmdescription)
		self.rewards = str(rewards)
		self.is_complete = False

		# list of pointers to encounters. empty on init,
		# populated later by calling "add_encounter()"
		self.encounters = []

	# end __init__

	def add_encounter(self,
					  level=None,
					  difficulty=None,
					  name=None,
					  description=None):
			encounter = Encounter(level=int(level), name=str(name), difficulty=int(difficulty), description=str(description))
			self.encounters.append(encounter)
			return encounter
	# end add_encounter

	def update(self, name, level, difficulty, description, gmdescription, rewards, state=None):
		self.name = str(name)
		self.level = int(level)
		self.difficulty = int(difficulty)
		self.description = str(description)
		self.rewards = str(rewards)
		self.gmdescription = str(gmdescription)

		if state == "True" or state == "False":
			self.is_complete = state
	# end update

	def get_encounters(self):
		return self.encounters
	def get_encounter(self, index):
		return self.encounters[int(index)]


	def get_next_noncomplete_encounter_index(self):
		for i in range(0,len(self.encounters)):
			state = self.encounters[i].get_status()

			if state != static.COMPLETE:
				return i

		return static.COMPLETE
	# end get_next_non-complete_encounter_index

	def get_complete(self):
		return self.is_complete
	def set_complete(self, is_complete):
		self.is_complete = bool(is_complete)
