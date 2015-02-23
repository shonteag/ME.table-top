import SimpleHTTPServer
import SocketServer
import sys
import subprocess

from WeaponHandler import Weapon
from ArmorHandler import Armor
from ItemHandler import Item
from LootHandler import LootHandler
from Game import Game
from Mission import Mission
from Encounter import Encounter
from Enemy import Enemy
import static

import subprocess

class FileServer(object):
	PORT = 8000
	Handler = None
	httpd = None

	def __init__(self, port=8000):
		self.PORT = port
		self.Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
		self.httpd = SocketServer.TCPServer(("", self.PORT), self.Handler)

		self.httpd.serve_forever()
	# end __init__
# end FileServer

def _write_header(file_object, current_page):
	file_object.write("""
	<style>
	#header a {
	width: 100px;
	height: 30px;
	color: black;
	float: left;
	underline: none;
	padding-top:10px;
	padding-bottom:10px;
	text-align:center;
	}
	#header a:hover {
	background-color:white;
	}
	#header a.active {
	background-color:white;
	}

	body {
	font-family: "Trebuchet MS", Helvetica, sans-serif;
	background-color:grey;
	}

	h1, h2, h3, h4, h5 {
	margin-bottom:3px;
	}
	</style>
	""")
	file_object.write("<div id=\"header\" style=\"width:100%;height:50px;background-color:lightgray;color:white;position:fixed;border-bottom:2px white;padding:0px; margin:-55 -8 0 -8\">")
	
	file_object.write("<a href=\"index.html\" ")
	if current_page == "game":
		file_object.write("class=\"active\"")
	file_object.write(">Game</a>")

	file_object.write("<a href=\"hub.html\" ")
	if current_page == "hub":
		file_object.write("class=\"active\"")
	file_object.write(">Current Hub</a>")	

	file_object.write("<a href=\"encounter.html\" ")
	if current_page == "encounter":
		file_object.write("class=\"active\"")
	file_object.write(">Encounter</a>")

	file_object.write("<a href=\"loot.html\" ")
	if current_page == "loot":
		file_object.write("class=\"active\"")
	file_object.write(">Loot</a>")

	file_object.write("</div>")

def generate_game_files(game, priority_mission=None):
	# first, clear out index.html
	game_file = open('index.html', 'w')
	game_file.truncate()

	# this will be the HTML and JavaScript/JQUERY to write out to "index.html"
	game_file.write("<html><body><div style='width:100%;margin-top:55px;'>")

	_write_header(game_file, "game")

	game_file.write("<h2>" + str(game.name) + "</h2> <i>Started on " + str(game.date_started) + "</i><br />")
	game_file.write("<hr />")
	if priority_mission != None and isinstance(priority_mission, Mission):
		game_file.write("<h3> Current PRIORITY Mission: <span style='color:yellow;'>" + str(priority_mission.name) + "</span></h3>")
		game_file.write("<i>Recommended Level <span style='color:yellow'>" + str(priority_mission.level) + "</span>, Difficulty <span style='color:yellow'>" + str(priority_mission.difficulty) + "</span></i><br />")
		game_file.write("<div style='float:left;width:50%;background-color:white;margin:10px;border-radius:5px;padding:2px;'>" + str(priority_mission.description) + "</div>")
		game_file.write("<div style='float:left;width:50%;background-color:white;margin:10px;border-radius:5px;padding:2px;'>" + str(priority_mission.rewards) + "</div>")


	game_file.write("</div></body></html>")
	game_file.close()

