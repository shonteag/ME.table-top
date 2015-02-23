'''
A collection of classes and methods to be used by the GUI
to save games to and load games from pickled objects.
'''

from Game import Game
import dill


def game_to_file(file_path, game):
	save_file = open(file_path, 'wb')
	save_file.truncate()
	dill.dump(game, save_file)

def game_from_file(file_path):
	save_file = open(file_path, 'rb')
	return dill.load(save_file)