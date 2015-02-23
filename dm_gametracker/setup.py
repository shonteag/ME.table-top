'''
To EXE
'''

from distutils.core import setup
import py2exe, sys, os

sys.argv.append('py2exe')

setup(
	options = {
		'py2exe':{
			'compressed':1,
			'optimize':2,
			'bundle_files':3,
			'dist_dir':'dist',
			'xref':False,
			'skip_archive':False,
			'ascii':False,
		}
	},
	zipfile=None,
	console=['Game Tracker.py']
)