def generate_hub_files(planet, area):
	hub_file = open('hub.html', 'w')
	hub_file.truncate()

	hub_file.write("<html><body><div style='width:100%;margin-top:55px;'>")
	_write_header(hub_file, "hub")

	hub_file.write("<h2>Planet <span style='color:yellow'>" + str(planet.name) + "</span>, Area <span style='color:yellow'>" + str(area.name) + "</span></h2>")
	hub_file.write("<i>Recommended Level <span style='color:yellow'>" + str(area.level) + "</span>, Average Difficulty <span style='color:yellow'>" + str(area.difficulty) + "</span></i><br />")
	hub_file.write(str(area.description) + "<br /><hr />")
	hub_file.write("""
	<script type="text/javascript">
	<!--
    function toggle_visibility(id) {
       var e = document.getElementById(id);
       if(e.style.display == 'block')
          e.style.display = 'none';
       else
          e.style.display = 'block';
    }
	//-->
	</script>
	""")

	#missions
	hub_file.write("<h4 onclick=\"toggle_visibility('missions')\">Missions</h4>")
	hub_file.write("<div id='missions' style='width:100%;background-color:white;'>")

	for mindex, mission in enumerate(area.missions):
		hub_file.write("<div style='width:100%;margin:5px;background-color:lightgray;box-shadow:3px 3px 2px gray;border-radius:2px;padding:2px;'>")
		hub_file.write("<b>" + str(mission.name) + "</b>, Level " + str(mission.level) + ", Difficulty (1-4) " + str(mission.difficulty) + "<br />")
		hub_file.write("<div style='width:100%;margin:4px;'>" + str(mission.description) + "</div>")
		hub_file.write("<div style='width:100%;margin:4px;'>" + str(mission.rewards) + "</div>")
		hub_file.write("</div>")

	hub_file.write("</div>")

	#stores
	hub_file.write("<h4 onclick=\"toggle_visibility('store')\">Stores</h4>")
	hub_file.write("<div id='Stores' style='width:100%;'>")


	hub_file.write("</div>")

	hub_file.write("</div></body></html>")
	hub_file.close()

def generate_encounter_files(encounter):
	# first clear out encounter.html
	encounter_file = open('encounter.html', 'w')
	encounter_file.truncate()

	# this will be current encounter
	encounter_file.write("<html><body><div style='width:100%;margin-top:55px;'>")
	_write_header(encounter_file, "encounter")

	encounter_file.write("<h2>Encounter: <span style='yellow'>" + str(encounter.name) + "</span></h2>")
	encounter_file.write("Level <span style='yellow'>" + str(encounter.level) + "</span>, Difficulty <span style='yellow'>" + str(encounter.difficulty) + "</span><br /><hr /><br />")

	# enemies
	encounter_file.write("<table style='width:100%;background-color:black;color:white;'>")
	for index, enemy in enumerate(encounter.enemies):
		encounter_file.write("<tr>")
		# image
		encounter_file.write("<td></td>")
		# name/level/difficulty/class/race
		encounter_file.write("<td><b><span style='color:'"+ static.DIFFICULTY_COLORS[enemy.properties['difficulty'] - 1] +">" + str(enemy.properties['name']) + "</span></b><br />")
		encounter_file.write("<td>"+ str(enemy.properties['race']) + " " + str(enemy.properties['class_key']) + "<br />")
		encounter_file.write("<i>Level " + str(enemy.properties['level']) + " " + str(static.DIFFICULTY_NAMES[enemy.properties['difficulty'] - 1]) + "</i></td>")
		# shield/armor/health max/current
		encounter_file.write("<td><span style='color:blue'>" + str(enemy.properties['shield']) + "</span> / <span style='color:blue'>" + str(enemy.properties['max_shield']) + "</span><br />")
		encounter_file.write("<span style='color:yellow'>" + str(enemy.properties['armor']) + "</span> / <span style='color:yellow'>" + str(enemy.properties['max_armor']) + "</span><br />")
		encounter_file.write("<span style='color:red'>" + str(enemy.properties['health']) + "</span> / <span style='color:red'>" + str(enemy.properties['max_health']) + "</span></td>")
		# percents
		try:
			armor_p = str(int((float(enemy.properties['armor'])/float(enemy.properties['max_armor'])) * 100.0))
		except:
			armor_p = "0"

		try:
			health_p = str(int((float(enemy.properties['health'])/float(enemy.properties['max_health'])) * 100.0))
		except:
			health_p = "0"

		try:
			shield_p = str(int((float(enemy.properties['shield'])/float(enemy.properties['max_shield'])) * 100.0))
		except:
			shield_p = "0"

		encounter_file.write("<td><span style='color:blue'>" + shield_p + "%</span><br />")
		encounter_file.write("<span style='color:yellow'>" + armor_p + "%</span><br />")
		encounter_file.write("<span style='color:red'>" + health_p + "%</span></td>")
		# recharge, DR
		encounter_file.write("<td><span style='color:blue'>+" + str(enemy.properties['shield_recharge']) + "</span> shield per turn<br />")
		encounter_file.write("<span style='color:yellow'>-" + str(enemy.properties['damage_reduction']) + "</span> damage w/ armor<br /></td>")


		encounter_file.write("</tr>")
	encounter_file.write("</table></div></body></html>")
	encounter_file.close()

