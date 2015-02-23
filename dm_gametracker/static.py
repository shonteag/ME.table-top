'''
static.py
Houses static values for passing information between classes.
'''

# State variables
STATES = ['', 'inactive', 'active', 'complete']
INACTIVE = 'inactive'
ACTIVE   = 'active'
COMPLETE = 'complete'

POWER_BIOTIC = 'biotic'
POWER_TECH = 'tech'

CLASSES = ['', 'SOL', 'ENG', 'ADT', 'VAN', 'SEN', 'INF']
CLASS_SOLDIER     = 'SOL'
CLASS_ENGINEER    = 'ENG'
CLASS_ADEPT       = 'ADT'
CLASS_VANGUARD    = 'VAN'
CLASS_SENTINEL    = 'SEN'
CLASS_INFILTRATOR = 'INF'
CLASS_NONE        = 'N/A'

ROLES = ['', 'support', 'tank', 'dps', 'none']
ROLE_SUPPORT = 'support'
ROLE_TANK    = 'tank'
ROLE_DPS     = 'dps'
ROLE_NONE    = 'none'

RACES = ['', 'human', 'asari', 'turian', 'salarian', 'other']
RACE_HUMAN    = 'human'
RACE_ASARI    = 'asari'
RACE_TURIAN   = 'turian'
RACE_SALARIAN = 'salarian'
RACE_OTHER    = 'other'

DIFFICULTIES = [1,2,3,4]
DIFFICULTY_NAMES = ['Trash', 'Average', 'Elite', 'Champion']
DIFFICULTY_COLORS = ['white', 'yellow', 'orange', 'red']

STATS_DEFAULT = {'ACC':8, 'CON':8, 'FIT':8, 'BIF':8, 'INT':8, 'AWR':8}

WEAPON_DEFAULT = "4, 4"


WEAPON_TYPES = ['', 'AR', 'SR', 'HP', 'SMG', 'SH', 'HW']
WEAPON_NAMES = ['', 'Assault Rifle', 'Sniper Rifle', 'Heavy Pistol', 'Submachine Gun', 'Shotgun', 'Heavy Weapon**']
WEAPON_TYPE_AR  = 'AR'	# assault rifle
WEAPON_TYPE_SR  = 'SR'	# sniper rifle
WEAPON_TYPE_HP  = 'HP'	# heavy pistol
WEAPON_TYPE_SMG = 'SMG'	# sub machine gun
WEAPON_TYPE_SH  = 'SH'	# shotgun
WEAPON_TYPE_HW  = 'HW'	# heavy weapon

QUALITIES_VALUES = [-1,0,1,2,3,4]
QUALITIES_NAMES = ['', 'Trash', 'Common', 'Industrial', 'Military', 'Experimental']
QUALITIES_COLOR = ['', 'darkgrey', 'white', 'blue', 'purple', 'orange']
QUALITY_TRASH        = 0
QUALITY_COMMON       = 1
QUALITY_INDUSTRIAL   = 2
QUALITY_MILITARY     = 3
QUALITY_EXPERIMENTAL = 4


TECH_COMBO_MULTIPLIER = 1.4
BIOTIC_COMBO_MULTIPLIER = 1.4


# LOOT STATICS
quality_chart = {'very_low':[7000, 10000, -1, -1, -1],
				 'low':[5249, 9924, 9994, 9999, 10000],
				 'average':[4850, 8350, 9550, 9950, 10000],
				 'good':[2450, 6950, 8950, 9750, 10000],
				 'very_good':[1400, 5400, 7900, 9400, 10000],
				 'exceptional':[-1, 3000, 6000, 8500, 10000]}
quality_credits = {'very_low':[5, 10, 0, 0, 0],
				   'low':[25, 70, 150, 275, 370],
				   'average':[100, 160, 300, 500, 1000],
				   'good':[200, 350, 600, 750, 1000],
				   'very_good':[400, 600, 800, 1000, 1200],
				   'exceptional':[600, 900, 1300, 1600, 2000]}
credit_rolls = {'very_low':10,
				'low':15,
				'average':20,
				'good':30,
				'very_good':35,
				'exceptional':40}
chest_types = ['very_low', 'low', 'average', 'good', 'very_good', 'exceptional']



