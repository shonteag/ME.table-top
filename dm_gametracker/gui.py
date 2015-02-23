'''
gui.py
Graphical User Interface for interacting with uderlying classes.
'''

import Tkinter as tk
import ScrolledText as st
import tkMessageBox as tkmb
import tkFileDialog as tkfd
import tkSimpleDialog as tksd
import ttk

from tkinterext.tkStatusBar import StatusBar

import subprocess

import datetime
import string
import math

from Scaler import Scaler
from PowerHandler import PowerHandler
from ClassHandler import ClassHandler
from WeaponHandler import Weapon
from ArmorHandler import Armor
from LootHandler import LootHandler
from ItemHandler import Item
from Game import Game
from Mission import Mission
from Encounter import Encounter
from Enemy import Enemy
import SavegameHandler
import static

import FileServer


'''
Small dialog box to ask for the name of the new game
'''
class NewGameInfo(tksd.Dialog):
	def body(self, master):
		tk.Label(master, text="Name:").grid(row=0, column=0)
		self.e_name = tk.Entry(master)
		self.e_name.grid(row=0, column=1)
		return self.e_name
	def apply(self):
		self.result = str(self.e_name.get())

'''
Small dialog wizard for new Mission NewGameInfo
'''
class NewMissionInfo(tksd.Dialog):
	def body(self, master):
		# name
		tk.Label(master, text="Name:").grid(row=0,column=0,sticky=tk.W)
		self.e_name = tk.Entry(master)
		self.e_name.grid(row=0,column=1)

		# level
		tk.Label(master, text="Level:").grid(row=1,column=0,sticky=tk.W)
		self.e_level = tk.Entry(master)
		self.e_level.grid(row=1,column=1)
		tk.Label(master, text="(1-20)").grid(row=1,column=2,sticky=tk.W)

		# difficulty
		tk.Label(master, text="Difficulty:").grid(row=2,column=0,sticky=tk.W)
		self.e_dif = tk.Entry(master)
		self.e_dif.grid(row=2, column=1)
		tk.Label(master, text="(1-4, 2 is average)").grid(row=2, column=2,sticky=tk.W)
	def apply(self):
		self.name = str(self.e_name.get())
		self.level = int(self.e_level.get())
		self.difficulty = int(self.e_dif.get())


'''
Small dialog wizard for new Encounter info
'''
class NewEncounterInfo(tksd.Dialog):
	def body(self, master):
		# name
		tk.Label(master, text="Name:").grid(row=0, column=0, sticky=tk.W)
		self.e_name = tk.Entry(master)
		self.e_name.grid(row=0, column=1)
	def apply(self):
		self.name = str(self.e_name.get())


'''
Small dialog wizard for new enemy info
'''
class NewEnemyInfo(tksd.Dialog):
	def body(self, master):
		# name
		tk.Label(master, text="Name:").grid(row=0,column=0,sticky=tk.W)
		self.e_name = tk.Entry(master)
		self.e_name.grid(row=0,column=1)

	def apply(self):
		self.name = str(self.e_name.get())


'''
Small dialog wizard for creating a new weapon
'''
class NewWeaponInfo(tksd.Dialog):
	def body(self, master):
		tk.Label(master, text="Quality:", bg='white', fg='black').grid(row=0, column=0, sticky=tk.W)
		self.v_qual = tk.StringVar()
		self.v_qual.set(static.QUALITIES_VALUES[1])
		op_qual = apply(ttk.OptionMenu, (master, self.v_qual) + tuple(static.QUALITIES_VALUES))
		op_qual.grid(row=0, column=1, sticky='ew')

		tk.Label(master, text="Type:", bg='white', fg='black').grid(row=1, column=0, sticky=tk.W)
		self.v_type = tk.StringVar()
		self.v_type.set(static.WEAPON_TYPES[1])
		op_type = apply(ttk.OptionMenu, (master, self.v_type) + tuple(static.WEAPON_TYPES))
		op_type.grid(row=1, column=1, sticky='ew')

		tk.Label(master, text="Shots Per Turn:").grid(row=2, column=0, sticky=tk.W)
		self.e_speed = tk.Entry(master)
		self.e_speed.grid(row=2, column=1, sticky='ew')

		tk.Label(master, text="Damage per Shot:").grid(row=3, column=0, sticky=tk.W)
		self.e_damage = tk.Entry(master)
		self.e_damage.grid(row=3, column=1, sticky='ew')

		tk.Label(master, text="crit_chance:").grid(row=4, column=0, sticky=tk.W)
		self.e_crit_chance = tk.Entry(master)
		self.e_crit_chance.grid(row=4, column=1, sticky='ew')

		tk.Label(master, text="crit_multiplier:").grid(row=5, column=0, sticky=tk.W)
		self.e_crit_multiplier = tk.Entry(master)
		self.e_crit_multiplier.grid(row=5, column=1, sticky='ew')

		tk.Label(master, text="mod_slots:").grid(row=6, column=0, sticky=tk.W)
		self.e_mods = tk.Entry(master)
		self.e_mods.grid(row=6, column=1, sticky='ew')
	def apply(self):
		self.qual = int(self.v_qual.get())
		self.type = str(self.v_type.get())
		self.speed = int(self.e_speed.get())
		self.damage = int(self.e_damage.get())
		self.crit = int(self.e_crit_chance.get())
		self.critm = float(self.e_crit_multiplier.get())
		self.mod_slots = int(self.e_mods.get())


class NewLootTableInfo(tksd.Dialog):
	def body(self, master):
		tk.Label(master, text="Average player level:").grid(row=0, column=0, sticky=tk.W)
		self.op_avg_level = tk.Entry(master)
		self.op_avg_level.grid(row=0, column=1, sticky='ew')

		tk.Label(master, text="Number of players:").grid(row=1, column=0, sticky=tk.W)
		self.op_num_players = tk.Entry(master)
		self.op_num_players.grid(row=1, column=1, sticky='ew')
	def apply(self):
		self.avg_level = int(self.op_avg_level.get())
		self.num_players = int(self.op_num_players.get())


class NewChestLootInfo(tksd.Dialog):
	def body(self, master):
		tk.Label(master, text='Chest Items Level:').grid(row=0, column=0, sticky=tk.W)
		self.e_level = tk.Entry(master)
		self.e_level.grid(row=0, column=1, sticky='ew')

		tk.Label(master, text='Guaranteed Quality:').grid(row=1, column=0, sticky=tk.W)
		self.e_gquality = tk.Entry(master)
		self.e_gquality.grid(row=1, column=1, sticky='ew')
		tk.Label(master, text='(0-4) or blank').grid(row=1, column=2, sticky=tk.E)

		tk.Label(master, text='Chest quality roll type:').grid(row=2, column=0, columnspan=2, sticky=tk.W)
		self.v_type = tk.StringVar()
		self.v_type.set(str(None))
		self.e_type = apply(ttk.OptionMenu, (master, self.v_type) + tuple(static.chest_types))
		self.e_type.grid(row=3, column=0, sticky='ew', columnspan=2)

		tk.Label(master, text='Gear Type:').grid(row=4, column=0, sticky=tk.W)
		self.v_gtype = tk.StringVar()
		self.v_gtype.set(str(None))
		self.e_type = apply(ttk.OptionMenu, (master, self.v_gtype) + tuple(['', 'None', 'armor', 'weapon']))
		self.e_type.grid(row=4, column=1, sticky='ew')

		tk.Label(master, text='Number of pieces:').grid(row=5, column=0, sticky=tk.W)
		self.e_num = tk.Entry(master)
		self.e_num.grid(row=5, column=1, sticky='ew')

		tk.Label(master, text='Contains Credits?').grid(row=6, column=0, sticky=tk.W)
		self.v_credits = tk.BooleanVar()
		self.v_credits.set(False)
		self.c_credits = ttk.Checkbutton(master, variable=self.v_credits, onvalue=True, offvalue=False)
		self.c_credits.grid(row=6, column=1, sticky=tk.W)
	def apply(self):
		self.level = int(self.e_level.get())
		if self.e_gquality.get() == "":
			self.e_gquality = None
		else:
			self.e_gquality = int(self.e_gquality.get())
		self.chest_type = str(self.v_type.get())
		self.gear_type = str(self.v_gtype.get())
		self.num_pieces = int(self.e_num.get())
		self.contains_credits = bool(self.v_credits.get())


