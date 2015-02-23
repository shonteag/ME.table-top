'''
ArmorHandler.py
This class is responsible for keeping track of an
armor item.
'''

import random
import os

class Armor(object):
	def __init__(self, w_type, w_type_name, w_man, w_man_name, w_key, w_name, w_quality, w_level,
		  		 shield, shield_recharge, damage_reduction, mod_slots, specials):
		self.max_shield = int(shield)
		self.shield_recharge = int(shield_recharge)
		self.damage_reduction = int(damage_reduction)

		self.type    = str(w_type)
		self.type_name = str(w_type_name)
		self.name    = str(w_name)
		self.man     = str(w_man)
		self.man_name= str(w_man_name)
		self.key     = str(w_key)
		self.level   = int(w_level)
		self.quality = int(w_quality)
		self.mod_slots = int(mod_slots)
		self.specials = specials

		icon_path = 'res/icon/gear/armor/' + str(w_type) + '/' + str(w_key) + '.gif'
		if not os.path.isfile(icon_path):
			icon_path = 'res/icon/gear/armor/' + str(w_type) + '/base_' + str(w_quality) + '.gif'
		self.icon_path = icon_path
	# end __init__

	def update(self, shield=None, shield_recharge=None, damage_reduction=None, mod_slots=None, specials=None):
		if shield != None:
			self.max_shield = shield
		if shield_recharge != None:
			self.shield_recharge = int(shield_recharge)
		if damage_reduction != None:
			self.damage_reduction = int(damage_reduction)
		if mod_slots != None:
			self.mod_slots = int(mod_slots)
		if specials != None:
			self.specials = specials
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
			   'max_shield':self.max_shield,
			   'shield_recharge':self.shield_recharge,
			   'damage_reduction':self.damage_reduction,
			   'mod_slots':self.mod_slots,
			   'specials':self.specials}

		return dic
	# end get_properties_as_dict
# end Armor