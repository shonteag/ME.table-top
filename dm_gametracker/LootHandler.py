'''
Class for the handling of loot rolling
'''

import random
import os
import math
from copy import deepcopy

from Encounter import Encounter
from Enemy import Enemy
from WeaponHandler import Weapon
from ArmorHandler import Armor
from ItemHandler import Item
import static


import xml.etree.cElementTree as et

class LootHandler(object):
	def __init__(self):
		# load weapons
		# this is keyed by gear type
		# 'weapon':{'AR':{'manufacturer':{'rarity#':{'stat', 'stat', ...}, 'rarity#':{}, ...}, 'manufacturer':{}, ...}, 'SR':{}, ...}
		# 'armor':{'light':{'manufacturer':{'rarity#':{'stat', 'stat', ...}, 'rarity#':{}, ...}, 'manufacturer':{}, ...} 'medium':{}, 'heavy':{}}
		self.base_gear_lookup = {'weapon':{'AR':{},
										   'SR':{},
										   'HP':{},
										   'SH':{},
										   'SMG':{}},
								 'armor':{'armor_light':{},
								 		  'armor_medium':{},
								 		  'armor_heavy':{}}}

		self.key_lookup = {}
		self.special_lookup = {}

		files = ['xml/gear/weapon/AR.xml',
				 'xml/gear/weapon/SR.xml',
				 'xml/gear/weapon/HP.xml',
				 'xml/gear/weapon/SH.xml',
				 'xml/gear/weapon/SMG.xml',
				 'xml/gear/armor/light.xml',
				 'xml/gear/armor/medium.xml',
				 'xml/gear/armor/heavy.xml']

		for filepath in files:
			tree = et.parse(filepath)
			root = tree.getroot()

			if root.tag == 'weapon_type':
				# this is a weapon
				weapon_type = root.attrib['key']
				if weapon_type not in self.key_lookup:
					self.key_lookup.update({weapon_type:root.attrib['name']})

				for man in root:
					if man.attrib['key'] not in self.key_lookup:
						self.key_lookup.update({man.attrib['key']:man.attrib['name']})
					if man.attrib['key'] not in self.base_gear_lookup['weapon'][weapon_type]:
						self.base_gear_lookup['weapon'][weapon_type].update({man.attrib['key']:{}})
					for weapon in man:
						if weapon.attrib['key'] not in self.key_lookup:
							self.key_lookup.update({weapon.attrib['key']:weapon.attrib['name']})
						if (weapon.attrib['key'] not in self.special_lookup) and ('special' in weapon.attrib):
							self.special_lookup.update({weapon.attrib['key']:weapon.attrib['special']})
						self.base_gear_lookup['weapon'][weapon_type][man.attrib['key']].update({weapon.attrib['key']:{}})
						for rarity in weapon:
							self.base_gear_lookup['weapon'][weapon_type][man.attrib['key']][weapon.attrib['key']].update({rarity.attrib['key']:{}})
							for att in rarity.attrib:
								self.base_gear_lookup['weapon'][weapon_type][man.attrib['key']][weapon.attrib['key']][rarity.attrib['key']].update({att:rarity.attrib[att]})

			elif root.tag == 'armor_type':
				armor_type = root.attrib['key']
				if armor_type not in self.key_lookup:
					self.key_lookup.update({armor_type:root.attrib['name']})

				for man in root:
					if man.attrib['key'] not in self.key_lookup:
						self.key_lookup.update({man.attrib['key']:man.attrib['name']})
					if man.attrib['key'] not in self.base_gear_lookup['armor'][armor_type]:
						self.base_gear_lookup['armor'][armor_type].update({man.attrib['key']:{}})
					for armor in man:
						if armor.attrib['key'] not in self.key_lookup:
							self.key_lookup.update({armor.attrib['key']:armor.attrib['name']})
						if (armor.attrib['key'] not in self.special_lookup) and ('special' in armor.attrib):
							self.special_lookup({armor.attrib['key']:armor.attrib['special']})
						self.base_gear_lookup['armor'][armor_type][man.attrib['key']].update({armor.attrib['key']:{}})
						for rarity in armor:
							self.base_gear_lookup['armor'][armor_type][man.attrib['key']][armor.attrib['key']].update({rarity.attrib['key']:{}})
							for att in rarity.attrib:
								self.base_gear_lookup['armor'][armor_type][man.attrib['key']][armor.attrib['key']][rarity.attrib['key']].update({att:rarity.attrib[att]})

	# end __init__

	'''
	Takes a list of tuples ([(item_id_number, %_chance_drop)]) and uses that
	to determine which (if any) drops.
	'''
	def roll_custom_loot(self, game, customs):
		rolled = []
		for item_tuple in customs:
			roll = random.randrange(0,101)
			if roll <= item_tuple[1]:
				new_item = deepcopy(game.items[int(item_tuple[0])])
				rolled.append(new_item)
		return rolled
	# end roll_custom_loot

	def roll_encounter_loot(self, game, encounter, avg_player_level, number_of_players):
		loot_table = []
		credits = 0

		if not encounter.customs_only:
			total_rolls = len(encounter.enemies) * int(math.floor(encounter.get_average_mob_level()))
			difficulty_ratio = (float(math.floor(encounter.get_average_mob_level())) / float(math.floor(avg_player_level)))
			difficulty_ratio *= (float(len(encounter.enemies)) / float(number_of_players))
			difficulty_ratio *= (float(math.ceil(encounter.get_average_mob_difficulty())) / float(2))
			if encounter.is_boss:
				difficulty_ratio += 1.0

			chart_key = ''

			if difficulty_ratio <= .05:
				return # no loot
			elif difficulty_ratio <= .1:
				#very low loot
				chart_key = 'very_low'
			elif difficulty_ratio <= .49:
				#low loot
				chart_key = 'low'
			elif difficulty_ratio <= 2:
				#average loot
				chart_key = 'average'
			elif difficulty_ratio <= 3:
				#good
				chart_key = 'good'
			elif difficulty_ratio <= 3.5:
				#very good
				chart_key = 'very_good'
			else: # difficulty_ratio > 3.5
				chart_key = 'exceptional'

			quality_chart = {'very_low':[7000, 10000, -1, -1, -1],
							 'low':[5249, 9924, 9994, 9999, 10000],
							 'average':[4850, 8350, 9550, 9950, 10000],
							 'good':[2450, 6950, 8950, 9750, 10000],
							 'very_good':[1400, 5400, 7900, 9400, 10000],
							 'exceptional':[-1, 3000, 6000, 8500, 10000]}

			quality_credits = {'very_low':[5, 10, 0, 0, 0],
							   'low':[25, 70, 150, 275, 370],
							   'average':[100, 160, 300, 500, 1000],
							   'good':[200, 350, 600, 750, 1000],
							   'very_good':[400, 600, 800, 1000, 1200],
							   'exceptional':[600, 900, 1300, 1600, 2000]}

			print "----| LOOT SUMMARY |---------------------------------"
			print "|   "
			print "| total_rolls: " + str(total_rolls)
			print "| difficulty_ratio: " + str(difficulty_ratio) + ", " + str(chart_key)
			# print "| LOOT:"

			for roll_index in range(0,total_rolls):
				quality_roll = random.randrange(1,10001)
				for qindex, quality_threshold in enumerate(quality_chart[chart_key]):
					if quality_roll <= quality_threshold:
						loot_roll = random.randrange(1,101)

						loot_type = None
						if loot_roll <= 40:
							# nothing
							break
						elif loot_roll > 40 and loot_roll <= 90:
							# credits
							if qindex == 0:
								credits += random.randrange(0, quality_credits[chart_key][qindex])
							else:
								credits += random.randrange(quality_credits[chart_key][qindex-1], quality_credits[chart_key][qindex])
							loot_type = 'credits'
						elif loot_roll > 90:
							# item
							loot_type = 'item'

						if loot_type == 'item':
							# choose type of item
							item_type = random.choice(self.base_gear_lookup.keys())
							# choose sub type
							item_sub_type = random.choice(self.base_gear_lookup[item_type].keys())
							# choose manufacturer
							item_man = random.choice(self.base_gear_lookup[item_type][item_sub_type].keys())
							# choose item
							item_key = random.choice(self.base_gear_lookup[item_type][item_sub_type][item_man].keys())

							item_base_dic = self.base_gear_lookup[item_type][item_sub_type][item_man][item_key][str(qindex)]
							item_name = self.key_lookup[item_key]

							#add specials to item
							if item_key in self.special_lookup:
								special = self.special_lookup[item_key]
							else:
								special = ""

							# roll more stats onto loot!
							if item_type == 'weapon':
								w_level = int(math.floor(encounter.get_average_mob_level()))
								w_quality = qindex
								w_shots_per_round = int(item_base_dic['speed'])
								w_damage_per_shot = int(item_base_dic['damage'])
								w_mod_slots       = int(item_base_dic['mod_slots'])
								w_mod_types       = []
								w_crit_chance     = int(item_base_dic['crit_chance'])
								w_crit_multiplier = float(item_base_dic['crit_multiplier'])

								#TODO: ADJUST DAMAGE / SHOTS_PER_ROUND FOR LEVEL!!!!!!!
								rolls = []
								potential_mod_types = deepcopy(static.mod_slot_types)
								potentials = deepcopy(static.weapon_stats[item_sub_type])

								w_mod_slots = 0

								roll_index = 0
								while roll_index < w_quality:
									choice_index = random.randrange(0,len(potentials))
									choice = potentials[choice_index]
									potentials.pop(choice_index)
									
									if choice.split(":")[0] == 'Fire Type':
										to_remove = []
										for i,pot in enumerate(potentials):
											if pot.split(":")[0] == 'Fire Type':
												to_remove.append(i)
										for index,i in enumerate(to_remove):
											potentials.pop(i-index)
									elif choice.split(":")[0] == 'Mod Slots':
										number_of_slots = random.randrange(1,6)
										w_mod_slots += number_of_slots
										choice = 'Mod Slots: ' + str(w_mod_slots)
									elif choice.split(":")[0] == 'Extra Roll' or choice.split(":")[0] == 'Bonus Roll':
										roll_index -= 2
									elif choice.split(":")[0] == 'Crit Mult':
										mult = random.choice([.25, .5, .75, 1])
										choice = 'Crit Mult: +' + str(int(mult * 100.0)) + '%'
										w_crit_multiplier += float((float(w_crit_multiplier) * float(mult)))
										w_crit_multiplier = round(w_crit_multiplier, 1)
									elif 'Permanent' in choice.split(":")[0].split():
										mod_type = choice.split(":")[0].split()[1]
										to_remove = []
										for i,pot in enumerate(potentials):
											if mod_type == pot.split(":")[0].split()[1]:
												to_remove.append(i)
										for index,i in enumerate(to_remove):
											potentials.pop(i-index)

										potential_mod_types.pop(potential_mod_types.index(mod_type))
										w_mod_slots -= 1

									rolls.append(choice)
									roll_index += 1

								# handle mod slots
								if w_mod_slots > 0:
									for i in range(0, w_mod_slots):
										mod = random.choice(potential_mod_types)
										w_mod_types.append(mod)
										potential_mod_types.pop(potential_mod_types.index(mod))
								else:
									w_mod_slots = 0


								weapon = Weapon(item_sub_type, self.key_lookup[item_sub_type], item_man, self.key_lookup[item_man], item_key, self.key_lookup[item_key],
									   		    w_quality, w_level,
									   		    w_shots_per_round, w_damage_per_shot, w_mod_slots, w_crit_chance, w_crit_multiplier, special, rolls=rolls, mod_types=w_mod_types)
								loot_table.append(weapon)

							elif item_type == 'armor':
								a_level = int(math.floor(encounter.get_average_mob_level()))
								a_quality = qindex
								a_shield = int(item_base_dic['shield'])
								a_shield_recharge = int(item_base_dic['shield_recharge'])
								a_damage_reduction = int(item_base_dic['damage_reduction'])
								a_mod_slots = int(item_base_dic['mod_slots'])

								#TODO: ADJUST SHIELD/SR/DR FOR LEVEL!!!!!

								armor = Armor(item_sub_type, self.key_lookup[item_sub_type], item_man, self.key_lookup[item_man], item_key, self.key_lookup[item_key],
											  a_quality, a_level,
											  a_shield, a_shield_recharge, a_damage_reduction, a_mod_slots, special)

								loot_table.append(armor)

							else:
								#problem. there are only those types of items.
								pass

							# print "|   " + str(item_name) + " (" + str(self.key_lookup[item_sub_type]) + ", Quality " + str(qindex) + ")"
							# print "|   " + str(self.key_lookup[item_man])
							# for key, val in item_base_dic.iteritems():
							# 	print "|        " + str(key) + ": " + str(val)

						break

			print "-----------------------------------------------------"

		# add custom items
		custom_loot = self.roll_custom_loot(game, encounter.special_loot)
		for item in custom_loot:
			loot_table.append(item)

		return (credits, loot_table)
	# end roll_encounter_loot

	'''
	number_items (int) is the size of the chest. If 0 and can_have_credits=True, will only contain credits.
	chest_type (str, 'very_low'/'low'/'average'/'good'/'very_good'/'exceptional') specifies quality roll chances
	guaranteed_quality (int, 0-5). If set, will ignore min_quality and max_quality.
	gear_type (str, "armor" or "weapon"). If unset, will roll 50/50 chance.
	can_have_credits (bool)
	'''
	def roll_chest_loot(self, chest_level=None, number_items=None, chest_type=None, guaranteed_quality=None, gear_type=None, can_have_credits=None):
		if number_items == None:
			number_items = 0

		loot_table = []

		print "----| CHEST SUMMARY |--------------------------------"
		print "| Chest Type: " + str(chest_type)
		print "| Number of Items: " + str(number_items)
		print "| Gear Type: " + str(gear_type)
		print "| Credit Chest: " + str(can_have_credits)

		# roll items
		for i in range(0, number_items):
			# roll rarity
			if guaranteed_quality == None:
				quality_roll = random.randrange(0, 10001)
				quality = None
				for qindex, quality_threshold in enumerate(static.quality_chart[chest_type]):
					if quality_roll <= quality_threshold:
						quality = qindex
						break
			else:
				quality = int(guaranteed_quality)

			# roll gear type
			if gear_type == None or gear_type == 'None':
				gear_type = random.choice(self.base_gear_lookup.keys())
			
			# choose sub type
			item_sub_type = random.choice(self.base_gear_lookup[gear_type].keys())
			# choose manufacturer
			item_man = random.choice(self.base_gear_lookup[gear_type][item_sub_type].keys())
			# choose item
			item_key = random.choice(self.base_gear_lookup[gear_type][item_sub_type][item_man].keys())
			item_base_dic = self.base_gear_lookup[gear_type][item_sub_type][item_man][item_key][str(quality)]
			item_name = self.key_lookup[item_key]

			#add specials to item
			if item_key in self.special_lookup:
				special = self.special_lookup[item_key]
			else:
				special = ""

			# roll more stats onto loot!
			if gear_type == 'weapon':
				w_level = int(chest_level)
				w_quality = quality
				w_shots_per_round = int(item_base_dic['speed'])
				w_damage_per_shot = int(item_base_dic['damage'])
				w_mod_slots       = int(item_base_dic['mod_slots'])
				w_mod_types       = []
				w_crit_chance     = int(item_base_dic['crit_chance'])
				w_crit_multiplier = float(item_base_dic['crit_multiplier'])

				#TODO: ADJUST DAMAGE / SHOTS_PER_ROUND FOR LEVEL!!!!!!!
				rolls = []
				potential_mod_types = deepcopy(static.mod_slot_types)
				potentials = deepcopy(static.weapon_stats[item_sub_type])

				w_mod_slots = 0

				roll_index = 0
				while roll_index < w_quality:
					choice_index = random.randrange(0,len(potentials))
					choice = potentials[choice_index]
					potentials.pop(choice_index)
					
					if choice.split(":")[0] == 'Fire Type':
						to_remove = []
						for i,pot in enumerate(potentials):
							if pot.split(":")[0] == 'Fire Type':
								to_remove.append(i)
						for index,i in enumerate(to_remove):
							potentials.pop(i-index)
					elif choice.split(":")[0] == 'Mod Slots':
						number_of_slots = random.randrange(1,6)
						w_mod_slots += number_of_slots
						choice = 'Mod Slots: ' + str(w_mod_slots)
					elif choice.split(":")[0] == 'Extra Roll' or choice.split(":")[0] == 'Bonus Roll':
						roll_index -= 2
					elif choice.split(":")[0] == 'Crit Mult':
						mult = random.choice([.25, .5, .75, 1])
						choice = 'Crit Mult: +' + str(int(mult * 100.0)) + '%'
						w_crit_multiplier += float((float(w_crit_multiplier) * float(mult)))
						w_crit_multiplier = round(w_crit_multiplier, 1)
					elif 'Permanent' in choice.split(":")[0].split():
						mod_type = choice.split(":")[0].split()[1]
						to_remove = []
						for i,pot in enumerate(potentials):
							if mod_type == pot.split(":")[0].split()[1]:
								to_remove.append(i)
						for index,i in enumerate(to_remove):
							potentials.pop(i-index)

						potential_mod_types.pop(potential_mod_types.index(mod_type))
						w_mod_slots -= 1

					rolls.append(choice)
					roll_index += 1

				# handle mod slots
				if w_mod_slots > 0:
					for i in range(0, w_mod_slots):
						mod = random.choice(potential_mod_types)
						w_mod_types.append(mod)
						potential_mod_types.pop(potential_mod_types.index(mod))
				else:
					w_mod_slots = 0




				weapon = Weapon(item_sub_type, self.key_lookup[item_sub_type], item_man, self.key_lookup[item_man], item_key, self.key_lookup[item_key],
					   		    w_quality, w_level,
					   		    w_shots_per_round, w_damage_per_shot, w_mod_slots, w_crit_chance, w_crit_multiplier, special, rolls=rolls, mod_types=w_mod_types)
				loot_table.append(weapon)

			elif gear_type == 'armor':
				a_level = int(chest_level)
				a_quality = quality
				a_shield = int(item_base_dic['shield'])
				a_shield_recharge = int(item_base_dic['shield_recharge'])
				a_damage_reduction = int(item_base_dic['damage_reduction'])
				a_mod_slots = int(item_base_dic['mod_slots'])

				#TODO: ADJUST SHIELD/SR/DR FOR LEVEL!!!!!
				armor = Armor(item_sub_type, self.key_lookup[item_sub_type], item_man, self.key_lookup[item_man], item_key, self.key_lookup[item_key],
							  a_quality, a_level,
							  a_shield, a_shield_recharge, a_damage_reduction, a_mod_slots, special)
				loot_table.append(armor)

			else:
				print "ERROR: (loothandler) no item key: " + str(gear_type)

		# roll credits
		credits = 0
		if can_have_credits:
			for i in range(0, static.credit_rolls[chest_type]):
				quality_roll = random.randrange(1,10001)
				quality = None
				for qindex, quality_threshold in enumerate(static.quality_chart[chest_type]):
					if quality_roll <= quality_threshold:
						quality = qindex
						break
				if quality != 0:
					credits += random.randrange(static.quality_credits[chest_type][quality-1], static.quality_credits[chest_type][quality])
				else:
					credits += random.randrange(0, static.quality_credits[chest_type][quality])

		print "-----------------------------------------------------"

		# add custom items

		return (credits, loot_table)
	# end roll_chest_loot

	def roll_store_special_item(self, gear_type=None, min_rarity=None, max_rarity=None, level=None, man_key=None):
		# roll quality
		rarity = random.randrange(min_rarity, max_rarity+1)

		# roll gear type
		if gear_type == None or gear_type == 'None':
			gear_type = random.choice(self.base_gear_lookup.keys())
		
		# choose sub type
		item_sub_type = random.choice(self.base_gear_lookup[gear_type].keys())
		# choose manufacturer
		if man_key == None:
			item_man = random.choice(self.base_gear_lookup[gear_type][item_sub_type].keys())
		else:
			item_man = man_key
		# choose item
		item_key = random.choice(self.base_gear_lookup[gear_type][item_sub_type][item_man].keys())
		item_base_dic = self.base_gear_lookup[gear_type][item_sub_type][item_man][item_key][str(quality)]
		item_name = self.key_lookup[item_key]

		#add specials to item
		if item_key in self.special_lookup:
			special = self.special_lookup[item_key]
		else:
			special = ""

		# roll more stats onto loot!
		if gear_type == 'weapon':
			w_level = int(level)
			w_quality = quality
			w_shots_per_round = int(item_base_dic['speed'])
			w_damage_per_shot = int(item_base_dic['damage'])
			w_mod_slots       = int(item_base_dic['mod_slots'])
			w_crit_chance     = int(item_base_dic['crit_chance'])
			w_crit_multiplier = float(item_base_dic['crit_multiplier'])

			#TODO: ADJUST DAMAGE / SHOTS_PER_ROUND FOR LEVEL!!!!!!!
			weapon = Weapon(item_sub_type, self.key_lookup[item_sub_type], item_man, self.key_lookup[item_man], item_key, self.key_lookup[item_key],
				   		    w_quality, w_level,
				   		    w_shots_per_round, w_damage_per_shot, w_mod_slots, w_crit_chance, w_crit_multiplier, special)
			return weapon

		elif gear_type == 'armor':
			a_level = int(level)
			a_quality = quality
			a_shield = int(item_base_dic['shield'])
			a_shield_recharge = int(item_base_dic['shield_recharge'])
			a_damage_reduction = int(item_base_dic['damage_reduction'])
			a_mod_slots = int(item_base_dic['mod_slots'])

			#TODO: ADJUST SHIELD/SR/DR FOR LEVEL!!!!!
			armor = Armor(item_sub_type, self.key_lookup[item_sub_type], item_man, self.key_lookup[item_man], item_key, self.key_lookup[item_key],
						  a_quality, a_level,
						  a_shield, a_shield_recharge, a_damage_reduction, a_mod_slots, special)
			return armor

		else:
			print "ERROR: (loothandler) no item key: " + str(gear_type)
	# end roll_store_special_item

if __name__=="__main__":
	loot_handler = LootHandler()
	loot_handler.print_stuff('weapon')

	encounter = Encounter(name='Test', level=5, difficulty=2)
	encounter.add_enemy()