class LootTableViewer(tk.Toplevel):
	def __init__(self, master, encounter, LootHandler, loot_table=None):
		tk.Toplevel.__init__(self, master)

		if encounter != None:
			self.title("Loot table viewer: " + str(encounter.name))
		else:
			self.title("Loot table viewer: CHEST")

		self.LootHandler = LootHandler

		if loot_table == None:
			self.loot_table = encounter.loot
		else:
			self.loot_table = loot_table

		w,h = self.winfo_screenwidth(), self.winfo_screenheight()
		self.geometry("%dx%d+0+0" % (w,h))

		#loot frame
		self.f_loot = tk.Frame(self, bg='black')
		self.f_loot.pack(fill=tk.BOTH, expand=1, side=tk.TOP)
		self.f_loot.grid_propagate(False)

		self.grid_width = w / 275

		self.f_control = tk.Frame(self, bg='black', height=100)
		self.f_control.pack(fill=tk.X, side=tk.BOTTOM, expand=0)

		if loot_table == None and encounter != None:
			ttk.Button(self.f_control, text='Reroll Loot', command=lambda: self._do_loot_roll(master, encounter)).pack(side=tk.LEFT)
		
		#ttk.Button(self.f_control, text='Generate Loot String', command=lambda: self._gen_string(master, encounter)).pack(side=tk.LEFT)

		#ttk.Button(self.f_control, text='Exit Loot Viewer').pack(side=tk.RIGHT)

		# MENU
		m_menubar = tk.Menu(self)
		self.config(menu=m_menubar)

		# Push to server
		m_websocket = tk.Menu(m_menubar, tearoff=0)
		m_menubar.add_cascade(label='WebSocket', menu=m_websocket)
		m_websocket.add_cascade(label="Push", command=lambda: self._do_loot_push(master))

		self._draw_loot_window()

	def _do_loot_push(self, master):
		FileServer.generate_loot_file(self.loot_table)
		print "Loot push complete."

	def _do_loot_roll(self, master, encounter):
		getter = NewLootTableInfo(master)
		encounter.add_loot_table(self.LootHandler.roll_encounter_loot(game, encounter, getter.avg_level, getter.num_players))
		self._draw_loot_window()

	def _draw_loot_window(self):
		loot_frames = []
		loot_images = []
		loot_text = []

		try:
			self.f_loot.destroy()
		except:
			pass

		self.f_loot = tk.Frame(self, bg='black')
		self.f_loot.pack(fill=tk.BOTH, expand=1, side=tk.TOP)
		self.f_loot.grid_propagate(False)

		for index, loot_piece in enumerate(self.loot_table[1]):
			f_loot_piece = tk.Frame(self.f_loot, bd=2, relief=tk.RAISED, bg='black', width=275, height=200)
			f_loot_piece.grid(row=(index / self.grid_width), column=(index % self.grid_width), sticky='ew', padx=2, pady=2)
			f_loot_piece.grid_propagate(False)

			loot_frames.append(f_loot_piece)

			#image first
			loot_icon = tk.PhotoImage(file=loot_piece.icon_path)
			loot_images.append(loot_icon)
			image_label = tk.Label(loot_frames[index], image=loot_icon)
			image_label.image = loot_images[index]
			image_label.grid(row=0, column=0, rowspan=5)

			if isinstance(loot_piece, Weapon) or isinstance(loot_piece, Armor):
				# name
				tk.Label(loot_frames[index], text=(loot_piece.name + " " + loot_piece.type_name + " (" + str(loot_piece.level) + ")"), bg='black', fg=static.QUALITIES_COLOR[int(loot_piece.quality) + 1]).grid(row=0, column=1, columnspan=3)
				# manufac
				tk.Label(loot_frames[index], text=loot_piece.man_name, bg='black', fg='white').grid(row=1, column=1, columnspan=3, sticky=tk.W)
				# stats
				if isinstance(loot_piece, Weapon):
					# this is a weapon
					# damage and speed
					tk.Label(loot_frames[index], text="Speed/Damage:", bg='black', fg='white').grid(row=2, column=1, sticky=tk.W)
					tk.Label(loot_frames[index], text=(str(loot_piece.shots_per_round)), bg='black', fg=static.QUALITIES_COLOR[int(loot_piece.quality) + 1]).grid(row=2, column=2, sticky=tk.W)
					tk.Label(loot_frames[index], text='D'+str(loot_piece.damage_per_shot), bg='black', fg=static.QUALITIES_COLOR[int(loot_piece.quality) + 1]).grid(row=2, column=3, sticky=tk.W)
					# crit and mult
					tk.Label(loot_frames[index], text="Crit Roll:", bg='black', fg='white').grid(row=3, column=1, sticky=tk.W)
					tk.Label(loot_frames[index], text=str(loot_piece.crit_chance), bg='black', fg=static.QUALITIES_COLOR[int(loot_piece.quality) + 1]).grid(row=3, column=2, sticky=tk.W)
					tk.Label(loot_frames[index], text=str(loot_piece.crit_multiplier), bg='black', fg=static.QUALITIES_COLOR[int(loot_piece.quality) + 1]).grid(row=3, column=3, sticky=tk.W)

					#modslots
					tk.Label(loot_frames[index], text="Mod slots:", bg='black', fg='white').grid(row=4, column=1, sticky=tk.W)
					tk.Label(loot_frames[index], text=str(loot_piece.mod_slots), bg='black', fg=static.QUALITIES_COLOR[int(loot_piece.quality) + 1]).grid(row=4, column=2, sticky=tk.W)

					#special
					t_special = st.ScrolledText(loot_frames[index], bg='black', fg='yellow', bd=0, wrap=tk.WORD, width=30, height=5)
					loot_text.append(t_special)
					loot_text[index].grid(row=5, column=0, columnspan=5, sticky='ew', padx=1)

					# mod types
					if loot_piece.mod_types != None:
						for i,mod_type in enumerate(loot_piece.mod_types):
							loot_text[index].insert(tk.END, "Modable " + str(mod_type) + "\n")
						loot_text[index].insert(tk.END, "\n")

					# rolls
					if loot_piece.rolls != None:
						for i,roll in enumerate(loot_piece.rolls):
							loot_text[index].insert(tk.END, str(roll) + "\n")
						loot_text[index].insert(tk.END, "\n")

					# flavor text
					if loot_piece.specials != "" and loot_piece.specials != None:
						loot_text[index].insert(tk.END, str(loot_piece.specials))
					
					t_special.config(state=tk.DISABLED)

				elif isinstance(loot_piece, Armor):
					# this is armor
					# shield/sr
					tk.Label(loot_frames[index], text="Shield/SR:", bg='black', fg='white').grid(row=2, column=1, sticky=tk.W)
					tk.Label(loot_frames[index], text=(str(loot_piece.max_shield)), bg='black', fg=static.QUALITIES_COLOR[int(loot_piece.quality) + 1]).grid(row=2, column=2, sticky=tk.W)
					tk.Label(loot_frames[index], text=str(loot_piece.shield_recharge), bg='black', fg=static.QUALITIES_COLOR[int(loot_piece.quality) + 1]).grid(row=2, column=3, sticky=tk.W)
					# DR
					tk.Label(loot_frames[index], text="DR:", bg='black', fg='white').grid(row=3, column=1, sticky=tk.W)
					tk.Label(loot_frames[index], text=str(loot_piece.damage_reduction), bg='black', fg=static.QUALITIES_COLOR[int(loot_piece.quality) + 1]).grid(row=3, column=2, sticky=tk.W)
					# modslots
					tk.Label(loot_frames[index], text='Mod Slots:', bg='black', fg='white').grid(row=4, column=1, sticky=tk.W)
					tk.Label(loot_frames[index], text=str(loot_piece.mod_slots), bg='black', fg=static.QUALITIES_COLOR[int(loot_piece.quality) + 1]).grid(row=4, column=2, sticky=tk.W)

					#special
					if loot_piece.specials != "" and loot_piece.specials != None:
						t_special = tk.Text(loot_frames[index], bg='black', fg='yellow', bd=0, wrap=tk.WORD, width=30)
						t_special.grid(row=5, column=0, columnspan=5, sticky='ew', padx=1)
						t_special.insert(tk.END, str(loot_piece.specials))
						t_special.config(state=tk.DISABLED)

			elif isinstance(loot_piece, Item):
				# this is a custom armor
				# name
				tk.Label(loot_frames[index], text=loot_piece.name, bg='black', fg=static.QUALITIES_COLOR[int(loot_piece.quality) + 1]).grid(row=0, column=1, columnspan=3)
				# value
				tk.Label(loot_frames[index], text=loot_piece.value, bg='black', fg=static.QUALITIES_COLOR[int(loot_piece.quality) + 1]).grid(row=1, column=1, columnspan=2, sticky=tk.W)
				tk.Label(loot_frames[index], text='Credits', bg='black', fg='white').grid(row=1, column=3, sticky=tk.E)

				t_description = tk.Text(loot_frames[index], bg='black', fg='yellow', bd=0, wrap=tk.WORD, width=30)
				t_description.grid(row=5, column=0, columnspan=5, sticky='ew', padx=1)
				t_description.insert(tk.END, str(loot_piece.description))
				t_description.config(state=tk.DISABLED)

			else:
				#done fucked up. there isnt anything here.
				tkmb.showerror("Error", "The loot table has encountered an unknown piece of loot.\n\n" \
							   + "INTERNAL ERROR: loot_piece is not of instance Armor or Weapon")

		#credits
		f_credits = tk.Frame(self.f_loot, bd=2, relief=tk.RAISED, bg='black', width=275, height=110)
		f_credits.grid(row=(len(self.loot_table[1]) / self.grid_width), column=(len(self.loot_table[1]) % self.grid_width), sticky='ew', padx=2, pady=2)
		f_credits.grid_propagate(False)
		credits_icon = tk.PhotoImage(file='res/icon/credits.gif')
		l_icon = tk.Label(f_credits, image=credits_icon)
		l_icon.image = credits_icon
		l_icon.grid(row=0, column=0, rowspan=5, padx=1)

		tk.Label(f_credits, text='Credits', bg='black', fg='white').grid(row=0, column=1, columnspan=3)
		tk.Label(f_credits, text=str(self.loot_table[0]), bg='black', fg='white').grid(row=1, column=1, sticky=tk.W, padx=1)

	def _gen_string(self, master, encounter):
		pass
# end class LootTableViewer


'''
Small dialog wizard for incoming damage to an enemy.
'''
class TakeDamageInfo(tksd.Dialog):
	def body(self, master):
		tk.Label(master, text="Raw Damage:").grid(row=0, column=0)
		self.e_damage = tk.Entry(master)
		self.e_damage.grid(row=0, column=1)
	def apply(self):
		self.damage = int(self.e_damage.get())

'''
Small dialog wizard for healing
'''
class HealInfo(tksd.Dialog):
	def body(self, master):
		tk.Label(master, text='+ Health:').grid(row=0, column=0)
		self.e_health = tk.Entry(master)
		self.e_health.insert(0, '0')
		self.e_health.grid(row=0, column=1)

		tk.Label(master, text='+ Armor:').grid(row=1, column=0)
		self.e_armor = tk.Entry(master)
		self.e_armor.insert(0, '0')
		self.e_armor.grid(row=1, column=1)

		tk.Label(master, text='+ Shield:').grid(row=2, column=0)
		self.e_shield = tk.Entry(master)
		self.e_shield.insert(0, '0')
		self.e_shield.grid(row=2, column=1)
	def apply(self):
		self.health = int(self.e_health.get())
		self.armor = int(self.e_armor.get())
		self.shield = int(self.e_shield.get())

'''
Small dialog for power selection
'''
class PowerSelector(tksd.Dialog):
	def body(self, master):
		self.PowerHandler = PowerHandler()

		self.l_powers = tk.Listbox(master, selectmode=tk.BROWSE)
		self.l_powers.grid(row=0, column=0, sticky='ew')

		for power_key in self.PowerHandler.power_dictionary:
			self.l_powers.insert(tk.END, str(power_key))
	def apply(self):
		self.power_key = self.l_powers.get(tk.ACTIVE)
		print self.power_key

