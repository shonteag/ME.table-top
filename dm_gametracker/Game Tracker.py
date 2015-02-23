# __main__.py
# exe launching

import gui
import Game
import Planet
import Area
import Store
import Mission
import Encounter
import Enemy
import ClassHandler
import WeaponHandler
import ArmorHandler
import PowerHandler
import ItemHandler
import SavegameHandler
import LootHandler
import FileServer
import static
import Scaler
import Roller


import Tkinter
import ScrolledText
import tkMessageBox
import tkFileDialog
import tkSimpleDialog
import ttk

import xml.etree.ElementTree
import xml.etree.cElementTree
import xml.sax
import random, os, sys
import math
from copy import deepcopy
import datetime
import string

import dill




def launch():
	# console log HEADER
	print " --------------------------------------------------------------------"
	print "| ME D&D Game Tracker                                                |"
	print "| This is the GM suite to be used in constructing and GM-ing a game. |"
	print "| Software Author: Shonte Amato-Grill                                |"
	print "| Game Authors: Joshua Szabo & Shonte Amato-Grill                    |"
	print "| Content Copyright Holders: BioWare and EA Corporation              |"
	print "|     This content is distributed as fan-made free-ware only. No     |"
	print "|     claim to ownership is made or inferred.                        |"
	print " --------------------------------------------------------------------"
	print "  NOTE: Closing this console window will terminate the Game Tracker!!"
	print "\n"

	root = Tkinter.Tk()
	root.withdraw()
	tracker = gui.GameTracker(root)


if __name__ == "__main__":
	launch()