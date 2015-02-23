'''
Encounter.py
This object tracks and stores data on a specific encounter:
enemies (health, shields, powers, cooldowns, weapons, dots,
negative effects, primes, etc.)
'''

from Scaler import Scaler
from Enemy import Enemy
import static

class Encounter(object):

	def __init__(self, level=None, difficulty=None, enemies=None, name=None, description=None, is_boss=None):
		if difficulty == None:
			difficulty = 1
		self.difficulty = difficulty

		if enemies == None:
			self.enemies = []
		else:
			self.enemies = enemies

		self.num_enemies = len(self.enemies)

		self.state = static.INACTIVE

		self.name = name
		self.description = description
		self.level = level

		self.turn = 0

		if is_boss == None:
			is_boss = False
		self.is_boss = bool(is_boss)

		self.loot = None

		self.Scaler = Scaler()

		# special loot table
		# list of tuples [(item_id_number, %drop chance)]
		self.special_loot = []
		self.customs_only = False
	# end __init__

	def add_enemy(self,
				  name=None,
				  class_key=None,
				  race=None,
				  role=None,
				  level=None,
				  difficulty=None,
				  max_health=None,
				  max_armor=None,
				  max_shield=None,
				  health = None,
				  shield = None,
				  shield_recharge=None,
				  damage_reduction=None,
				  weapons=None,
				  powers=None,
				  description=None,
				  power_handler=None,
				  class_handler=None,
				  stats=None):
		# set defaults
		if level == None:
			level = self.level

		if difficulty == None:
			difficulty = self.difficulty

		if stats == None:
			stats = class_handler.get_class_details(class_key)['base_stats']

		if max_health == None:
			max_health = self.Scaler.roll_health(level, difficulty, role, class_key, stats=stats)

		if health == None:
			health = max_health
		if shield == None:
			shield = max_shield

		new_enemy = Enemy(name=name, class_key=class_key, race=race, role=role, level=level, difficulty=difficulty,
						  max_health=max_health, max_armor=max_armor, max_shield=max_shield, shield_recharge=shield_recharge, damage_reduction=damage_reduction,
						  weapons=weapons, powers=powers, description=description, power_handler=power_handler, class_handler=class_handler,
						  stats=stats)

		self.enemies.append(new_enemy)
		self.num_enemies += 1

		return new_enemy
	# end add_enemy

	def add_special(self, number, chance):
		self.special_loot = list(self.special_loot)
		self.special_loot.append([number, chance])

	def delete_special(self, index):
		self.special_loot.pop(index)

	def update(self, name, level, diff, description, is_boss, special_loot, customs_only):
		self.name = str(name)
		self.level = int(level)
		self.difficulty = int(diff)
		self.description = str(description)
		self.is_boss = bool(is_boss)
		self.customs_only = bool(customs_only)
	# end update

	def next_turn(self):
		for enemy in self.enemies:
			enemy.new_turn()
			self.turn += 1
	# end next_turn

	def get_state(self):
		return self.state
	def set_state(self, state):
		self.state = state

	def add_loot_table(self, loot_table):
		self.loot = loot_table

	def get_average_mob_level(self):
		level_add = 0
		for enemy in self.enemies:
			level_add += enemy.properties['level']
		return (float(level_add)/float(len(self.enemies)))

	def get_average_mob_difficulty(self):
		diff_add = 0
		for enemy in self.enemies:
			diff_add += enemy.properties['difficulty']
		return (float(diff_add) / float(len(self.enemies)))
	
# end Encounter


if __name__ == "__main__":
	class_handler = ClassHandler()
	power_handler = PowerHandler()

	name = str(raw_input("Name: "))
	class_key = str(raw_input("Class: "))
	role = str(raw_input("Role: "))
	level = int(raw_input("Level: "))
	difficulty = int(raw_input("Dif (1-4): "))
	max_health = int(raw_input("health: "))
	max_shield = int(raw_input("shield: "))
	recharge = int(raw_input("  recharge: "))
	powers = str(raw_input("powers (space separated): "))

	Encounter = Encounter(level)

	Encounter.add_enemy(name=name, class_key=class_key, role=role, level=level, difficulty=difficulty,
						max_health=max_health, max_shield=max_shield, shield_recharge=recharge, powers=powers.split(),
						damage_reduction=0)