'''
This is the Combat tracker window. Does cool shit. Like track combat.
'''
class CombatTracker(tk.Toplevel):
	def __init__(self, master, encounter):
		tk.Toplevel.__init__(self, master)
		self.title("Combat Tracker: " + str(encounter.name))

		self.w, self.h = self.winfo_screenwidth(), self.winfo_screenheight()
		self.h -= 20
		self.geometry("%dx%d+0+0" % (self.w, self.h))

		self.f_main = tk.Frame(self, bg='black')
		self.f_main.pack(fill=tk.BOTH, expand=0)
		self.f_main.pack_propagate(False)

		# toolbar
		self.f_toolbar = tk.Frame(self, bg='white', height=40)
		self.f_toolbar.pack(side=tk.BOTTOM, fill=tk.X)
		self.f_toolbar.pack_propagate(False)

		self.PowerHandler = PowerHandler()
		self.ClassHandler = ClassHandler()

		# MENU
		m_menubar = tk.Menu(self)
		self.config(menu=m_menubar)

		# Push to server
		m_websocket = tk.Menu(m_menubar, tearoff=0)
		m_menubar.add_cascade(label='WebSocket', menu=m_websocket)
		m_websocket.add_cascade(label="Push", command=lambda: self._do_encounter_push(master))

		self._draw_combat(master, encounter)

	def _draw_combat(self, master, encounter):
		#pages
		frame_width = self.w
		frame_height = self.h

		self.number_of_columns = (frame_width / 400)
		self.number_of_rows = (frame_height / 500)

		self.number_enemies_per_page = self.number_of_rows * self.number_of_columns
		self.number_of_pages = len(encounter.enemies) / self.number_enemies_per_page
		if (len(encounter.enemies) % self.number_enemies_per_page) > 0:
			self.number_of_pages += 1

		self.current_page = 0
		self._draw_page(master, encounter, page_index=0)

		last_button = ttk.Button(self.f_toolbar, text='<<', command=lambda: last_page(master, encounter, int(self.current_page-1)))
		next_button = ttk.Button(self.f_toolbar, text='>>', command=lambda: next_page(master, encounter, int(self.current_page+1)))

		next_turn_button = ttk.Button(self.f_toolbar, text='Next Turn', command=lambda: next_turn(master, encounter, 0))
		next_turn_button.pack(anchor=tk.CENTER, side=tk.TOP)

		last_button.pack(side=tk.LEFT)
		next_button.pack(side=tk.LEFT)

		def last_page(master, encounter, page_index):
			if page_index < 0:
				tkmb.showerror("IndexError", "No previous page.")
				return
			self.current_page = page_index
			self._draw_page(master, encounter, page_index=page_index)
		def next_page(master, encounter, page_index):
			if page_index >= self.number_of_pages:
				tkmb.showerror("IndexError", "No next page.")
				return
			self.current_page = page_index
			self._draw_page(master, encounter, page_index=page_index)

		def next_turn(master, encounter, page_index):
			encounter.next_turn()
			self._draw_page(master, encounter, page_index=0)
		# end next_turn

	def _draw_page(self, master, encounter, page_index=0):
		try:
			self.f_main.destroy()
		except:
			pass

		# push to FileServer
		FileServer.generate_encounter_files(encounter)

		self.f_main = tk.Frame(self, bg='black')
		self.f_main.pack(fill=tk.BOTH, expand=0)

		start_index = self.number_enemies_per_page * page_index
		end_index = (self.number_enemies_per_page * (page_index + 1))

		enemy_frame_list = []
		enemy_power_boxes = []
		enemy_effects_boxes = []

		for index in range(0, end_index-start_index):
			if ((self.number_enemies_per_page*page_index) + index) >= len(encounter.enemies):
				break

			enemy = encounter.enemies[index + start_index]

			f_enemy = tk.Frame(self.f_main, bg='black', bd=1, relief=tk.RAISED, height=500, width=400)
			enemy_frame_list.append(f_enemy)
			enemy_frame_list[index].grid_propagate(False)
			enemy_frame_list[index].grid(row=(index/self.number_of_columns), column=(index%self.number_of_columns), sticky='ew')

			color = str(static.DIFFICULTY_COLORS[int(enemy.properties['difficulty']) - 1])
			if enemy.is_alive:
				name_color = 'white'
			else:
				name_color = 'red'

			# name and difficulty and level
			tk.Label(enemy_frame_list[index], text=enemy.properties['name'], bg='black', fg=name_color).grid(row=0, column=0, columnspan=2)
			tk.Label(enemy_frame_list[index], text="Level "+str(enemy.properties['level'])+" "+str(enemy.properties['class_key']), bg='black', fg=color).grid(row=0, column=2, columnspan=1, sticky=tk.E)
			tk.Label(enemy_frame_list[index], text=str(static.DIFFICULTY_NAMES[int(enemy.properties['difficulty']) - 1])+" "+str(enemy.properties['role']), bg='black', fg=color).grid(row=0, column=3, columnspan=2, sticky=tk.W)
			tk.Label(enemy_frame_list[index], text=str(enemy.properties['class_key']))

			# max_shield / shield recharge / DR
			ttk.Separator(enemy_frame_list[index], orient=tk.HORIZONTAL).grid(row=1, column=0, columnspan=6, sticky='ew')
			tk.Label(enemy_frame_list[index], text='MAX SHIELD', bg='black', fg='white').grid(row=2, column=0, sticky=tk.E)
			tk.Label(enemy_frame_list[index], text='MAX ARMOR', bg='black', fg='white').grid(row=2, column=1, sticky=tk.E)
			tk.Label(enemy_frame_list[index], text='MAX HEALTH', bg='black', fg='white').grid(row=2, column=2, sticky=tk.E)

			tk.Label(enemy_frame_list[index], text=str(enemy.properties['max_shield']), bg='black', fg='blue').grid(row=3, column=0, sticky=tk.E)
			tk.Label(enemy_frame_list[index], text=str(enemy.properties['max_armor']), bg='black', fg='yellow').grid(row=3, column=1, sticky=tk.E)
			tk.Label(enemy_frame_list[index], text=str(enemy.properties['max_health']), bg='black', fg='red').grid(row=3, column=2, sticky=tk.E)

			tk.Label(enemy_frame_list[index], text='Damage Reduction:', bg='black', fg='white').grid(row=4, column=0, columnspan=2, sticky=tk.W)
			tk.Label(enemy_frame_list[index], text=str(enemy.properties['damage_reduction'] * 100) + "%", bg='black', fg='yellow').grid(row=4, column=2, sticky=tk.W)

			tk.Label(enemy_frame_list[index], text='Shield Recharge:', bg='black', fg='white').grid(row=5, column=0, columnspan=2, sticky=tk.W)
			tk.Label(enemy_frame_list[index], text=str(enemy.properties['shield_recharge']), bg='black', fg='blue').grid(row=5, column=2, sticky=tk.W)

			#current HL / SH
			ttk.Separator(enemy_frame_list[index], orient=tk.HORIZONTAL).grid(row=6, column=0, columnspan=6, sticky='ew')
			tk.Label(enemy_frame_list[index], text='HEALTH', bg='black', fg='white').grid(row=6, column=0, sticky=tk.E)
			tk.Label(enemy_frame_list[index], text='ARMOR', bg='black', fg='white').grid(row=6, column=1, sticky=tk.E)
			tk.Label(enemy_frame_list[index], text='SHIELD', bg='black', fg='white').grid(row=6, column=2, sticky=tk.E)

			tk.Label(enemy_frame_list[index], text=str(enemy.properties['health']), bg='black', fg='red').grid(row=7, column=0, sticky=tk.E)
			tk.Label(enemy_frame_list[index], text=str(enemy.properties['armor']), bg='black', fg='yellow').grid(row=7, column=1, sticky=tk.E)
			tk.Label(enemy_frame_list[index], text=str(enemy.properties['shield']), bg='black', fg='blue').grid(row=7, column=2, sticky=tk.E)

			#     bars
			shield_width = 0
			armor_width = 0
			health_width = 0
			if enemy.properties['max_shield'] > 0:
				shield_width = math.floor(float(enemy.properties['shield']) / float(enemy.properties['max_shield']) * 400)
			if enemy.properties['max_armor'] > 0:
				armor_width = math.floor(float(enemy.properties['armor']) / float(enemy.properties['max_armor']) * 400)
			if enemy.properties['max_health'] > 0:
				health_width = math.floor(float(enemy.properties['health']) / float(enemy.properties['max_health']) * 400)

			tk.Frame(enemy_frame_list[index], bg='blue', height=10, width=int(shield_width)).grid(row=8, column=0, columnspan=6, sticky=tk.W)
			tk.Frame(enemy_frame_list[index], bg='yellow', height=10, width=int(armor_width)).grid(row=9, column=0, columnspan=6, sticky=tk.W)
			tk.Frame(enemy_frame_list[index], bg='red', height=10, width=int(health_width)).grid(row=10, column=0, columnspan=6, sticky=tk.W)

			# primes
			ttk.Separator(enemy_frame_list[index], orient=tk.HORIZONTAL).grid(row=11, column=0, columnspan=6, sticky='ew')
			tk.Label(enemy_frame_list[index], text='TECH PRIME', bg='black', fg='white').grid(row=11, column=0, sticky=tk.E)
			tk.Label(enemy_frame_list[index], text='BIOTIC PRIME', bg='black', fg='white').grid(row=11, column=1, sticky=tk.E)
			tk.Label(enemy_frame_list[index], text=str(enemy.get_tech_primed()), bg='black', fg='white').grid(row=12, column=0, sticky=tk.E)
			tk.Label(enemy_frame_list[index], text=str(enemy.get_biotic_primed()), bg='black', fg='white').grid(row=12, column=1, sticky=tk.E)

			# powers
			ttk.Separator(enemy_frame_list[index], orient=tk.HORIZONTAL).grid(row=13, column=0, columnspan=6, sticky='ew')
			l_available_powers = tk.Listbox(enemy_frame_list[index], selectmode=tk.BROWSE, height=7, bg='black', fg='white')
			enemy_power_boxes.append(l_available_powers)
			enemy_power_boxes[index].grid(row=14, column=0, columnspan=4, rowspan=4, sticky='ew')

			for key, cd in enemy.power_tracker.iteritems():
				enemy_power_boxes[index].insert(tk.END, str(key)+ ", CD: " + str(cd))

			#power buttons
			ttk.Button(enemy_frame_list[index], text='Use Power', command=lambda index=index, page_index=page_index, enemy=enemy: use_power(master, encounter, page_index, enemy, enemy_power_boxes[index])).grid(row=14, column=4, columnspan=2, sticky='ew')
			ttk.Button(enemy_frame_list[index], text='Reset CD', command=lambda index=index, page_index=page_index, enemy=enemy: reset_cd(master, encounter, page_index, enemy, enemy_power_boxes[index])).grid(row=15, column=4, columnspan=2, sticky='ew')

			#negative effects
			l_negative_effects = tk.Listbox(enemy_frame_list[index], selectmode=tk.BROWSE, height=7, bg='black', fg='white')
			enemy_effects_boxes.append(l_negative_effects)
			enemy_effects_boxes[index].grid(row=19, column=0, columnspan=4, rowspan=4, sticky='ew')

			for key, duration in enemy.negative_effects.iteritems():
				enemy_effects_boxes[index].insert(tk.END, str(key) + ", duration: " + str(duration))


			#effects buttons
			ttk.Button(enemy_frame_list[index], text='Remove', command=lambda index=index, page_index=page_index, enemy=enemy: remove_effect(master, encounter, page_index, enemy, enemy_effects_boxes[index])).grid(row=19, column=4, columnspan=2, sticky='ew')


			#buttons
			ttk.Button(enemy_frame_list[index], text='Power', command=lambda index=index, page_index=page_index, enemy=enemy: apply_power(master, encounter, page_index, enemy)).grid(row=24, column=0)
			ttk.Button(enemy_frame_list[index], text='Damage', command=lambda index=index, page_index=page_index, enemy=enemy: take_damage(master, encounter, page_index, enemy)).grid(row=24, column=1)
			ttk.Button(enemy_frame_list[index], text='Heal', command=lambda index=index, page_index=page_index, enemy=enemy: heal(master, encounter, page_index, enemy)).grid(row=24, column=2)
			ttk.Button(enemy_frame_list[index], text='Kill', command=lambda index=index, page_index=page_index, enemy=enemy: kill(master, encounter, page_index, enemy)).grid(row=24, column=3)
			ttk.Button(enemy_frame_list[index], text='Res', command=lambda index=index, page_index=page_index, enemy=enemy: resurrect(master, encounter, page_index, enemy)).grid(row=24, column=4)

			def get_name_color(enemy):
				if enemy.is_alive:
					return 'white'
				else:
					return 'red'
			# end get_name_color

			def use_power(master, encounter, page_index, enemy, power_list):
				power_key = power_list.get(tk.ACTIVE).split(',')[0]
				damage = enemy.use_power(power_key)
				tkmb.showinfo("Power Damage", str(power_key)+" does "+str(damage)+" to target.")
				self._draw_page(master, encounter, page_index=page_index)
			#end use_power
			def reset_cd(master, encounter, page_index, enemy, power_list):
				power_key = power_list.get(tk.ACTIVE).split(',')[0]
				enemy.power_tracker[power_key] = 0
				self._draw_page(master, encounter, page_index=page_index)
			# end reset_cd

			def remove_effect(master, encounter, page_index, enemy, negative_list):
				del enemy.negative_effects[str(negative_list.get(tk.ACTIVE)).split(',')[0]]
				self._draw_page(master, encounter, page_index=page_index)
			# end remove_effect

			def apply_power(master, encounter, page_index, enemy):
				power_key = PowerSelector(master).power_key
				damage = enemy.enemy_cast_on_self(str(power_key))
				tkmb.showinfo("Combat Info", str(enemy.properties['name'])+" takes "+str(damage)+" from "+str(power_key)+".")
				self._draw_page(master, encounter, page_index=page_index)
			# end apply_power
			def take_damage(master, encounter, page_index, enemy):
				damage = int(TakeDamageInfo(master).damage)
				enemy.take_damage(damage)
				self._draw_page(master, encounter, page_index=page_index)
			# end take_damage
			def heal(master, encounter, page_index, enemy):
				if not enemy.is_alive:
					tkmb.showerror("Enemy Dead", "You must revive an enemy before healing it (1 turn cost to Healer).")
					return

				getter = HealInfo(master)
				health = int(getter.health)
				armor = int(getter.armor)
				shield = int(getter.shield)

				enemy.heal(health, armor, shield)
				self._draw_page(master, encounter, page_index=page_index)
			# end heal
			def kill(master, encounter, page_index, enemy):
				if not enemy.is_alive:
					tkmb.showerror("Enemy Dead", str(enemy.properties['name'])+" is already dead, stupid.")
					return

				enemy.kill()
				self._draw_page(master, encounter, page_index=page_index)
			# end kill
			def resurrect(master, encounter, page_index, enemy):
				if enemy.is_alive:
					tkmb.showerror("Enemy Alive", str(enemy.properties['name'])+" is already alive, idiot.")
					return

				enemy.resurrect()
				self._draw_page(master, encounter, page_index=page_index)
			# end resurrect
	# end _draw_page
# end class CombatTracker

