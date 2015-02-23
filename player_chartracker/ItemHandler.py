'''
ItemHandler.py
Used for custom items. Items can then be added to loot tables,
vendors and inventories of all types.

Item (object)
quality (color), Name, Value (credits per unit)
'''
import static
import os

class Item(object):
	def __init__(self, name=None, quality=None, value=None, img_src=None, description=None, gmdescription=None):
		if name == None:
			name = "Unamed Item"
		if quality == None or int(quality) not in static.QUALITIES_VALUES:
			quality = 1
		if value == None or int(value) < 0:
			value = 0

		self.name = name
		self.quality = quality
		self.value = value
		self.description = description
		self.gmdescription = gmdescription

		icon_path = 'res/icon/item/'+str(name)+'.gif'
		if not os.path.isfile(icon_path):
			icon_path = 'res/icon/item/base_' + str(quality) + '.gif'
		self.icon_path = icon_path
	# end __init__

	def update(self, name, quality, value, img_src, description, gmdescription):
		self.name = name
		self.quality = quality
		self.value = value
		self.description = description
		self.gmdescription = gmdescription

		icon_path = 'res/icon/item/'+str(name)+'.gif'
		if not os.path.isfile(icon_path):
			icon_path = 'res/icon/item/base_' + str(quality) + '.gif'
		self.icon_path = icon_path
	# end update
# end Item