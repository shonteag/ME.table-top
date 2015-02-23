'''
Class that represents a store, located in a peaceful area.
'''

import static
from LootHandler import LootHandler
from Encounter import Encounter

class Store(object):
	def __init__(self, name=None, special_slots=None, special_min_rarity=None, max_rarity=None, description=None, gmdescription=None):
		self.name = str(name)
		self.description = str(description)
		self.gmdescription = str(gmdescription)

		if special_slots == None:
			special_slots = 1
		self.special_slots = int(special_slots)
		if special_min_rarity == None:
			special_min_rarity = 2
		self.special_min_rarity = int(special_min_rarity)

		if max_rarity == None:
			max_rarity = 3
		self.max_rarity = max_rarity

		# -1 is infinite
		self.max_shield_charge_quantity = -1
		self.current_shield_charge_quantity = -1
		self.max_health_pack_quantity = -1
		self.current_health_pack_qunatity = -1

		self.specials = []
		self.merchandise = []

		self.LootHandler = LootHandler()
	# end __init__

	def update(name, special_slots, special_min_rarity, max_rarity, description, gmdescription):
		self.name = str(name)
		self.description = str(description)
		self.gmdescription = str(gmdescription)
		self.special_slots = int(special_slots)
		self.special_min_rarity = int(special_min_rarity)
		self.max_rarity = int(max_rarity)
	# end update

	def add_loot_table(self, loot_table=None, specials=None):
		if loot_table != None:
			self.merchandise = loot_table
		if specials != None:
			self.specials = specials
	# end add_loot_table

	def restock(self):
		self.current_health_pack_qunatity = self.max_health_pack_quantity
		self.current_shield_charge_quantity = self.max_shield_charge_quantity
	# end restock

	def roll_specials(self):
		self.specials = []
		for i in range(0, self.special_slots):
			self.specials.append(LootHandler.roll_store_special_item(min_rarity=special_min_rarity, max_rarity=max_rarity))
	# end roll_specials

	
# end Store
