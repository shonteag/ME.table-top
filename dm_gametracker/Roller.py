'''
Roller.py
This is an object that handles random rolls.
'''

import random

class Roller(object):
	def __init__(self):
		pass
	# end __init__

	def roll(self, sides):
		return random.randrange(1,int(sides) + 1)
	# end roll
# end Roller