# WEAPON STATS
weapon_stats = {
	"AR":["Fire Type: Fragmented Shot", "Fire Type: Impact", "Fire Type: Overload",
	      "Phasing Rounds: 200% damage to shields, -50% damage to armor", "Armor Piercing: Ignore DR", "Phasing Rounds: Ignore Shield, 0 damage to armor",
	      "Aim Assist: Increases accuracy by 25-50%", "Range Bonus: Medium to Long range", "Crit Mult: +25% to +50%",
	      "Mod Slots: 1-5", "Extra Roll", "Bonus Roll",
	      "Permanent Ammo Mod: Incendiary", "Permanent Ammo Mod: Phasic", "Permanent Ammo Mod: Cryo",
	      "Permanent Scope Mod: Scope 1", "Permanent Scope Mod: Scope 2",
	      "Permanent Frame Mod: Light-weight Materials", "Permanent Frame Mod: Scout/Recon Frame",
	      "Permanent Stock Mod: Recoil Reduction",
	      "Permanent Barrel Mod: Extended Barrel", "Permanent Barrel Mod: Silencer", "Permanent Barrel Mod: Omni-blade"],
	"SH":["Fire Type: Fragmented Shot", "Fire Type: Impact", "Fire Type: Overload",
	      "Phasing Rounds: 200% damage to shields, -50% damage to armor", "Armor Piercing: Ignore DR", "Phasing Rounds: Ignore Shield, 0 damage to armor",
	      "Aim Assist: Increases accuracy by 25-50%", "Crit Mult: +25% to +50%",
	      "Mod Slots: 1-5", "Extra Roll", "Bonus Roll",
	      "Permanent Ammo Mod: Incendiary", "Permanent Ammo Mod: Phasic", "Permanent Ammo Mod: Cryo",
	      "Permanent Scope Mod: Scope 1", "Permanent Scope Mod: Scope 2",
	      "Permanent Frame Mod: Light-weight Materials",
	      "Permanent Stock Mod: Recoil Reduction",
	      "Permanent Barrel Mod: Extended Barrel", "Permanent Barrel Mod: Omni-blade"],
	"HP":["Fire Type: Fragmented Shot", "Fire Type: Impact", "Fire Type: Overload",
	      "Phasing Rounds: 200% damage to shields, -50% damage to armor", "Armor Piercing: Ignore DR", "Phasing Rounds: Ignore Shield, 0 damage to armor",
	      "Aim Assist: Increases accuracy by 25-50%", "Range Bonus: Medium to Long range", "Crit Mult: +25% to +50%",
	      "Mod Slots: 1-5", "Extra Roll", "Bonus Roll",
	      "Permanent Ammo Mod: Incendiary", "Permanent Ammo Mod: Phasic", "Permanent Ammo Mod: Cryo",
	      "Permanent Scope Mod: Scope 1", "Permanent Scope Mod: Scope 2",
	      "Permanent Frame Mod: Light-weight Materials", "Permanent Frame Mod: Scout/Recon Frame",
	      "Permanent Stock Mod: Recoil Reduction",
	      "Permanent Barrel Mod: Extended Barrel", "Permanent Barrel Mod: Silencer", "Permanent Barrel Mod: Omni-blade"],
	"SMG":["Fire Type: Fragmented Shot", "Fire Type: Impact", "Fire Type: Overload",
	       "Phasing Rounds: 200% damage to shields, -50% damage to armor", "Armor Piercing: Ignore DR", "Phasing Rounds: Ignore Shield, 0 damage to armor",
	       "Aim Assist: Increases accuracy by 25-50%", "Range Bonus: Medium to Long range", "Crit Mult: +25% to +50%",
	       "Mod Slots: 1-5", "Extra Roll", "Bonus Roll",
	       "Permanent Ammo Mod: Incendiary", "Permanent Ammo Mod: Phasic", "Permanent Ammo Mod: Cryo",
	       "Permanent Scope Mod: Scope 1", "Permanent Scope Mod: Scope 2",
	       "Permanent Frame Mod: Light-weight Materials", "Permanent Frame Mod: Scout/Recon Frame",
	       "Permanent Stock Mod: Recoil Reduction",
	       "Permanent Barrel Mod: Extended Barrel", "Permanent Barrel Mod: Silencer", "Permanent Barrel Mod: Omni-blade"],
	"SR":["Fire Type: Fragmented Shot", "Fire Type: Impact", "Fire Type: Overload",
	      "Phasing Rounds: 200% damage to shields, -50% damage to armor", "Armor Piercing: Ignore DR", "Phasing Rounds: Ignore Shield, 0 damage to armor",
	      "Aim Assist: Increases accuracy by 25-50%", "Range Bonus: Medium to Long range", "Crit Mult: +25% to +50%",
	      "Mod Slots: 1-5", "Extra Roll", "Bonus Roll",
	      "Permanent Ammo Mod: Incendiary", "Permanent Ammo Mod: Phasic", "Permanent Ammo Mod: Cryo",
	      "Permanent Scope Mod: Scope 1", "Permanent Scope Mod: Scope 2",
	      "Permanent Frame Mod: Light-weight Materials",
	      "Permanent Stock Mod: Recoil Reduction",
	      "Permanent Barrel Mod: Extended Barrel", "Permanent Barrel Mod: Silencer", "Permanent Barrel Mod: Omni-blade"],
}
mod_slot_types = ['Barrel', 'Ammo', 'Scope', 'Stock', 'Frame']