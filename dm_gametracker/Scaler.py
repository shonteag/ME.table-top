'''
Scaler.py
This is a collection of methods that handle scaling of enemies based on level.
'''

import math
import random
from ClassHandler import ClassHandler
from PowerHandler import PowerHandler
from WeaponHandler import Weapon
import static

class Scaler(object):
	def __init__(self, class_handler=None, power_handler=None, weapon_handler=None):
		if class_handler == None:
			class_handler = ClassHandler()
		if power_handler == None:
			power_handler = PowerHandler()
		#if weapon_handler == None:
			#weapon_handler = WeaponHandler()

		self.ClassHandler = class_handler
		self.PowerHandler = power_handler
		#self.WeaponHandler = weapon_handler

	# end __init__

	'''roll_health()
	Rolls a characters health based on level and difficulty.
	'''
	def roll_health(self, level, difficulty, role, class_key, stats=None):
		if stats == None and (class_key != static.CLASS_NONE and class_key in static.CLASSES):
			stats = self.ClassHandler.get_class_details(class_key)['base_stats']
			class_modifier = self.ClassHandler.get_class_details(class_key)['con_modifier']
		else:
			stats = static.STATS_DEFAULT
			class_modifier = 0

		return ((8 + class_modifier + (stats['CON'] * difficulty) + stats['FIT']) * level)
	# end roll_health

	def roll_shield(self, level, difficulty, role, class_key, stats=None):
		return 0
	# end roll_shield

	def roll_weapon_damage(self, level, difficulty, role, class_key, type=None):
		# choose weapon type

		# pick damage based on weapon type

		return 0
	# end roll_weapon_damage

	def roll_stats(self, level, difficulty, role, class_key):
		base_stats = self.ClassHandler.get_class_details(class_key)['base_stats']

		#do stuff to stats here
		available_points = int(level)/int(4)

		return base_stats
	# end roll_stats