def generate_loot_file(loot_table):
	loot_file = open('loot.html', 'w')

	# wipe loot table
	loot_file.truncate()

	# write new loot
	loot_file.write("<html><body><div style='width:100%;margin-top:55px;'><table>")

	# header
	_write_header(loot_file, "loot")

	loot_file.write("""
	<style>
	tr {
		box-shadow: 4px 4px 2px #888888;
		background-color: black;
		color: white;
		border: 1px solid;
		border-radius: 20px;
	}

	td {
		padding: 2px 2px 2px 2px;
	}
	</style>
	""")

	for index, loot_piece in enumerate(loot_table[1]):
		loot_file.write("<tr>")
		# image
		loot_file.write("<td><img src=\"" + str(loot_piece.icon_path) + "\" /></td>")

		if isinstance(loot_piece, Armor) or isinstance(loot_piece, Weapon):
			# name / manufacturer
			loot_file.write("<td><b><span style=\"color:" + static.QUALITIES_COLOR[int(loot_piece.quality) + 1] + "\">" + str(loot_piece.name) + " " + loot_piece.type_name + "</span></b><br />")
			loot_file.write("Level " + str(loot_piece.level) + "<br />")
			loot_file.write(str(loot_piece.man_name) + "</td>")

			if isinstance(loot_piece, Weapon):
				loot_file.write("<td>DAMAGE<br /><b>" + str(loot_piece.shots_per_round) + "</b> x <b>D" + str(loot_piece.damage_per_shot) + "</b></td>")
				loot_file.write("<td>CRIT<br /><b>" + str(loot_piece.crit_chance) + " chance</b>, <b>" + str(loot_piece.crit_multiplier) + " multiplier</b></td>")
				loot_file.write("<td>MOD SLOTS<br /><b>" + str(loot_piece.mod_slots) + "</b></td>")

				loot_file.write("<td>")
				if loot_piece.mod_types != None and loot_piece.mod_types != []:
					loot_file.write("Modable<br />")
					for slot in loot_piece.mod_types:
						loot_file.write("<span style=\"color:" + static.QUALITIES_COLOR[int(loot_piece.quality) + 1] + "\">" + str(slot) + "</span><br />")
				loot_file.write("</td>")

				loot_file.write("<td>")
				if loot_piece.rolls != None:
					for roll in loot_piece.rolls:
						try:
							loot_file.write("<span style=\"color:" + static.QUALITIES_COLOR[int(loot_piece.quality) + 1] + "\">" + str(roll).split(":")[0] + ":</span> " + str(roll).split(":")[1] + "<br />")
						except:
							loot_file.write("<span style=\"color:" + static.QUALITIES_COLOR[int(loot_piece.quality) + 1] + "\">" + str(roll) + "</span><br />")
				loot_file.write("</td>")

				loot_file.write("<td>")
				if loot_piece.specials != "" and loot_piece.specials != None:
					loot_file.write(loot_piece.specials)
				loot_file.write("</td>")

			if isinstance(loot_piece, Armor):
				loot_file.write("<td>SHIELD<br /><b>" + str(loot_piece.max_shield) + " shield</b>, <b>" + str(loot_piece.shield_recharge) + " recharge</b></td>")
				loot_file.write("<td>DR<br /><b>" + str(loot_piece.damage_reduction) + "</b></td>")
				loot_file.write("<td>MOD SLOTS<br /><b>" + str(loot_piece.mod_slots) + "</b></td>")
				
				loot_file.write("<td>")
				if loot_piece.specials != "" and loot_piece.specials != None:
					loot_file.write(loot_piece.specials)
				loot_file.write("</td>")

		elif isinstance(loot_piece, Item):
			loot_file.write("<td><b><span style=\"color:" + static.QUALITIES_COLOR[int(loot_piece.quality) + 1] + "\">" + str(loot_piece.name) + "</span></b></td>")
			loot_file.write("<td><b><span style=\"color:" + static.QUALITIES_COLOR[int(loot_piece.quality) + 1] + "\">"+ str(loot_piece.value) +"</span></b> Credits</td>")
			loot_file.write("<td></td>")
			loot_file.write("<td></td>")
			loot_file.write("<td>"+ str(loot_piece.description) +"</td>")

		loot_file.write("</tr>")
	
	loot_file.write("<tr><td><img src=\"res/icon/credits.gif\" /></td>")
	loot_file.write("<td>" + str(loot_table[0]) + " credits</td></tr>")
	loot_file.write("</table>")

	loot_file.write("</body></html>")
	loot_file.close()

if __name__ == "__main__":
	if "-p" in sys.argv:
		port = int(sys.argv[sys.argv.index("-p") + 1])
	else:
		port = 8000

	server = FileServer(port=port)