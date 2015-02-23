'''
RaidEncounter.py
Represents an encounter for a raid.
'''

from Enemy import Enemy
from Encounter import Encounter
from PowerHandler import PowerHandler
from ClassHandler import ClassHandler
import static
import random

class RaidEncounter(Encounter):
	def __init__(self, name=None, difficulty=None, description=None, is_boss=None):
		self.name = str(name)
		self.difficulty = int(difficulty)
		self.description = str(description)
		self.is_boss = bool(is_boss)

		super(RaidEncounter, self).__init__(level=20, difficulty=self.difficulty, description=self.description, is_boss=self.is_boss)

		self.enemies = []

		# triggers fire events. they are checked at the beginning of every new turn.
		# trigger types:
		# 'enemy_property'
		# DEFINITION 'enemy_property'
		#    KEYS: enemy_index, enemy_property_key, less_than (True, False=greater_than), enemy_property_threshold
		#		                ------------------  ------------------------------------  ------------------------
		#                       health              True ("less than")                    int
		#                       armor               False ("greater than")                int
		#                       shield                                                    int
		#
		# TRIGGERS ARE KEYED BY TRIGGER_NAME
		# {trigger_name: [trigger_type, {...KEYS...}, [event_name, event_name2, ...]]}
		self.triggers = {}


		# events are fired by triggers. one trigger can fire multiple events.
		# add event BEFORE trigger!!!
		# triggers are bound to raid bosses, events are bound to encounters
		# 
		# event types:
		# 'aoe', 'buff', 'heal', 'kill', 'resurrect', 'spawn'
		# DEFINITION 'aoe'
		#    KEYS: number_of_targets, damage_min, damage_max
		# DEFINITION 'buff'
		#    KEYS: target_index, duration, enemy_property_key, value_effect
		#                                  ------------------  ------------
		#                                  max_health          int
		#                                  max_armor           int
		#                                  damage_reduction    float (.01, .99)
		#                                  max_shield          int
		#                                  shield_recharge     int
		# DEFINITION 'heal'
		#    KEYS: target_index, shield_heal, armor_heal, health_heal
		# DEFINITION 'kill'
		#    KEYS: target_index
		# DEFINITION 'resurrect'
		#    KEYS: target_index
		# DEFINITION 'spawn'
		#    KEYS: target_index
		#
		# EVENTS KEYED BY EVENT_NAME
		# {event_name: [event_type, {...KEYS...}, cooldown]}
		self.events = {}
		self.cooldown_events = {}
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
		level = 20

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

		return new_enemy
	# end add_enemy

	def next_turn(self):
		for trigger_name, trigger_val in self.triggers.iteritems():
			if trigger_val[0] == 'enemy_property':
				if trigger_val[1]['less_than']:
					if self.enemies[int(trigger_val[1]['enemy_index'])].properties[trigger_val[1]['enemy_property_key']] <= trigger_val[1]['enemy_property_threshold']:
						self.fire_event(trigger_val[2]) #passes list of events to fire_event method
					else:
						pass #no event
				else: #'less_than' is actually greater than
					if self.enemies[int(trigger_val[1]['enemy_index'])].properties[trigger_val[1]['enemy_property_key']] >= trigger_val[1]['enemy_property_threshold']:
						self.fire_event(trigger_val[2])
					else:
						pass

		for enemy in self.enemies:
			enemy.new_turn()
			self.turn += 1

		# reduce event cooldowns
		events_cd_to_remove = []
		for event_name, event_cd in self.cooldown_events.iteritems():
			if int(event_cd)-1 <= 0:
				events_cd_to_remove.append(event_name)
			else:
				self.cooldown_events.update({event_name:event_cd-1})
		for event_name in events_cd_to_remove:
			del self.cooldown_events[event_name]

	# end next_turn

	def fire_event(self, event_names):
		for event_name in event_names:
			if event_name not in self.cooldown_events:
				event_val = self.events[event_name]
				print "TRIGGER FIRES EVENT: " + str(event_name)
				self.cooldown_events.update({str(event_name):int(event_val[2])})

				if event_val[0] == 'aoe':
					print "  --> AOE: " + str(random.randrange(event_val[1]['damage_min'], event_val[1]['damage_max'])) + " versus " + str(event_val[1]['number_of_targets'])

				elif event_val[0] == 'buff':
					print "not implemented yet"

				elif event_val[0] == 'heal':
					self.enemies[event_val[1]['target_index']].heal(event_val[1]['health_heal'], event_val[1]['armor_heal'], event_val[1]['shield_heal'])
					print "  --> Heal ("+ str(self.enemies[event_val[1]['target_index']].properties['name']) +"): H" + str(event_val[1]['health_heal']) + ", A" + str(event_val[1]['armor_heal']) + ", S" + str(event_val[1]['shield_heal'])

				elif event_val[0] == 'kill':
					self.enemies[event_val[1]['target_index']].kill()

				elif event_val[0] == 'resurrect':
					self.enemies[event_val[1]['target_index']].resurrect()

				elif event_val[0] == 'spawn':
					print "not implemented yet"

			else:
				pass #event on cooldown
	# end fire_event

	def add_event(self, event_name, event_val):
		self.events.update({str(event_name):list(event_val)})
	# end add_event

	def add_trigger(self, trigger_name, trigger_val):
		self.triggers.update({str(trigger_name):list(trigger_val)})
	# end add_trigger

if __name__ == '__main__':
	class_handler = ClassHandler()
	power_handler = PowerHandler()

	encounter = RaidEncounter(name="TestEncounter", difficulty=4, description="None", is_boss=True)
	enemy = encounter.add_enemy(name="Boss", class_key="SOL", race="human", role='tank', difficulty=4, max_health=400, max_armor=1000, max_shield=1000, damage_reduction=.3, shield_recharge=50, power_handler=power_handler, class_handler=class_handler)

	encounter.add_trigger("shield_too_low", ["enemy_property", {'enemy_index':0, 'enemy_property_key':'shield', 'less_than':True, 'enemy_property_threshold':1}, ['event_shield_overcharge', 'event_shield_deploy']])
	encounter.add_event("event_shield_overcharge", ['heal', {'target_index':0, 'health_heal':0, 'armor_heal':0, 'shield_heal':600}, 10])
	encounter.add_event("event_shield_deploy", ['aoe', {'number_of_targets':'ALL', 'damage_min':100, 'damage_max':300}, 5])

	while True:
		command = int(raw_input("Damage to take: "))
		enemy.take_damage(command)
		print enemy.properties['health'], enemy.properties['armor'], enemy.properties['shield']
		encounter.next_turn()