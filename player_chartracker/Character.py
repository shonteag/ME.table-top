'''
Enemy.py
This class IS the enemy. It tracks powers, weapons,
health, shields, armor and everything that goes with
them: cooldowns, durations, etc.
It also tacks negative effect applied by players: dots,
debuffs, primer effects, etc.
'''

import sys
from copy import deepcopy
import math

from ClassHandler import ClassHandler
from PowerHandler import PowerHandler
#from WeaponHandler import Weapon
from Roller import Roller
import static

class Character(object):

	'''__init__
	name 			: str, human-friendly identifier
	class_key		: str, [SOL, VAN, SEN, SOL, ADT, INF]
	race			: str, [Asari, Human, Turian, Salarian]
	role			: str, [support, tank, dps, none]
	level			: int, [1, ..., 20]
	difficulty		: int, [1 (trash), 2 (elite), 3 (champion), 4 (boss)]
	max_health		: int
	max_shield		: int
	damage_reduction: int
	weapons			: str "4, 4, 4, 8, 6, ..." (Each comma-delimited indicates an attack roll.)
	powers			: list, [power_key, power_key, ...]
	description		: str
	power_handler   : PowerHandler object
	class_handdler  : ClassHandler object
	stats			: dict {'FIT','ACC','CON','AWR','INT','BIF'}
	'''
	def __init__(self,
				 name=None,
				 class_key=None,
				 race=None,
				 role=None,
				 level=None,
				 difficulty=None,
				 max_health=None,
				 max_shield=None,
				 shield_recharge=None,
				 max_armor=None,
				 damage_reduction=None,
				 weapons=None,
				 powers=None,
				 description=None,
				 power_handler=None,
				 class_handler=None,
				 stats=None):
		'''Tracks character properties, passed to new istances of Enemy
		at init-time.
		'''
		self.properties = {}

		if name == None:
			name = "No Name"
		if class_key == None:
			class_key = static.CLASS_SOLDIER
		if race == None:
			race = static.RACE_HUMAN
		if role == None:
			role = static.ROLE_NONE
		if level == None:
			level = 0
		if difficulty == None:
			difficulty = 2
		if max_health == None:
			max_health = 100
		if max_shield == None:
			max_shield = 200
		if shield_recharge == None:
			shield_recharge = 10
		if max_armor == None:
			max_armor = 0
		if damage_reduction == None:
			damage_reduction = float(0)
		if power_handler == None:
			power_handler = PowerHandler()
		if class_handler == None:
			class_handler = ClassHandler()
		if weapons == None:
			weapons = None
		if powers == None:
			powers = []
		if stats == None:
			if class_key != static.CLASS_NONE and class_key in static.CLASSES:
				stats = class_handler.get_class_details(class_key=str(class_key))['base_stats']
			else:
				stats = static.STATS_DEFAULT


		self.properties.update({'name':str(name)})
		self.properties.update({'class_key':str(class_key)})
		self.properties.update({'race':str(race)})
		self.properties.update({'role':str(role)})
		self.properties.update({'level':int(level)})
		self.properties.update({'difficulty':int(difficulty)})
		self.properties.update({'max_health':int(max_health)})
		self.properties.update({'health':int(max_health)})
		self.properties.update({'max_shield':int(max_shield)})
		self.properties.update({'shield_recharge':int(shield_recharge)})
		self.properties.update({'shield':int(max_shield)})
		self.properties.update({'max_armor':int(max_armor)})
		self.properties.update({'armor':int(max_armor)})
		self.properties.update({'damage_reduction':float(damage_reduction)})
		self.properties.update({'weapons':weapons})
		self.properties.update({'powers':powers})
		self.properties.update({'description':str(description)})
		self.properties.update({'base_stats':stats})

		# set to False to stop tracking.
		self.is_alive = True

		# is primed for biotic or tech detonation. if 0 then no, otherwise
		# int indicates how many turns before it falls off.
		self.tech_primed = 0
		self.biotic_primed = 0

		'''power_tracker tracks power cooldowns.
		{power_key:int(turns_until_ready)}
		If turns_until_ready == 0, then power is ready.
		Every power turns_until_ready -= 1 at start of new turn.
		'''
		self.power_tracker = {}

		'''negative_effects tracks negative effects such as powers
		cast by players (dots, debuffs) and how long they are active.
		{power_key:int(turns_until_gone)}
		'''
		self.negative_effects = {}

		'''task_on_turn tracks each task to complete on turns.
		For instance, 'shield + 10' increases shiled by 10 at start
		of each turn.
		'''
		self.task_on_turn = []


		self.PowerHandler = power_handler
		self.ClassHandler = class_handler

		self.Roller = Roller()

		if stats == None:
			self.stats = static.STATS_DEFAULT

		#setup powers
		self._setup_powers()
	# end __init__

	def update(self, name, level, difficulty, role, race, class_key, max_health, max_shield, shield_recharge, max_armor, damage_reduction,
			   weapons, powers, description, stats):
		self.properties['name'] = str(name)
		self.properties['level'] = int(level)
		self.properties['difficulty'] = int(difficulty)
		self.properties['role'] = str(role)
		self.properties['race'] = str(race)
		self.properties['class_key'] = str(class_key)
		self.properties['max_health'] = int(max_health)
		self.properties['health'] = int(max_health)
		self.properties['max_shield'] = int(max_shield)
		self.properties['shield'] = int(max_shield)
		self.properties['shield_recharge'] = int(shield_recharge)
		self.properties['max_armor'] = int(max_armor)
		self.properties['armor'] = int(max_armor)
		self.properties['damage_reduction'] = float(damage_reduction)
		self.properties['weapons'] = weapons
		self.properties['powers'] = powers
		self.properties['description'] = str(description)
		self.properties['base_stats'] = stats

		self._setup_powers()
	# end update

	def update_stats(self, stats):
		self.properties['base_stats'] = stats
	# end update_stats

	def add_weapon(self, weapon):
		self.properties['weapons'] = weapon
	# end add_weapon

	def _setup_powers(self):
		for power_key in self.properties['powers']:
			self.power_tracker.update({str(power_key):0})
	# end _setup_powers

	'''use_power sets the cooldown.'''
	def use_power(self, power_key):
		power_properties = self.PowerHandler.get_power_details(power_keys=[str(power_key)])
		self.power_tracker.update({str(power_key):int(power_properties[power_key]['cd'])})

		damage = self.PowerHandler.roll_power_damage(power_key, self.properties['level'], self.properties['difficulty'])
		return damage
	# end use_power

	'''used when an enemy throws a power at this target'''
	def character_cast_on_self(self, power_key):
		powers_properties = self.PowerHandler.get_power_details(power_keys=[str(power_key)])
		power_properties = powers_properties[power_key]
		power_type = self.PowerHandler.get_power_type(str(power_key))

		used = False
		used_as_detonator = False

		tech_combo = 0 #False
		biotic_combo = 0 #False

		# this automatically rolls base damage to level and difficulty of mob
		base_damage = float(self.PowerHandler.roll_power_damage(power_key, self.properties['level'], self.properties['difficulty']))

		# -------------------------------------------
		# COMBOS
		if power_properties['detonator']:
			if power_type == 'tech':
				if self.tech_primed > 0:
					used_as_detonator = True
					# TECH DETONATION!
					tech_combo = 1 #True
					print "Tech Explosion!"
					self.tech_primed = 0
					used = True
			elif power_type == 'biotic':
				if self.biotic_primed > 0:
					used_as_detonator = True
					#BIOTIC DETONATION!
					biotic_combo = 1 #True
					print "Biotic Combo!"
					self.biotic_primed = 0
					used = True

		if power_properties['primer'] and used == False:
			if power_type == 'tech':
				#target primed!
				self.tech_primed = int(power_properties['duration'])
				print "Primed for tech combo for " + str(self.tech_primed) + " turns!"
			elif power_type == 'biotic':
				#biotic primed
				self.biotic_primed = int(power_properties['duration'])
				print "Primed for biotic combo for " + str(self.biotic_primed) + " turns!"

		# -------------------------------------------
		# DOTS
		if power_properties['dot'] and not used_as_detonator:
			print "Dotted for " + str(power_properties['duration']) + " turns!"
			self.negative_effects.update({power_key:int(power_properties['duration'])})

		# calculate immediate damage
		base_damage *= (static.BIOTIC_COMBO_MULTIPLIER*biotic_combo)
		base_damage *= (static.TECH_COMBO_MULTIPLIER*tech_combo)

		return int(math.floor(base_damage))

	# end enemy_cast_on_self

	'''This method is used to call the next turn. All cooldowns -1,
	shields + shield restore value, all dots -1, tech and biotic primes -1,
	and all task_on_turn entries executed.
	'''
	def new_turn(self):
		#check if alive
		if not self.is_alive:
			return 0

		# Cooldowns first.
		for key, cdval in self.power_tracker.iteritems():
			if cdval >= 1:
				self.power_tracker[key] = cdval - 1

		# now primes
		if self.tech_primed >= 1:
			self.tech_primed -= 1
		if self.biotic_primed >= 1:
			self.biotic_primed -= 1

		#now shields
		if self.properties['shield'] < self.properties['max_shield']:
			shield_damage = self.properties['max_shield'] - self.properties['shield']
			newshield = self.properties['shield'] + self.properties['shield_recharge']
			#but what if shield damage is less than shield_recharge? charge up to max_shield
			if newshield > self.properties['max_shield']:
				newshield = self.properties['max_shield']

			self.properties.update({'shield':int(newshield)})

		# execute dots
		new_negative_effects = deepcopy(self.negative_effects)
		for key, turns_left in self.negative_effects.iteritems():
			if int(turns_left) > 0:
				self.take_damage(self.Roller.roll(int(self.PowerHandler.get_power_details(power_keys=[str(key)])[key]['dot_tick'])), source=key)
				new_negative_effects[key] = turns_left - 1
			else:
				#dot is over. remove it.
				new_negative_effects.pop(key, None)
		self.negative_effects = new_negative_effects

	# end new_turn

	def take_damage(self, amount, source=None):
		if amount <= self.properties['shield']:
			newshield = self.properties['shield'] - amount
			self.properties.update({'shield':int(newshield)})
			print str("You take " + str(amount) + " damage to shields (" + str(newshield) + " remaining) (" + str(source) + ")."
		else: #amount > self.properties['shield']:
			shielddamage = self.properties['shield']
			remainder = amount - shielddamage
			self.properties.update({'shield':0})

			# armor and dr
			if remainder - int((math.ceil(remainder * self.properties['damage_reduction']))) <= self.properties['armor']:
				armor_damage = remainder - int(math.ceil(remainder * self.properties['damage_reduction']))
				newarmor = self.properties['armor'] - armor_damage
				self.properties.update({'armor':int(newarmor)})
				print str("You takes " + str(armor_damage) + " damage to armor. (" + str(newarmor) + ") (" + str(source) + ")."
			else: #armor_damage > self.properties['armor']:
				armor_damage = self.properties['armor']
				remainder -= armor_damage
				self.properties.update({'armor':0})

				# health
				newhealth = self.properties['health'] - remainder
				self.properties.update({'health':int(newhealth)})


				print str("You take " + str(shielddamage) + " to shield (0 remaining) (" + str(source) + ")."
				print str("You take " + str(armor_damage) + " to armor (0 remaining) (" + str(source) + ")."
				print str("You take " + str(remainder) + " to health (" + str(newhealth) + " remaining) (" + str(source) + ")."

				if self.properties['health'] <= 0:
					#target dead
					print str("You are dead.")
					self.is_alive = False
	# end take_damage

	def resurrect(self):
		self.properties['health'] = 10
		self.is_alive = True
	# end resurrect

	def heal(self, health, armor, shield):
		if not self.is_alive:
			return
		
		self.properties['health'] += health
		self.properties['armor'] += armor
		self.properties['shield'] += shield

		if self.properties['health'] > self.properties['max_health']:
			self.properties['health'] = self.properties['max_health']
		if self.properties['armor'] > self.properties['max_armor']:
			self.properties['armor'] = self.properties['max_armor']
		if self.properties['shield'] > self.properties['max_shield']:
			self.properties['shield'] = self.properties['max_shield']
	# end heal

	def kill(self):
		if not self.is_alive:
			return

		self.properties['health'] = 0
		self.properties['armor'] = 0
		self.properties['shield'] = 0
		self.is_alive = False
	# end kill

	def get_cooldowns(self):
		return self.power_tracker
	def get_negative_effects(self):
		return self.negative_effects
	def get_tech_primed(self):
		return self.tech_primed
	def get_biotic_primed(self):
		return self.biotic_primed
	def get_health_shields(self):
		return self.properties['health'], self.properties['shield']

# end Character