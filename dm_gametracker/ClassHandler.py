

'''
Class.py
This contains classes and methods used for generating enemies.
-
ClassXmlHandler is used to load in all classes predifined in
the xml/class.xml file. This should never be accessed externally.
-
ClassHandler is used to manage all external calls. It handles classes
with default values. The external Enemy class can be modified to create
custom enemies.
'''

import xml.sax
from copy import deepcopy
import sys
import static

class ClassXmlHandler(xml.sax.ContentHandler):
	def __init__(self):
		self.class_lookup = {}

		self.CurrentData = ""

		self.class_key = ""
		# class details follows format:
		# [class_name, weapon_slots, tech_slots, biotic_slots, melee, con_modifier, [powers]]
		self.class_details = {}

		# this will hold all unlockable powers by power_key
		self.powers = []
		# power details can be looked up by checking the power handler class

		self.base_stats = {}

		self.stats = False
	# end __init__

	def startElement(self, tag, attributes):
		self.CurrentData = tag
		if tag == 'class':
			#print "Found class: " + str(attributes['name']) + " (" + str(attributes['key']) + ")"
			# reset
			self.class_details = {}
			self.class_key = ""
			self.powers = []
			self.base_stats = {}
			# key and name
			self.class_key = str(attributes['key'])
			self.class_details.update({'class_name':str(attributes['name'])})
		if tag == 'base_stats':
			self.stats = True
	# end startElement

	def endElement(self, tag):
		if tag == "powers":
			self.class_details.update({'powers':deepcopy(self.powers)})

		elif tag == 'base_stats':
			self.stats = False
			self.class_details.update({'base_stats':deepcopy(self.base_stats)})

		elif tag == 'class':
			self.class_lookup.update({str(self.class_key):deepcopy(self.class_details)})

		self.CurrentData = ""
	# end endElement

	def characters(self, content):
		if self.CurrentData == 'class':
			pass
		elif self.CurrentData == 'powers' or self.CurrentData == 'key':
			if self.CurrentData == 'key':
				self.powers.append(str(content))
			else:
				pass
		elif self.stats and self.CurrentData != 'base_stats':
			self.base_stats.update({str(self.CurrentData):content})
		else:
			self.class_details.update({str(self.CurrentData):str(content)})
	# end characters

	def get_detail_dictionary(self):
		return self.class_lookup
	# end get_detail_dictionary

#end ClassXmlHandler

class ClassHandler(object):
	def __init__(self):
		self.parser = xml.sax.make_parser()
		self.parser.setFeature(xml.sax.handler.feature_namespaces, 0)
		self.Handler = ClassXmlHandler()
		self.parser.setContentHandler(self.Handler)

		self.parser.parse('xml/class.xml')

		'''class_lookup is dictionary in following format:
		{class_key:{class_name, weap_slots, tech_slots, biotic_slots, melee, con_modifier, [powers]}}
		'''
		self.class_dictionary = self.Handler.get_detail_dictionary()
	# end __init__

	def print_class_details(self):
		for key, entry in self.class_dictionary.iteritems():
			print "CLASS: " + str(entry['class_name']) + " (" + str(key) + ")"
			for inkey, inval in entry.iteritems():
				if inkey != "powers":
					print "   " + str(inkey) + ": " + str(inval)
				else:
					print "   Unlockable Powers:"
					for power in inval:
						print "     " + str(power)
	# end print_class_details

	def get_class_details(self, class_key=None):
		if class_key == None:
			return self.class_dictionary
		elif class_key == static.CLASS_NONE:
			return
		else:
			try:
				return self.class_dictionary[str(class_key)]
			except KeyError, error:
				print "ERROR: No class key defined (" + str(class_key) + ")"
	# end get_class_details
#end ClassHanlder


if __name__ == "__main__":
	ClassHandler = ClassHandler()

	if "-print" in sys.argv:
		ClassHandler.print_class_details()

	if '-details' in sys.argv:
		class_key = sys.argv[int(sys.argv.index('-details') + 1)]
		class_info = ClassHandler.get_class_details(str(class_key))