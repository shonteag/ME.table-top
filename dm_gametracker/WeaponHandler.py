'''
WeaponHandler.py
This class is responsible for weapon-strings. It can
convert strings to weapon data and weapon data back to
passable strings.

'''

import random
import os

class Weapon(object):
	def __init__(self, w_type, w_type_name, w_man, w_man_name, w_key, w_name, w_quality, w_level, shots_per_round, 
				 damage_per_shot, mod_slots, crit_chance, crit_multiplier, specials, rolls=None, mod_types=None):
		self.shots_per_round = int(shots_per_round)
		self.damage_per_shot = int(damage_per_shot)
		self.mod_slots       = int(mod_slots)
		self.mod_types       = mod_types
		self.crit_chance     = int(crit_chance)
		self.crit_multiplier = float(crit_multiplier)

		self.type    = str(w_type)
		self.type_name = str(w_type_name)
		self.name    = str(w_name)
		self.man     = str(w_man)
		self.man_name= str(w_man_name)
		self.key     = str(w_key)
		self.level   = int(w_level)
		self.quality = int(w_quality)
		self.specials = specials

		self.rolls = rolls

		#icon stuff
		icon_path = 'res/icon/gear/weapon/' + str(w_type) + '/' + str(w_key) + '_' + str(w_quality) +'.gif'
		if not os.path.isfile(icon_path):
			icon_path = 'res/icon/gear/weapon/' + str(w_type) + '/base_' + str(w_quality) + '.gif'
		self.icon_path = str(icon_path)
	# end __init__

	def update(self, shots_per_round=None, damage_per_shot=None, mod_slots=None, 
			   crit_chance=None, crit_multiplier=None, specials=None, rolls=None, mod_types=None):
		if shots_per_round != None:
			self.shots_per_round = shots_per_round
		if damage_per_shot != None:
			self.damage_per_shot = damage_per_shot
		if mod_slots != None:
			self.mod_slots = mod_slots
		if crit_chance != None:
			self.crit_chance = crit_chance
		if crit_multiplier != None:
			self.crit_multiplier = crit_multiplier
		if specials != None:
			self.specials = specials
		if rolls != None:
			self.rolls = rolls
		if mod_types != None:
			self.mod_types = mod_types
	# end update

	def get_properties_as_dict(self):
		dic = {'type':self.type,
			   'type_name':self.type_name,
			   'name':self.name,
			   'man_key':self.man,
			   'man_name':self.man_name,
			   'key':self.key,
			   'level':self.level,
			   'quality':self.quality,
			   'shots_per_round':self.shots_per_round,
			   'damage_per_shot':self.damage_per_shot,
			   'mod_slots':self.mod_slots,
			   'crit_chance':self.crit_chance,
			   'crit_multiplier':self.crit_multiplier,
			   'specials':self.specials}

		return dic
	# end get_properties_as_dict

	def roll_damage(self, acc_score):
		damage = 0
		for i in range(0,self.shots_per_round):
			acc_roll = random.randrange(1,20+1)
			if acc_roll <= acc_score:
				this_damage = random.randrange(1,self.damage_per_shot+1)
				if acc_roll <= self.crit_chance:
					this_damage *= self.crit_multiplier
				damage += this_damage

		return damage
	# end roll_damage
# end Weapon