'''
This is the main class that spawns all other classes when necessary.
'''
class GameTracker(tk.Toplevel):
	def __init__(self, master):
		# Globals
		self.PowerHandler = PowerHandler()
		self.ClassHandler = ClassHandler()
		self.LootHandler = LootHandler()
		#self.WeaponHandler = WeaponHandler()
		self.Scaler = Scaler(class_handler=self.ClassHandler,
							 power_handler=self.PowerHandler
							 #weapon_handler=self.WeaponHandler
							 )

		# pointer to the current Game object.
		# if none, then no game loaded.
		self.game = None
		self.encounter = None

		self.WebServerProcess = None

		tk.Toplevel.__init__(self, master)
		self.title("ME Game Tracker")

		self.w, self.h = self.winfo_screenwidth(), self.winfo_screenheight()
		self.h -= 20
		self.geometry("%dx%d+0+0" % (self.w, self.h))

		self.f_main = None
		self.f_treeview = None
		self.tree = None
		self.f_encounter = None

		self.tree_tracker = {}

		# styles
		self.theme = ttk.Style()
		self.theme.theme_use('clam')

		# setup methods
		self.draw_components(master)
		self.draw_menu(master)
		self.draw_game(master)

		# exit protocol register
		self.protocol("WM_DELETE_WINDOW", lambda: self.do_exit(master))

		# key bindings
		self.bind("<F5>", lambda: self.do_save_game(master, file_path='saves/quicksave.game'))

		self.mainloop()
	# end __init__

	def draw_components(self, master):
		# Components

		# Frames
		self.f_main = tk.Frame(self, bg='red')
		self.f_main.pack(fill=tk.BOTH, expand=1)

		#   Left-side bar for TreeView
		self.f_treeview = tk.Frame(self.f_main, bg='white', width=350, bd=2, relief=tk.GROOVE)
		self.f_treeview.pack(fill=tk.Y, expand=0, side=tk.LEFT)
		self.f_treeview.pack_propagate(False)
		self.f_treeview.grid_propagate(False)
		#      Tree Load button
		ttk.Button(self.f_treeview, text="Load", command=lambda: self.do_load_mission_or_encounter(master)).pack(fill=tk.X)
		#      Tree delete button
		ttk.Button(self.f_treeview, text="Delete", command=lambda: self.do_delete_mission_or_encounter(master)).pack(fill=tk.X)
		#      Tree
		self.tree = ttk.Treeview(self.f_treeview, height=40)
		self.tree.pack(fill=tk.BOTH)


		#   Encounter area
		self.f_encounter = tk.Frame(self.f_main, bg='white')
		self.f_encounter.pack(fill=tk.BOTH, expand=1)
		self.f_encounter.pack_propagate(False)
		self.f_encounter.grid_propagate(False)

		# status bar
		self.status_bar = StatusBar(self.f_main)
		self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
		self.status_bar.set("%s", "Application running...")

	# end draw_components

	def draw_menu(self, master):
		m_menubar = tk.Menu(self)
		self.config(menu=m_menubar)

		# File drop-down
		m_file = tk.Menu(m_menubar, tearoff=0)
		m_menubar.add_cascade(label='File', menu=m_file)

		m_file.add_command(label="New Game", command=lambda: self.do_new_game(master))
		m_file.add_command(label="Save Game", command=lambda: self.do_save_game(master))
		m_file.add_command(label="Load Game", command=lambda: self.do_load_game(master))

		m_file.add_separator()
		m_file.add_command(label='Exit', command=lambda: self.do_exit(master))

		# Loot drop down
		m_loot = tk.Menu(m_menubar, tearoff=0)
		m_menubar.add_cascade(label='Loot', menu=m_loot)

		m_chest = tk.Menu(m_loot, tearoff=1)
		m_loot.add_cascade(label='Chest', menu=m_chest)
		m_chest.add_command(label="Custom Chest", command=lambda: self.do_roll_chest_loot(master))

		# Websocket
		m_socket = tk.Menu(m_menubar, tearoff=0)
		m_menubar.add_cascade(label='WebSocket', menu=m_socket)

		m_socket.add_command(label="Open Socket", command=lambda: self.do_open_socket(master))
		m_socket.add_command(label="Kill Socket", command=lambda: self.do_kill_socket(master))
		m_socket.add_separator()
		m_socket.add_command(label="Push Latest Game Details", command=lambda: self.do_push_game_details(master))

		# Help drop down
		m_help = tk.Menu(m_menubar, tearoff=0)
		m_menubar.add_cascade(label='Help', menu=m_help)

		m_help.add_command(label="View Help", command=lambda: self.draw_help(master))
	# end draw_menu

	def draw_game(self, master):
		self.f_main.destroy()
		self.draw_components(master)

		if self.game != None:
			self.draw_treeview(master)

		self.update()

	# end draw_game

	def draw_treeview(self, master):
		try:
			self.tree.delete('game')
		except:
			pass

		if self.game != None:
			self.tree.insert('', 'end', iid='game', text=str(self.game.name), open=True, tag='game')
			# priority missions
			self.tree.insert('game', 'end', iid='priority_missions', open=True, text='Priority Missions (Main Storyline)')
			for prindex, priority_mission in enumerate(self.game.missions):
				self.tree.insert('priority_missions', 'end', iid=('priority_mission_'+str(priority_mission.name)+'_'+str(prindex)),
								 text='Priority: '+str(priority_mission.name)+', L'+str(priority_mission.level)+' D'+str(priority_mission.difficulty),
								 tag='priority_mission:'+str(prindex), open=True)
				for eindex, encounter in enumerate(priority_mission.encounters):
					self.tree.insert('priority_mission_'+str(priority_mission.name)+'_'+str(prindex), 'end', iid='encounter_pri_'+str(encounter.name)+'_'+str(eindex),
									 text=str(encounter.name), tag=('encounter_pri:'+str(prindex)+':'+str(eindex)))
					for enindex, enemy in enumerate(encounter.enemies):
						self.tree.insert('encounter_pri_'+str(encounter.name)+'_'+str(eindex), 'end', iid='enemy_pri_'+str(enemy.properties['name']+'_'+str(enindex)),
										 text=str(enemy.properties['name']),
										 tag=('enemy_pri:'+str(prindex)+':'+str(eindex)+':'+str(enindex)))

			# raids
			self.tree.insert('game', 'end', iid='raids', open=True, text='Raids (Premades)')
			for rindex, raid in enumerate(self.game.raids):
				pass

			# planets per game
			self.tree.insert('game', 'end', iid='planets', text='Planets (Exploration)', open=True)
			for pindex, planet in enumerate(self.game.planets):
				self.tree.insert('planets', 'end', iid=('planet_'+str(planet.name)+'_'+str(pindex)), text=str(planet.name)+' (Planet)', tag=('planet:'+str(pindex)), open=True)

				# areas per planet
				for aindex, area in enumerate(planet.areas):
					self.tree.insert('planet_'+str(planet.name)+'_'+str(pindex), 'end', iid=('area_'+str(area.name)+'_'+str(aindex)), text=str(area.name)+' (Area)', tag=('area:'+str(pindex)+':'+str(aindex)), open=True)

					# missions per area
					self.tree.insert(('area_'+str(area.name)+'_'+str(aindex)), 'end', iid=str(area.name)+'_missions', text='Missions', tag=('missions_list'), open=True)
					for mindex, mission in enumerate(area.missions):
						self.tree.insert(str(area.name)+'_missions', 'end', iid=('mission_'+str(mission.name)+'_'+str(mindex)),
										 text=str(mission.name + ", L" + str(mission.level) + ", D" + str(mission.difficulty)),
										 tag=('mission:'+str(pindex)+':'+str(aindex)+':'+str(mindex)), open=True)
						for eindex, encounter in enumerate(mission.encounters):
							self.tree.insert('mission_'+str(mission.name)+'_'+str(mindex), 'end', iid='encounter_'+str(encounter.name)+'_'+str(eindex),
											 text=str(encounter.name), tag=('encounter:'+str(pindex)+':'+str(aindex)+':'+str(mindex)+':'+str(eindex)))
							for enindex, enemy in enumerate(encounter.enemies):
								self.tree.insert('encounter_'+str(encounter.name)+'_'+str(eindex), 'end', iid='enemy_'+str(enemy.properties['name']+'_'+str(enindex)),
												 text=str(enemy.properties['name']),
												 tag=('enemy:'+str(pindex)+':'+str(aindex)+':'+str(mindex)+':'+str(eindex)+':'+str(enindex)))

					# shops for area
					self.tree.insert(('area_'+str(area.name)+'_'+str(aindex)), 'end', iid=str(area.name)+'_stores', text='Stores', tag=('stores_list'))
					for sindex, store in enumerate(area.stores):
						self.tree.insert(str(area.name)+'_stores', 'end', iid=str(area.name)+'_stores_'+str(store.name), text=str(store.name), tag=('store:'+str(pindex)+':'+str(aindex)+':'+str(sindex)))

			# items
			self.tree.insert('game', 'end', iid='items', text='Custom Items', open=False)
			for iindex, item in enumerate(self.game.items):
				self.tree.insert('items', 'end', iid=('item_'+str(item.name)+'_'+str(iindex)), text=str(item.name), tag='item:'+str(iindex), open=False)

			# TODO: Add store tracking.
		self.update()
	# end draw_treeview

	def draw_game_details(self, master):
		self.f_encounter.destroy()
		self.f_encounter = tk.Frame(self.f_main, bg='white')
		self.f_encounter.pack(fill=tk.BOTH, expand=1)
		self.f_encounter.grid_propagate(False)
		self.f_encounter.pack_propagate(False)

		if self.game == None:
			return

		f_header = tk.Frame(self.f_encounter, bg='grey', height=40)
		f_header.pack(fill=tk.X, expand=0)
		f_details = tk.Frame(self.f_encounter, bg='white')
		f_details.pack(fill=tk.BOTH, expand=1)
		f_header.pack_propagate(False)
		f_details.grid_propagate(False)

		# header
		tk.Label(f_header, text=str(self.game.name) + ", Game Details", bg='grey', fg='blue').pack(side=tk.LEFT)

		# details body
		tk.Label(f_details, text="Name:", bg='white', fg='black').grid(row=2, column=0, sticky=tk.W)
		tk.Label(f_details, text=str(self.game.name), bg='white', fg='blue').grid(row=2, column=1, sticky=tk.W)

		tk.Label(f_details, text="Date Started:", bg='white', fg='black').grid(row=3, column=0, sticky=tk.W)
		tk.Label(f_details, text=str(self.game.date_started), bg='white', fg='blue').grid(row=3, column=1, sticky=tk.W)

		# add mission button
		ttk.Button(f_details, text="Add Planet", command=lambda: self.do_new_planet(master)).grid(row=4, column=0, sticky='ew')
		ttk.Button(f_details, text="Add Priority Mission", command=lambda: self.do_new_priority_mission(master)).grid(row=5, column=0, sticky='ew')
		ttk.Button(f_details, text="Add Raid",).grid(row=6, column=0, sticky='ew')
		ttk.Button(f_details, text="Add Custom Item", command=lambda: self.do_new_item(master)).grid(row=7, column=0, sticky='ew')
	# end draw_game

	def draw_item(self, master, item):
		self.f_encounter.destroy()
		self.f_encounter = tk.Frame(self.f_main, bg='white')
		self.f_encounter.pack(fill=tk.BOTH, expand=1)
		self.f_encounter.grid_propagate(False)
		self.f_encounter.pack_propagate(False)

		if self.game == None:
			return

		f_header = tk.Frame(self.f_encounter, bg='grey', height=40)
		f_header.pack(fill=tk.X, expand=0)
		f_details = tk.Frame(self.f_encounter, bg='white')
		f_details.pack(fill=tk.BOTH, expand=1)
		f_header.pack_propagate(False)
		f_details.grid_propagate(False)

		# header
		tk.Label(f_header, text=str(self.game.name) + " :: " + str(item.name) + ", Item Details", bg='grey', fg='blue').pack(side=tk.LEFT)

		# details
		tk.Label(f_details, text="Name:", bg='white', fg='black').grid(row=2, column=0, sticky=tk.W)
		v_name = tk.StringVar()
		e_name = tk.Entry(f_details, textvariable=v_name, bg='white', fg='black')
		e_name.grid(row=2, column=1, sticky=tk.W)
		v_name.set(item.name)

		tk.Label(f_details, text="Rarity:", bg='white', fg='black').grid(row=3, column=0, sticky=tk.W)
		v_qual = tk.StringVar()
		e_qual = tk.Entry(f_details, textvariable=v_qual, bg='white', fg='black')
		e_qual.grid(row=3, column=1, sticky=tk.W)
		v_qual.set(item.quality)
		tk.Label(f_details, text='(0-4)', bg='white', fg='black').grid(row=3, column=2, sticky=tk.W)

		tk.Label(f_details, text="Value (per unit):", bg='white', fg='black').grid(row=4, column=0, sticky=tk.W)
		v_val = tk.StringVar()
		e_val = tk.Entry(f_details, textvariable=v_val, bg='white', fg='black')
		e_val.grid(row=4, column=1, sticky=tk.W)
		v_val.set(str(item.value))

		tk.Label(f_details, text="Image:", bg='white', fg='black').grid(row=5, column=0, sticky=tk.W)
		v_img_src = item.icon_path
		tk.Label(f_details, text=v_img_src, bg='white', fg='black').grid(row=5, column=1, sticky=tk.W)
		tk.Label(f_details, text='If no image at this location, it will use base/quality image.', bg='white', fg='black').grid(row=5, column=2, sticky=tk.W)

		tk.Label(f_details, text="Item Description (Player)", bg='white', fg='black').grid(row=6, column=0, columnspan=2, sticky=tk.W)
		e_desc = st.ScrolledText(f_details, bg='white', fg='black', height=20)
		e_desc.grid(row=7, column=0, columnspan=4)
		e_desc.insert(tk.END, str(item.description))

		tk.Label(f_details, text="Item Description (GM Only)", bg='white', fg='black').grid(row=8, column=0, columnspan=2, sticky=tk.W)
		e_gmdesc = st.ScrolledText(f_details, bg='white', fg='black', height=20)
		e_gmdesc.grid(row=9, column=0, columnspan=4)
		e_gmdesc.insert(tk.END, str(item.gmdescription))

		#image preview
		tk.Label(f_details, text=item.name, bg='black', fg=static.QUALITIES_COLOR[int(item.quality)+1]).grid(row=2, column=5, sticky='ew')
		loot_icon = tk.PhotoImage(file=item.icon_path)
		image_label = tk.Label(f_details, image=loot_icon)
		image_label.image = loot_icon
		image_label.grid(row=3, column=5, rowspan=4, sticky=tk.W)

		# update button
		ttk.Button(f_header, text="Update", command=lambda: update(master, item, v_name.get(), int(v_qual.get()), int(v_val.get()), v_img_src,
															       e_desc.get('1.0', tk.END), e_gmdesc.get('1.0', tk.END))).pack(side=tk.RIGHT)

		def update(master, item, name, quality, value, img_src, description, gmdescription):
			item.update(name, quality, value, img_src, description, gmdescription)
			self.draw_treeview(master)
			self.draw_item(master, item)
			self.status_bar.set("%s", "Item updated...")
		# end update

	# end draw_item

	def draw_planet(self, master, planet):
		self.f_encounter.destroy()
		self.f_encounter = tk.Frame(self.f_main, bg='white')
		self.f_encounter.pack(fill=tk.BOTH, expand=1)
		self.f_encounter.grid_propagate(False)
		self.f_encounter.pack_propagate(False)

		f_header = tk.Frame(self.f_encounter, bg='grey', height=40)
		f_header.pack(fill=tk.X, expand=0)
		f_details = tk.Frame(self.f_encounter, bg='white')
		f_details.pack(fill=tk.BOTH, expand=1)
		f_header.pack_propagate(False)
		f_details.grid_propagate(False)

		# header
		label_text = str(self.game.name) + " :: " + str(planet.name) + ", Planet Details"
		tk.Label(f_header, text=label_text, bg='grey', fg='blue').pack(side=tk.LEFT)

		# details body
		tk.Label(f_details, text="Name:", bg='white', fg='black').grid(row=2, column=0, sticky=tk.W)
		v_name = tk.StringVar()
		e_name = tk.Entry(f_details, textvariable=v_name, bg='white', fg='black')
		e_name.grid(row=2, column=1, sticky=tk.W)
		v_name.set(planet.name)

		tk.Label(f_details, text="Level:", bg='white', fg='black').grid(row=3, column=0, sticky=tk.W)
		v_level = tk.StringVar()
		e_level = tk.Entry(f_details, textvariable=v_level, bg='white', fg='black')
		e_level.grid(row=3, column=1, sticky=tk.W)
		v_level.set(str(planet.level))
		tk.Label(f_details, text="(1-20)", bg='white', fg='black').grid(row=3, column=2, sticky=tk.W)

		tk.Label(f_details, text="Difficulty:", bg='white', fg='black').grid(row=4, column=0, sticky=tk.W)
		v_diff = tk.StringVar()
		e_diff = tk.Entry(f_details, textvariable=v_diff, bg='white', fg='black')
		e_diff.grid(row=4, column=1, sticky=tk.W)
		v_diff.set(str(planet.difficulty))
		tk.Label(f_details, text="(1-4, 2 average, 4 champion)", bg='white', fg='black').grid(row=4, column=2, sticky=tk.W)

		tk.Label(f_details, text="Planet Description", bg='white', fg='black').grid(row=6, column=0, columnspan=2, sticky=tk.W)
		e_desc = st.ScrolledText(f_details, bg='white', fg='black', height=20)
		e_desc.grid(row=7, column=0, columnspan=4)
		e_desc.insert(tk.END, str(planet.description))

		tk.Label(f_details, text="Planet Description (GM Only)", bg='white', fg='black').grid(row=8, column=0, columnspan=2, sticky=tk.W)
		e_gmdesc = st.ScrolledText(f_details, bg='white', fg='black', height=20)
		e_gmdesc.grid(row=9, column=0, columnspan=4)
		e_gmdesc.insert(tk.END, str(planet.gmdescription))

		# save button
		ttk.Button(f_header, text="Update", command=lambda: update(master, planet, v_name.get(), int(v_level.get()), int(v_diff.get()),
																   e_desc.get('1.0', tk.END), e_gmdesc.get('1.0', tk.END))).pack(side=tk.RIGHT)

		# new area button
		ttk.Button(f_details, text="Add Area", command=lambda: self.do_new_area(master, planet)).grid(row=3, column=5)

		def update(master, planet, name, level, difficulty, description, gmdescription, tree_selection=None):
			planet.update(name, level, difficulty, description, gmdescription)
			self.draw_treeview(master)
			if tree_selection != None:
				self.tree.selection_set(tree_selection)
			self.status_bar.set("%s", "Planet updated.")
		# end update
	# end draw_planet

	def draw_area(self, master, planet, area):
		self.f_encounter.destroy()
		self.f_encounter = tk.Frame(self.f_main, bg='white')
		self.f_encounter.pack(fill=tk.BOTH, expand=1)
		self.f_encounter.grid_propagate(False)
		self.f_encounter.pack_propagate(False)

		f_header = tk.Frame(self.f_encounter, bg='grey', height=40)
		f_header.pack(fill=tk.X, expand=0)
		f_details = tk.Frame(self.f_encounter, bg='white')
		f_details.pack(fill=tk.BOTH, expand=1)
		f_header.pack_propagate(False)
		f_details.grid_propagate(False)

		# header
		label_text = str(self.game.name) + " :: " + str(planet.name) + " :: " + str(area.name) + ", Area Details"
		tk.Label(f_header, text=label_text, bg='grey', fg='blue').pack(side=tk.LEFT)

		# details body
		tk.Label(f_details, text="Name:", bg='white', fg='black').grid(row=2, column=0, sticky=tk.W)
		v_name = tk.StringVar()
		e_name = tk.Entry(f_details, textvariable=v_name, bg='white', fg='black')
		e_name.grid(row=2, column=1, sticky=tk.W)
		v_name.set(area.name)

		tk.Label(f_details, text="Level:", bg='white', fg='black').grid(row=3, column=0, sticky=tk.W)
		v_level = tk.StringVar()
		e_level = tk.Entry(f_details, textvariable=v_level, bg='white', fg='black')
		e_level.grid(row=3, column=1, sticky=tk.W)
		v_level.set(str(area.level))
		tk.Label(f_details, text="(1-20)", bg='white', fg='black').grid(row=3, column=2, sticky=tk.W)

		tk.Label(f_details, text="Difficulty:", bg='white', fg='black').grid(row=4, column=0, sticky=tk.W)
		v_diff = tk.StringVar()
		e_diff = tk.Entry(f_details, textvariable=v_diff, bg='white', fg='black')
		e_diff.grid(row=4, column=1, sticky=tk.W)
		v_diff.set(str(area.difficulty))
		tk.Label(f_details, text="(1-4, 2 average, 4 champion)", bg='white', fg='black').grid(row=4, column=2, sticky=tk.W)

		tk.Label(f_details, text="Planet Description", bg='white', fg='black').grid(row=6, column=0, columnspan=2, sticky=tk.W)
		e_desc = st.ScrolledText(f_details, bg='white', fg='black', height=20)
		e_desc.grid(row=7, column=0, columnspan=4)
		e_desc.insert(tk.END, str(area.description))

		tk.Label(f_details, text="Planet Description (GM Only)", bg='white', fg='black').grid(row=8, column=0, columnspan=2, sticky=tk.W)
		e_gmdesc = st.ScrolledText(f_details, bg='white', fg='black', height=20)
		e_gmdesc.grid(row=9, column=0, columnspan=4)
		e_gmdesc.insert(tk.END, str(area.gmdescription))

		# save button
		ttk.Button(f_header, text="Update", command=lambda: update(master, area, v_name.get(), int(v_level.get()), int(v_diff.get()),
																   e_desc.get('1.0', tk.END), e_gmdesc.get('1.0', tk.END))).pack(side=tk.RIGHT)
		ttk.Button(f_header, text="WebSocket Push as Current Hub", command=lambda: FileServer.generate_hub_files(planet, area)).pack(side=tk.RIGHT, padx=3)

		# new area button
		ttk.Button(f_details, text="Add Mission", command=lambda: self.do_new_mission(master, planet, area)).grid(row=3, column=5)

		def update(master, area, name, level, difficulty, description, gmdescription, tree_selection=None):
			area.update(name, level, difficulty, description, gmdescription)
			self.draw_treeview(master)
			if tree_selection != None:
				self.tree.selection_set(tree_selection)
			self.status_bar.set("%s","Area updated.")
		# end update
	# end draw_area

	def draw_priority_mission(self, master, mission):
		self.draw_mission(master, None, None, mission, is_priority=True)
	# end draw_priority_mission

	def draw_mission(self, master, planet, area, mission, is_priority=False):
		self.f_encounter.destroy()
		self.f_encounter = tk.Frame(self.f_main, bg='white')
		self.f_encounter.pack(fill=tk.BOTH, expand=1)
		self.f_encounter.grid_propagate(False)
		self.f_encounter.pack_propagate(False)

		f_header = tk.Frame(self.f_encounter, bg='grey', height=40)
		f_header.pack(fill=tk.X, expand=0)
		f_details = tk.Frame(self.f_encounter, bg='white')
		f_details.pack(fill=tk.BOTH, expand=1)
		f_header.pack_propagate(False)
		f_details.grid_propagate(False)

		# header
		if is_priority:
			label_text = str(self.game.name) + " :: " + str(mission.name) + ", PRIORITY MISSION"
		else:
			label_text = str(self.game.name) + " :: " + str(planet.name) + " :: " + str(area.name) + " :: " + str(mission.name) + ", Mission Details"
		tk.Label(f_header, text=label_text, bg='grey', fg='blue').pack(side=tk.LEFT)

		# details body
		tk.Label(f_details, text="Name:", bg='white', fg='black').grid(row=2, column=0, sticky=tk.W)
		v_name = tk.StringVar()
		e_name = tk.Entry(f_details, textvariable=v_name, bg='white', fg='black')
		e_name.grid(row=2, column=1, sticky=tk.W)
		v_name.set(mission.name)

		tk.Label(f_details, text="Level:", bg='white', fg='black').grid(row=3, column=0, sticky=tk.W)
		v_level = tk.StringVar()
		e_level = tk.Entry(f_details, textvariable=v_level, bg='white', fg='black')
		e_level.grid(row=3, column=1, sticky=tk.W)
		v_level.set(str(mission.level))
		tk.Label(f_details, text="(1-20)", bg='white', fg='black').grid(row=3, column=2, sticky=tk.W)

		tk.Label(f_details, text="Difficulty:", bg='white', fg='black').grid(row=4, column=0, sticky=tk.W)
		v_diff = tk.StringVar()
		e_diff = tk.Entry(f_details, textvariable=v_diff, bg='white', fg='black')
		e_diff.grid(row=4, column=1, sticky=tk.W)
		v_diff.set(str(mission.difficulty))
		tk.Label(f_details, text="(1-4, 2 average, 4 champion)", bg='white', fg='black').grid(row=4, column=2, sticky=tk.W)

		tk.Label(f_details, text="Mission Description (Briefing)", bg='white', fg='black').grid(row=6, column=0, columnspan=7, sticky=tk.W)
		e_desc = st.ScrolledText(f_details, bg='white', fg='black', height=20)
		e_desc.grid(row=7, column=0, columnspan=7)
		e_desc.insert(tk.END, str(mission.description))

		tk.Label(f_details, text="Mission Rewards", bg='white', fg='black').grid(row=8, column=0, columnspan=7, sticky=tk.W)
		e_rewards = st.ScrolledText(f_details, bg='white', fg='black', height=20)
		e_rewards.grid(row=9, column=0, columnspan=7)
		e_rewards.insert(tk.END, str(mission.rewards))

		tk.Label(f_details, text="GM Description (Not visible to players)", bg='white', fg='black').grid(row=6, column=7, columnspan=2, sticky=tk.W)
		e_gmdesc = st.ScrolledText(f_details, bg='white', fg='black', height=40)
		e_gmdesc.grid(row=7, column=7, rowspan=4, columnspan=2)
		e_gmdesc.insert(tk.END, str(mission.gmdescription))

		# is it complete?
		tk.Label(f_details, text="Complete?", bg='white', fg='black').grid(row=2, column=5, sticky=tk.E)
		v_comp = tk.StringVar()
		v_comp.set(str(mission.is_complete))
		c_comp = ttk.Checkbutton(f_details, variable=v_comp, onvalue='True', offvalue='False')
		c_comp.grid(row=2, column=6, sticky=tk.W)

		# save button
		ttk.Button(f_header, text="Update", command=lambda: update(master, mission, v_name.get(), int(v_level.get()), int(v_diff.get()),
																   e_desc.get('1.0', tk.END), e_gmdesc.get('1.0', tk.END),
																   e_rewards.get('1.0', tk.END), str(v_comp.get()))).pack(side=tk.RIGHT)

		if is_priority:
			ttk.Button(f_header, text="WebSocket Push as Current Priority Mission", command=lambda: self.do_push_game_details(master, self.game, mission)).pack(side=tk.RIGHT, padx=3)

		# new encounter button
		ttk.Button(f_details, text="Add Encounter", command=lambda: self.do_new_encounter(master, planet, area, mission)).grid(row=3, column=5, columnspan=2, sticky='ew')

		def update(master, mission, name, level, difficulty, description, gmdescription, rewards, mstate):
			mission.update(name, level, difficulty, description, gmdescription, rewards, state=mstate)
			self.draw_treeview(master)
			self.status_bar.set("%s", "Mission updated.")
		# end update

	# end draw_mission

	def draw_encounter(self, master, planet, area, mission, encounter, is_priority=False):
		self.f_encounter.destroy()
		self.f_encounter = tk.Frame(self.f_main, bg='white')
		self.f_encounter.pack(fill=tk.BOTH, expand=1)
		self.f_encounter.grid_propagate(False)
		self.f_encounter.pack_propagate(False)

		f_header = tk.Frame(self.f_encounter, bg='grey', height=40)
		f_header.pack(fill=tk.X, expand=0)
		f_details = tk.Frame(self.f_encounter, bg='white')
		f_details.pack(fill=tk.BOTH, expand=1)
		f_header.pack_propagate(False)
		f_details.grid_propagate(False)

		# header
		if is_priority:
			label_text = str(self.game.name) + " :: " + str(mission.name) + " (PRIORITY MISSION) :: " + str(encounter.name) + ", Encounter Details"
		else:
			label_text = str(self.game.name) + " :: " + str(planet.name) + " :: " + str(area.name) + " :: " + str(mission.name) + " :: " + str(encounter.name) + ", Encounter Details"
		tk.Label(f_header, text=label_text, bg='grey', fg='blue').pack(side=tk.LEFT)

		#details
		tk.Label(f_details, text="Name:", bg='white', fg='black').grid(row=0, column=0, sticky=tk.W)
		v_name = tk.StringVar()
		e_name = tk.Entry(f_details, textvariable=v_name, bg='white', fg='black')
		e_name.grid(row=0, column=1, sticky=tk.W)
		v_name.set(encounter.name)

		tk.Label(f_details, text="Level:", bg='white', fg='black').grid(row=1, column=0, sticky=tk.W)
		v_level = tk.StringVar()
		e_level = tk.Entry(f_details, textvariable=v_level, bg='white', fg='black')
		e_level.grid(row=1, column=1, sticky=tk.W)
		v_level.set(str(encounter.level))
		tk.Label(f_details, text="(1-20)", bg='white', fg='black').grid(row=1, column=2, sticky=tk.W)

		tk.Label(f_details, text="Difficulty:", bg='white', fg='black').grid(row=2, column=0, sticky=tk.W)
		v_diff = tk.StringVar()
		e_diff = tk.Entry(f_details, textvariable=v_diff, bg='white', fg='black')
		e_diff.grid(row=2, column=1, sticky=tk.W)
		v_diff.set(str(encounter.difficulty))
		tk.Label(f_details, text="(1-4, 2 average, 4 champion)", bg='white', fg='black').grid(row=2, column=2, sticky=tk.W)

		tk.Label(f_details, text="Boss encounter?", bg='white', fg='black').grid(row=3, column=0, columnspan=2, sticky=tk.W)
		v_boss = tk.BooleanVar()
		v_boss.set(bool(encounter.is_boss))
		c_boss = ttk.Checkbutton(f_details, variable=v_boss, onvalue=True, offvalue=False)
		c_boss.grid(row=3, column=2, sticky=tk.W)

		ttk.Separator(f_details, orient=tk.VERTICAL).grid(row=0, column=3, rowspan=5, sticky='ns', padx=3)

		tk.Label(f_details, text="Encounter Description (Mechanics)", bg='white', fg='black').grid(row=0, column=5, columnspan=2, sticky=tk.W)
		e_desc = st.ScrolledText(f_details, bg='white', fg='black', height=5)
		e_desc.grid(row=1, column=5, columnspan=5, rowspan=5)
		e_desc.insert(tk.END, str(encounter.description))

		ttk.Button(f_header, text="WebSocket Push as Current Encounter", command=lambda: FileServer.generate_encounter_files(encounter)).pack(side=tk.RIGHT, padx=3)

		# add enemy button
		ttk.Button(f_details, text='Add Enemy', command=lambda: self.do_add_enemy(master, planet, area, mission, encounter)).grid(row=4, column=0, columnspan=3, sticky='ew')

		ttk.Separator(f_details, orient=tk.HORIZONTAL).grid(row=7, column=0, columnspan=10, sticky='ew', pady=5)

		# enemies
		ttk.Button(f_details, text="Combat Tracker", command=lambda: do_combat_tracker(master, encounter)).grid(row=8, column=0, columnspan=5)

		# loot
		tk.Label(f_details, text='Customs Only?', bg='white', fg='black').grid(row=8, column=6, sticky=tk.E)
		v_specialsonly = tk.BooleanVar()
		v_specialsonly.set(bool(encounter.customs_only))
		c_specialsonly = ttk.Checkbutton(f_details, variable=v_specialsonly, onvalue=True, offvalue=False)
		c_specialsonly.grid(row=8, column=7, sticky=tk.W)

		ttk.Button(f_details, text='View Loot', command=lambda: do_view_loot(master, encounter)).grid(row=8, column=8, sticky='ew')
		ttk.Button(f_details, text="Roll Loot", command=lambda: do_roll_loot(master, mission, encounter)).grid(row=8, column=9, sticky='ew')

		# specials loot definitions
		ttk.Separator(f_details, orient=tk.HORIZONTAL).grid(row=9, column=0, columnspan=10, sticky='ew', pady=5)
		tk.Label(f_details, text='Special Item Loot Table', bg='white', fg='blue').grid(row=10, column=0, columnspan=10)
		l_special_loot = tk.Listbox(f_details, selectmode=tk.BROWSE)
		l_special_loot.grid(row=11, column=0, columnspan=4, rowspan=4, sticky='ew')
		for item_tuple in encounter.special_loot:
			l_special_loot.insert(tk.END, str(item_tuple[0]) + "," + str(self.game.items[int(item_tuple[0])].name) + "," + str(item_tuple[1]) + "%")
		# add new button
		ttk.Button(f_details, text='Delete', command=lambda: do_delete_special()).grid(row=15, column=2, columnspan=2, sticky='ew')

		options = ['']
		for item in self.game.items:
			options.append(item.name)

		v_special_item = tk.StringVar()
		op_special_item = apply(ttk.OptionMenu, (f_details, v_special_item) + tuple(options))
		op_special_item.grid(row=16, column=0, columnspan=2, sticky='ew')
		v_chance = tk.StringVar()
		e_chance = tk.Entry(f_details, textvariable=v_chance, bg='white', fg='black')
		e_chance.grid(row=16, column=2, sticky='ew')
		v_chance.set("0")
		ttk.Button(f_details, text='Add New', command=lambda: do_add_new_special_loot()).grid(row=16, column=3, sticky='ew')


		ttk.Button(f_header, text="Update", command=lambda encounter=encounter: encounter.update(v_name.get(), int(v_level.get()), int(v_diff.get()),
																		     			  e_desc.get('1.0', tk.END), bool(v_boss.get()), l_special_loot.get(0, tk.END), bool(v_specialsonly.get()))).pack(side=tk.RIGHT)

		def do_roll_loot(master, mission, encounter):
			getter = NewLootTableInfo(master)
			encounter.add_loot_table(self.LootHandler.roll_encounter_loot(self.game, encounter, getter.avg_level, getter.num_players))
			do_view_loot(master, encounter)
		def do_view_loot(master, encounter):
			loot_viewer = LootTableViewer(master, encounter, self.LootHandler)

		def do_add_new_special_loot():
			item_number = 0
			for item in self.game.items:
				if item.name == v_special_item.get():
					break
				item_number += 1
			item_chance = int(v_chance.get())
			encounter.add_special(item_number, item_chance)
			self.draw_encounter(master, planet, area, mission, encounter, is_priority=is_priority)

		def do_delete_special():
			selection_index = l_special_loot.curselection()
			encounter.delete_special(selection_index[0])
			self.draw_encounter(master, planet, area, mission, encounter, is_priority=is_priority)

		def do_combat_tracker(master, encounter):
			tracker = CombatTracker(master, encounter)

	# end draw_encounter

	def draw_enemy(self, master, planet, area, mission, encounter, enemy, is_priority=False):
		self.f_encounter.destroy()
		self.f_encounter = tk.Frame(self.f_main, bg='white')
		self.f_encounter.pack(fill=tk.BOTH, expand=1)
		self.f_encounter.grid_propagate(False)
		self.f_encounter.pack_propagate(False)

		f_header = tk.Frame(self.f_encounter, bg='grey', height=40)
		f_header.pack(fill=tk.X, expand=0)
		f_details = tk.Frame(self.f_encounter, bg='white')
		f_details.pack(fill=tk.BOTH, expand=1)
		f_header.pack_propagate(False)
		f_details.grid_propagate(False)

		if is_priority:
			label_text = str(self.game.name) + " :: " + str(mission.name) + " (PRIORITY MISSION) :: " + str(encounter.name) + " :: " + str(enemy.properties['name']) + ", Enemy Details"
		else:
			label_text = str(self.game.name) + " :: " + str(planet.name) + " :: " + str(area.name) + " :: " + str(mission.name) + " :: " + str(encounter.name) + " :: " + str(enemy.properties['name']) + ", Enemy Details"
		tk.Label(f_header, text=label_text, bg='grey', fg='blue').pack(side=tk.LEFT)

		tk.Label(f_details, text="Name:", bg='white', fg='black').grid(row=0, column=0, sticky=tk.W)
		v_name = tk.StringVar()
		e_name = tk.Entry(f_details, textvariable=v_name, bg='white', fg='black')
		e_name.grid(row=0, column=1, sticky=tk.W)
		v_name.set(enemy.properties['name'])

		tk.Label(f_details, text="Level:", bg='white', fg='black').grid(row=1, column=0, sticky=tk.W)
		v_level = tk.StringVar()
		e_level = tk.Entry(f_details, textvariable=v_level, bg='white', fg='black')
		e_level.grid(row=1, column=1, sticky=tk.W)
		v_level.set(str(enemy.properties['level']))
		tk.Label(f_details, text="(1-20)", bg='white', fg='black').grid(row=1, column=2, sticky=tk.W)

		tk.Label(f_details, text="Difficulty:", bg='white', fg='black').grid(row=2, column=0, sticky=tk.W)
		v_diff = tk.StringVar()
		e_diff = tk.Entry(f_details, textvariable=v_diff, bg='white', fg='black')
		e_diff.grid(row=2, column=1, sticky=tk.W)
		v_diff.set(str(enemy.properties['difficulty']))
		tk.Label(f_details, text="(1-4, 2 average, 4 champion)", bg='white', fg='black').grid(row=2, column=2, sticky=tk.W)

		tk.Label(f_details, text="Role:", bg='white', fg='black').grid(row=3, column=0, sticky=tk.W)
		v_role = tk.StringVar()
		v_role.set(enemy.properties['role'])
		op_role = apply(ttk.OptionMenu, (f_details, v_role) + tuple(static.ROLES))
		op_role.grid(row=3, column=1, sticky='ew')

		tk.Label(f_details, text="Race:", bg='white', fg='black').grid(row=4, column=0, sticky=tk.W)
		v_race = tk.StringVar()
		v_race.set(enemy.properties['race'])
		op_race = apply(ttk.OptionMenu, (f_details, v_race) + tuple(static.RACES))
		op_race.grid(row=4, column=1, sticky='ew')

		tk.Label(f_details, text="Class:", bg='white', fg='black').grid(row=5, column=0, sticky=tk.W)
		v_class = tk.StringVar()
		v_class.set(enemy.properties['class_key'])
		op_role = apply(ttk.OptionMenu, (f_details, v_class) + tuple(static.CLASSES))
		op_role.grid(row=5, column=1, sticky='ew')

		tk.Label(f_details, text="Max Health:", bg='white', fg='black').grid(row=6, column=0, sticky=tk.W)
		v_health = tk.StringVar()
		e_mhealth = tk.Entry(f_details, textvariable=v_health, bg='white', fg='black')
		e_mhealth.grid(row=6, column=1, sticky=tk.W)
		v_health.set(str(enemy.properties['max_health']))

		tk.Label(f_details, text="Max Shield / Recharge:", bg='white', fg='black').grid(row=7, column=0, sticky=tk.W)
		v_shield = tk.StringVar()
		v_recharge = tk.StringVar()
		e_mshield = tk.Entry(f_details, textvariable=v_shield, bg='white', fg='black')
		e_mshield.grid(row=7, column=1, sticky=tk.W)
		e_recharge = tk.Entry(f_details, textvariable=v_recharge, bg='white', fg='black')
		e_recharge.grid(row=7, column=2, sticky=tk.W, padx=3)
		v_shield.set(str(enemy.properties['max_shield']))
		v_recharge.set(str(enemy.properties['shield_recharge']))

		tk.Label(f_details, text="Armor:", bg='white', fg='black').grid(row=8, column=0, sticky=tk.W)
		v_armor = tk.StringVar()
		e_armor = tk.Entry(f_details, textvariable=v_armor, bg='white', fg='black')
		e_armor.grid(row=8, column=1, sticky=tk.W)
		v_armor.set(str(enemy.properties['max_armor']))	

		tk.Label(f_details, text="Damage Reduction:", bg='white', fg='black').grid(row=9, column=0, sticky=tk.W)
		v_dr = tk.StringVar()
		e_dr = tk.Entry(f_details, textvariable=v_dr, bg='white', fg='black')
		e_dr.grid(row=9, column=1, sticky=tk.W)
		v_dr.set(str(enemy.properties['damage_reduction']))

		# stats
		ttk.Separator(f_details, orient=tk.VERTICAL).grid(row=0, column=3, rowspan=10, sticky='ns', padx=3)
		tk.Label(f_details, text="Attributes", bg='white', fg='black').grid(row=0, column=4, columnspan=2)

		tk.Label(f_details, text="CON", bg='white', fg='black').grid(row=1, column=4, sticky=tk.W)
		v_con = tk.StringVar()
		e_con = tk.Entry(f_details, textvariable=v_con, bg='white', fg='black')
		e_con.grid(row=1, column=5, sticky=tk.W)
		v_con.set(enemy.properties['base_stats']['CON'])

		tk.Label(f_details, text="ACC", bg='white', fg='black').grid(row=2, column=4, sticky=tk.W)
		v_acc = tk.StringVar()
		e_acc = tk.Entry(f_details, textvariable=v_acc, bg='white', fg='black')
		e_acc.grid(row=2, column=5, sticky=tk.W)
		v_acc.set(enemy.properties['base_stats']['ACC'])

		tk.Label(f_details, text="FIT", bg='white', fg='black').grid(row=3, column=4, sticky=tk.W)
		v_fit = tk.StringVar()
		e_fit = tk.Entry(f_details, textvariable=v_fit, bg='white', fg='black')
		e_fit.grid(row=3, column=5, sticky=tk.W)
		v_fit.set(enemy.properties['base_stats']['FIT'])

		tk.Label(f_details, text="INT", bg='white', fg='black').grid(row=4, column=4, sticky=tk.W)
		v_int = tk.StringVar()
		e_int = tk.Entry(f_details, textvariable=v_int, bg='white', fg='black')
		e_int.grid(row=4, column=5, sticky=tk.W)
		v_int.set(enemy.properties['base_stats']['INT'])

		tk.Label(f_details, text="AWR", bg='white', fg='black').grid(row=5, column=4, sticky=tk.W)
		v_awr = tk.StringVar()
		e_awr = tk.Entry(f_details, textvariable=v_awr, bg='white', fg='black')
		e_awr.grid(row=5, column=5, sticky=tk.W)
		v_awr.set(enemy.properties['base_stats']['AWR'])

		tk.Label(f_details, text="BIF", bg='white', fg='black').grid(row=6, column=4, sticky=tk.W)
		v_bif = tk.StringVar()
		e_bif = tk.Entry(f_details, textvariable=v_bif, bg='white', fg='black')
		e_bif.grid(row=6, column=5, sticky=tk.W)
		v_bif.set(enemy.properties['base_stats']['BIF'])

		ttk.Button(f_details, text="Roll Stats", command=lambda: self.do_roll_stats(master, mission, encounter, enemy, mission_index, encounter_index, enemy_index,
																					int(enemy.properties['level']),
																					int(enemy.properties['difficulty']),
																					str(enemy.properties['role']),
																					str(enemy.properties['class_key']))).grid(row=7, column=4, columnspan=2, sticky='ew')

		# weapon
		ttk.Separator(f_details, orient=tk.VERTICAL).grid(row=0, column=6, rowspan=10, sticky='ns', padx=3)
		if enemy.properties['weapons'] != None:
			weapon = enemy.properties['weapons']
			tk.Label(f_details, text=(str(weapon.name) + ', ' + str(weapon.man)), bg='white', fg=static.QUALITIES_COLOR[int(weapon.quality)]).grid(row=0, column=7, columnspan=2, sticky=tk.W)
			tk.Label(f_details, text=(str(weapon.shots_per_round) + ' x D' + str(weapon.damage_per_shot)), bg='white', fg='black').grid(row=1, column=7, columnspan=2, sticky=tk.W)
			tk.Label(f_details, text=(str(weapon.crit_chance * 10) + "\%" + " Crit Chance"), bg='white', fg='black').grid(row=2, column=7, sticky=tk.W)
			tk.Label(f_details, text=(str(weapon.crit_multiplier * 100) + "\%" + " Crit Multiplier"), bg='white', fg='black').grid(row=2, column=8, sticky=tk.W)
			ttk.Button(f_details, text="Roll Damage", command=lambda: roll_damage(weapon, enemy.properties['base_stats']['ACC'])).grid(row=3, column=7, columnspan=2, sticky='ew')
		else:
			# there is no weapon. so create one.
			ttk.Button(f_details, text="Create Weapon", command=lambda: self.do_new_weapon(master, mission, encounter, enemy)).grid(row=0, column=7, columnspan=2, sticky='ew')

		e_desc = st.ScrolledText(f_details, bg='white', fg='black', height=5)
		e_desc.grid(row=11, column=0, columnspan=10, rowspan=1, pady=3)
		e_desc.insert(tk.END, str(enemy.properties['description']))

		# powers
		ttk.Separator(f_details, orient=tk.HORIZONTAL).grid(row=12, column=0, columnspan=10, sticky='ew', pady=3)
		tk.Label(f_details, text="Powers", bg='white', fg='black').grid(row=13, column=0, columnspan=3)

		all_powers = self.PowerHandler.get_power_list()

		# current powers
		l_enemy_powers = tk.Listbox(f_details, selectmode=tk.BROWSE)
		l_enemy_powers.grid(row=14, column=0, columnspan=2, rowspan=4, sticky='ew')

		# buttons
		ttk.Button(f_details, text="<<", command=lambda: add_power()).grid(row=15, column=2, sticky='ew')
		ttk.Button(f_details, text=">>", command=lambda: remove_power()).grid(row=16, column=2, sticky='ew')

		# available powers
		l_available_powers = tk.Listbox(f_details, selectmode=tk.BROWSE, height=20,)
		l_available_powers.grid(row=14, column=3, columnspan=3, rowspan=6, sticky='ew')

		# populate
		for key in enemy.properties['powers']:
			l_enemy_powers.insert(tk.END, str(key))

		for key in all_powers:
			if key not in enemy.properties['powers']:
				l_available_powers.insert(tk.END, str(key))




		# save button
		ttk.Button(f_header, text="Update", command=lambda: enemy.update(v_name.get(),
																		 int(v_level.get()),
																		 int(v_diff.get()),
																		 v_role.get(),
																		 v_race.get(),
																		 v_class.get(),
																		 int(v_health.get()),
																		 int(v_shield.get()),
																		 int(v_recharge.get()),
																		 int(v_armor.get()),
																		 float(v_dr.get()),
																		 enemy.properties['weapons'],
																		 l_enemy_powers.get(0, tk.END),
																		 e_desc.get('1.0', tk.END),
																		 {'CON':int(v_con.get()),
																		  'FIT':int(v_fit.get()),
																		  'INT':int(v_int.get()),
																		  'BIF':int(v_bif.get()),
																		  'AWR':int(v_awr.get()),
																		  'ACC':int(v_acc.get())})).pack(side=tk.RIGHT)

		def add_power():
			selection_index = l_available_powers.curselection()
			selection = l_available_powers.get(selection_index)
			l_enemy_powers.insert(tk.END, str(selection))
			l_available_powers.delete(selection_index)

		def remove_power():
			selection_index = l_enemy_powers.curselection()
			selection = l_enemy_powers.get(selection_index)
			l_available_powers.insert(tk.END, str(selection))
			l_enemy_powers.delete(selection_index)

		def roll_damage(weapon, acc_score):
			damage = weapon.roll_damage(acc_score)
			tkmb.showinfo("Damage", "Weapon does " + str(damage) + " damage.")

	# end draw_enemy

	def draw_help(self, master):
		self.f_encounter.destroy()
		self.f_encounter = tk.Frame(self.f_main, bg='white')
		self.f_encounter.pack(fill=tk.BOTH, expand=1)
		self.f_encounter.grid_propagate(False)
		self.f_encounter.pack_propagate(False)

		f_header = tk.Frame(self.f_encounter, bg='grey', height=40)
		f_header.pack(fill=tk.X, expand=0)
		f_details = tk.Frame(self.f_encounter, bg='white')
		f_details.pack(fill=tk.BOTH, expand=1)
		f_header.pack_propagate(False)
		f_details.pack_propagate(False)

		label_text = "Help Manual"
		tk.Label(f_header, text=label_text, bg='grey', fg='blue').pack(side=tk.LEFT)

		text = st.ScrolledText(f_details, bg='white', fg='black')
		text.pack(fill=tk.BOTH, expand=1)

		with open('man.txt', 'r') as manual:
			text.insert(tk.END, manual.read())

		text.config(state=tk.DISABLED)
	# end draw_help

	# -------------------------------------------------------------------------------
	# Command handlers
	def do_new_game(self, master):
		name = NewGameInfo(master).result
		if name != None:
			date = datetime.date.today()
			self.game = Game(name=name, date_started=str(date.month) + '/' + str(date.day) + '/' + str(date.year))
			self.draw_game(master)
			self.draw_treeview(master)
	# end do_new_game

	def do_new_item(self, master):
		name = NewGameInfo(master).result
		if name != None:
			self.game.add_item(name=name)
			self.draw_treeview(master)
	# end do_new_item

	def do_new_planet(self, master):
		getter = NewMissionInfo(master)
		name = getter.name
		level = getter.level
		difficulty = getter.difficulty

		if name != None and level != None and difficulty != None:
			self.game.add_planet(name=name, level=level, difficulty=difficulty)
			self.draw_treeview(master)
		else:
			tkmb.showerror("Entry Error", "One or more values were missing.")
	# end do_new_planet

	def do_new_priority_mission(self, master):
		getter = NewMissionInfo(master)
		name = getter.name
		level = getter.level
		difficulty = getter.difficulty

		if name != None and level != None and difficulty != None:
			self.game.add_priority_mission(name=name, level=level, difficulty=difficulty)
			self.draw_treeview(master)
		else:
			tkmb.showerror("Entry Error", "One or more values were missing.")
	# end do_new_priority_mission

	def do_new_area(self, master, planet):
		getter = NewMissionInfo(master)
		name = getter.name
		level = getter.level
		difficulty = getter.difficulty

		if name != None and level != None and difficulty != None:
			planet.add_area(name=name, level=level, difficulty=difficulty)
			self.draw_treeview(master)
		else:
			tkmb.showerror("Entry Error", "One or more values were missing.")
	# end do_new_area

	def do_new_mission(self, master, planet, area):
		if self.game == None:
			tkmb.showerror("Game Error", "You can't add a mission before creating or loading a game, stupid!")
			return

		getter = NewMissionInfo(master)
		name = getter.name
		level = getter.level
		difficulty = getter.difficulty

		if name != None and level != None and difficulty != None:
			area.add_mission(name=name, level=level, difficulty=difficulty)
			self.draw_treeview(master)
		else:
			tkmb.showerror("Entry Error", "One or more values were missing.")
	# end do_new_mission

	def do_new_encounter(self, master, planet, area, mission):
		if self.game == None or mission == None:
			tkmb.showerror("Game Error", "You can't addd an enouncter if there's no game or mission, shit-head!")

		getter = NewEncounterInfo(master)
		name = getter.name
		level = getter.level
		difficulty = getter.difficulty

		if name != None and level != None and difficulty != None:
			mission.add_encounter(name=name, level=level, difficulty=difficulty, description=None)
			self.draw_treeview(master)
		else:
			tkmb.showerror("Entry Error", "One or more values were missing.")
	# end do_new_encounter

	def do_add_enemy(self, master, planet, area, mission, encounter):
		if self.game == None or mission == None or encounter == None:
			tkmb.showerror("Game Error", "You can't addd a mission without a game, mission, or encounter. Dumbass.")
			return

		name = NewEnemyInfo(master).name

		if name != None:
			encounter.add_enemy(name=name, class_handler=self.ClassHandler, power_handler=self.PowerHandler, class_key=static.CLASS_SOLDIER)
			self.draw_treeview(master)
		else:
			tkmb.showerror("Entry Error", "One or more values were missing.")
	# end do_add_enemy

	def do_new_weapon(self, master, planet, area, mission, encounter, enemy):
		getter = NewWeaponInfo(master)

		weapon = Weapon(str(getter.type), 'Unknown', 'man_unknown', str(getter.type), int(getter.qual),
						int(enemy.properties['level']), int(getter.speed), int(getter.damage), int(getter.mod_slots), int(getter.crit), float(getter.critm))

		enemy.add_weapon(weapon)
		self.draw_enemy(master, mission, encounter, enemy)
	# end do_new_weapon

	def do_roll_stats(self, master, mission, encounter, enemy, mission_index, encounter_index, enemy_index, level, difficulty, role, class_key):
		# stats = Scaler.roll_stats(level, difficulty, role, class_key)
		# enemy.update_stats(stats)
		# self.draw_enemy(master, mission, encounter, enemy)
		tkmb.showinfo("Implementation", "Auto-roll is not yet implemented for attributes.")
	# end do_roll_stats

	def do_load_mission_or_encounter(self, master):
		#first get the selection
		focus_iid = self.tree.focus()

		if focus_iid == '':
			tkmb.showerror("Error", "You didn't select anything from the tree, stupid!")
			return

		focus_item = self.tree.item(focus_iid)
		try:
			tag_split = focus_item['tags'][0].split(":")
			tag = tag_split[0]
		except IndexError, error:
			# no information here
			tkmb.showerror("Error", "No information available for the selected item.\n\nInternal Error: Tag is missing from tree-element.")
			return

		if tag_split[0] == 'game':
			# this is the game itself
			self.draw_game_details(master)

		elif tag_split[0] == 'item':
			item = self.game.items[int(tag_split[1])]
			self.draw_item(master, item)

		elif tag_split[0] == 'priority_mission':
			#this is a game priority storyline mission
			mission = self.game.missions[int(tag_split[1])]
			self.draw_priority_mission(master, mission)

		elif tag_split[0] == 'encounter_pri':
			mission = self.game.missions[int(tag_split[1])]
			encounter = mission.encounters[int(tag_split[2])]
			self.draw_encounter(master, None, None, mission, encounter, is_priority=True)

		elif tag_split[0] == 'enemy_pri':
			mission = self.game.missions[int(tag_split[1])]
			encounter = mission.encounters[int(tag_split[2])]
			enemy = encounter.enemies[int(tag_split[3])]
			self.draw_enemy(master, None, None, mission, encounter, enemy, is_priority=True)

		elif tag_split[0] == 'planet':
			#this is a planet
			planet = self.game.planets[int(tag_split[1])]
			self.draw_planet(master, planet)

		elif tag_split[0] == 'area':
			#this is a planet area
			planet = self.game.planets[int(tag_split[1])]
			area = planet.areas[int(tag_split[2])]
			self.draw_area(master, planet, area)

		elif tag_split[0] == 'mission':
			# this is a mission thingy
			planet = self.game.planets[int(tag_split[1])]
			area = planet.areas[int(tag_split[2])]
			mission = area.missions[int(tag_split[3])]
			self.draw_mission(master, planet, area, mission)

		elif tag_split[0] == 'encounter':
			# this is an encounter thingy
			planet = self.game.planets[int(tag_split[1])]
			area = planet.areas[int(tag_split[2])]
			mission = area.missions[int(tag_split[3])]
			encounter = mission.encounters[int(tag_split[4])]
			self.draw_encounter(master, planet, area, mission, encounter)

		elif tag_split[0] == 'enemy':
			planet = self.game.planets[int(tag_split[1])]
			area = planet.areas[int(tag_split[2])]
			mission = area.missions[int(tag_split[3])]
			encounter = mission.encounters[int(tag_split[4])]
			enemy = encounter.enemies[int(tag_split[5])]
			self.draw_enemy(master, planet, area, mission, encounter, enemy)

		else:
			# idk what you fucked up, but it should be one of the above...
			tkmb.showerror("Error", "No information available for the selected item.")

	# end do_load_mission_or_encounter

	def do_delete_mission_or_encounter(self, master):
		#first get the selection
		focus_iid = self.tree.focus()

		if focus_iid == '':
			tkmb.showerror("Error", "You didn't select anything from the tree, stupid!")
			return

		focus_item = self.tree.item(focus_iid)

		if not tkmb.askokcancel("Delete Element", "Are you sure you want to delete that? (It will delete all sub-elements from the tree too, ya know...)"):
			return

		try:
			tag_split = focus_item['tags'][0].split(":")
			tag = tag_split[0]
		except IndexError, error:
			# no information here
			tkmb.showerror("Error", "No information available for the selected item.\n\nInternal Error: Tag is missing from tree-element.")
			return

		if tag_split[0] == 'game':
			# this is the game itself
			self.draw_game_details(master)

		if tag_split[0] == 'item':
			if tkmb.askokcancel('Item Deletion', 'Removing this item may cause issues if you have included said item in a loot table!'):
				self.game.items.pop(int(tag_split[1]))

		elif tag_split[0] == 'priority_mission':
			#this is a game priority storyline mission
			self.game.missions.pop(int(tag_split[1]))

		elif tag_split[0] == 'encounter_pri':
			mission = self.game.missions[int(tag_split[1])]
			mission.encounters.pop(int(tag_split[2]))

		elif tag_split[0] == 'enemy_pri':
			mission = self.game.missions[int(tag_split[1])]
			encounter = mission.encounters[int(tag_split[2])]
			encounter.enemies.pop(int(tag_split[3]))

		elif tag_split[0] == 'planet':
			#this is a planet
			self.game.planets.pop(int(tag_split[1]))

		elif tag_split[0] == 'area':
			#this is a planet area
			planet = self.game.planets[int(tag_split[1])]
			planet.areas.pop(int(tag_split[2]))

		elif tag_split[0] == 'mission':
			# this is a mission thingy
			planet = self.game.planets[int(tag_split[1])]
			area = planet.areas[int(tag_split[2])]
			area.missions.pop(int(tag_split[3]))

		elif tag_split[0] == 'encounter':
			# this is an encounter thingy
			planet = self.game.planets[int(tag_split[1])]
			area = planet.areas[int(tag_split[2])]
			mission = area.missions[int(tag_split[3])]
			mission.encounters.pop(int(tag_split[4]))

		elif tag_split[0] == 'enemy':
			planet = self.game.planets[int(tag_split[1])]
			area = planet.areas[int(tag_split[2])]
			mission = area.missions[int(tag_split[3])]
			encounter = mission.encounters[int(tag_split[4])]
			encounter.enemies.pop(int(tag_split[5]))

		else:
			# idk what you fucked up, but it should be one of the above...
			tkmb.showerror("Error", "No information available for the selected item.")

		self.draw_treeview(master)

	# end do_delete_mission_or_encounter

	def do_save_game(self, master, file_path=None):
		if file_path == None:
			save_file = tkfd.asksaveasfilename(defaultextension='game', initialdir='saves', parent=master, title="Save game as...")
		else:
			save_file = file_path
		if save_file != None:
			self.status_bar.set("Saving game to %s", save_file)
			SavegameHandler.game_to_file(save_file, self.game)
			self.status_bar.set("%s", "Game saved.")
	# end do_save_game

	def do_load_game(self, master):
		load_file = tkfd.askopenfilename(defaultextension='game', initialdir='saves', parent=master, title="Open game...")
		if load_file != None:
			self.status_bar.set("Loading game from %s", load_file)
			self.game = SavegameHandler.game_from_file(load_file)

			self.f_main.destroy()
			self.draw_components(master)
			self.draw_treeview(master)
			self.status_bar.set("%s", "Game loaded.")
	# end do_load_game

	def do_roll_chest_loot(self, master):
		getter = NewChestLootInfo(master)
		loot_table = self.LootHandler.roll_chest_loot(chest_level=getter.level, number_items=getter.num_pieces, chest_type=getter.chest_type, guaranteed_quality=getter.e_gquality, gear_type=getter.gear_type, can_have_credits=getter.contains_credits)
		viewer = LootTableViewer(master, None, self.LootHandler, loot_table=loot_table)
	# end do_roll_chest_loot

	def do_exit(self, master):
		if tkmb.askokcancel("Quit", "Please save all changes before quitting!"):
			if self.WebServerProcess != None:
				self.WebServerProcess.kill()
				self.WebServerProcess = None
			master.destroy()
	# end do_exit

	def do_open_socket(self, master, port=8000):
		if self.WebServerProcess == None:
			self.WebServerProcess = subprocess.Popen("python FileServer.py -p %d" % port)
			self.status_bar.set("WebServer running on port %d", port)
			self.status_bar.set_weblabel("WebServer Running (PORT %d)", port)
		else:
			tkmb.showerror("WebSocket Error", "WebSocket service is already running.")
	# end do_open_socket

	def do_kill_socket(self, master):
		if self.WebServerProcess != None:
			self.WebServerProcess.kill()
			self.WebServerProcess = None
			self.status_bar.set("%s", "WebServer service killed.")
			self.status_bar.set_weblabel("%s", "WebServer Offline")
		else:
			tkmb.showerror("WebSocket Error", "No WebSocket service is running.")
	# end do_kill_socket

	def do_push_game_details(self, master, game, current_mission):
		FileServer.generate_game_files(self.game, current_mission)
		print "Game details pushed to WebSocket."
	# end do_push_game_details
	# -------------------------------------------------------------------------------


if __name__ == "__main__":
	root = tk.Tk()
	root.withdraw()
	tracker = GameTracker(root)