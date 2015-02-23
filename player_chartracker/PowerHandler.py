'''
PowerHandler.py
PowerHandler handles loading of powers from power.xml
file and also can serve required data to calling methods.
All lookups are handled by an instance of this object.
'''

import xml.sax
from copy import deepcopy
import sys

class PowerXmlHandler(xml.sax.ContentHandler):
	def __init__(self):
		'''power_lookup is a dictionary that follows this format:
		{power_key:{power_name, cd}}
		'''
		self.power_lookup = {}
		
		self.power_key = ""
		self.power_inner_dic = {}

		self.CurrentData = ""
	# end __init__

	def startElement(self, tag, attributes):
		self.CurrentData = tag
		if tag == "power":
			# reset
			self.power_key = ""
			self.power_inner_dic ={}

			self.power_key = attributes['key']
			self.power_inner_dic.update({'power_name':str(attributes['name'])})
	# end startElement

	def endElement(self, tag):
		if tag == "power":
			self.power_lookup.update({str(self.power_key):deepcopy(self.power_inner_dic)})

		self.CurrentData = ""
	# end endElement

	def characters(self, content):
		if self.CurrentData == "power":
			pass
		else:
			self.power_inner_dic.update({str(self.CurrentData):str(content)})
	# end characters

	def get_detail_dictionary(self):
		return self.power_lookup
	# end get_detail_dictionary
# end PowerXmlHandler

class PowerHandler(object):
	def __init__(self):
		self.parser = xml.sax.make_parser()
		self.parser.setFeature(xml.sax.handler.feature_namespaces, 0)
		self.Handler = PowerXmlHandler()
		self.parser.setContentHandler(self.Handler)

		self.parser.parse('xml/power.xml')

		self.power_dictionary = self.Handler.get_detail_dictionary()
	# end __init__

	def print_power_details(self):
		for key, attribute_dic in self.power_dictionary.iteritems():
			print "Power: " + str(attribute_dic['power_name']) + " (" + str(key) + ")"
			for innerkey, innerval in attribute_dic.iteritems():
				print "  " + str(innerkey) + " : " + str(innerval)
	# end print_power_details

	def get_power_list(self, ptype=None):
		powers = []
		if ptype == None:
			for key in self.power_dictionary:
				powers.append(str(key))
		elif ptype == static.POWER_BIOTIC:
			for key in self.power_dictionary:
				if self.get_power_type(key) == static.POWER_BIOTIC:
					powers.append(key)
		elif ptype == static.POWER_TECH:
			for key in self.power_dictionary:
				if self.get_power_type(key) == static.POWER_TECH:
					powers.append(key)
		else:
			#whoops. no go here.
			pass
		return powers
	# end get_power_list

	'''Used externally to get details of certain powers. If none is
	specified, it will return the entire dictionary (all powers). Otherwise,
	power_keys MUST be a list [power_key, power_key, ...] and the
	method will return a dictionary containing keys for all entries
	in said list.
	'''
	def get_power_details(self, power_keys=None):
		if power_keys == None:
			return self.power_dictionary
		else:
			return_dictionary = {}
			for power_key in power_keys:
				try:
					return_dictionary.update({power_key:self.power_dictionary[str(power_key)]})
				except KeyError, error:
					print "ERROR: No power key defined " + str(power_key)
			return return_dictionary
	# end get_power_details

	'''This will return all powers of a specified type, either
	"biotic" or "tech". Can be access externally.
	'''
	def get_type_powers(self, power_type):
		power_type = power_type.lower()
		if (power_type != 'biotic') and (power_type != 'tech'):
			print "ERROR: power_type must be \'biotic\' or \'tech\'."
			raise Exception("key_error")
			return 0

		return_dictionary = {}

		for key, inner_dic in self.power_dictionary.iteritems():
			keysplit = key.split("_")
			if power_type in keysplit:
				return_dictionary.update({key:inner_dic})

		return return_dictionary
	# end get_type_powers

	def get_power_type(self, power_key):
		keysplit = power_key.split("_")
		return keysplit[0]
	#end get_type


	def roll_power_damage(self, power_key, level, difficulty):
		power_base_damage = self.get_power_details(power_keys=[power_key])[power_key]['damage']

		#do some rollls based on level and difficulty of mob <----------------------------------------- ROLL DAMAGE TO LEVEL!!!!!!!
		# NOTE: Player difficulty is always 2!

		return power_base_damage
	# end roll_power_damage
# end PowerHandler

if __name__ == "__main__":
	PowerHandler = PowerHandler()

	if "-print" in sys.argv:
		PowerHandler.print_power_details()

	if "-type" in sys.argv:
		type_powers = PowerHandler.get_type_powers(str(sys.argv[sys.argv.index('-type') + 1]))
		for key, inner_dic in type_powers.iteritems():
			print "Power: " + str(inner_dic['power_name'])