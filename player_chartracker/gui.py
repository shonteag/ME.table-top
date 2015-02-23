import Tkinter as tk
import ScrolledText as st
import tkMessageBox as tkmb
import tkFileDialog as tkfd
import tkSimpleDialog as tksd
import ttk

import urllib

from tkinterext.tkStatusBar import StatusBar


class Downloader(tk.Toplevel):
	def __init__(self, master, splash):
		folders = ['xml', 'res']

		tk.Toplevel.__init__(self, master)
		self.title="Download Wizard"

		self.w, self.h = 500, 400
		self.window_w, self.window_h = self.winfo_screenwidth(), self.winfo_screenheight() 
		self.geometry("%dx%d+%d+%d" % (self.w, self.h, (self.window_w-(self.window_w/2)-(self.w/2)), (self.window_h-(self.window_h/2)-(self.h/2))))

		self.resizable(0,0)

		# draw components	
		self.draw_components(master, splash, step=1)

	# end __init__

	def draw_components(self, master, splash, step=1, address=None):
		try:
			self.f_main.destroy()
		except:
			pass
		self.f_main = tk.Frame(self)
		self.f_main.pack(fill=tk.BOTH, expand=1)

		bg_img = tk.PhotoImage(file='res/img/splash.gif')
		bg_label = tk.Label(self.f_main, image=bg_img)
		bg_label.photo = bg_img
		bg_label.place(x=0, y=0, relheight=1)

		self.f_container = tk.Frame(self.f_main, bg='lightgray', padx=3, pady=3)
		self.f_container.place(x=100, y=0, relheight=1, width=400)

		
	# end draw_components

class Splash(tk.Toplevel):
	def __init__(self, master):

		tk.Toplevel.__init__(self, master)
		self.title("Character Tracker")

		# geometry
		self.w, self.h = 300, 400 
		self.window_w, self.window_h = self.winfo_screenwidth(), self.winfo_screenheight()
		self.geometry("%dx%d+%d+%d" % (self.w, self.h, (self.window_w-(self.window_w/2)-(self.w/2)), (self.window_h-(self.window_h/2)-(self.h/2))))

		# styling
		self.theme = ttk.Style()
		self.theme.theme_use('clam')

		self.overrideredirect(1)

		self.draw_components(master)

		self.mainloop()
	# end __init__

	def draw_components(self, master):
		self.f_main = tk.Frame(self, bd=4, relief=tk.RAISED, bg='black')
		self.f_main.pack(fill=tk.BOTH, expand=1)

		# background image
		bg_img = tk.PhotoImage(file='res/img/splash.gif')
		bg_label = tk.Label(self.f_main, image=bg_img)
		bg_label.photo = bg_img
		bg_label.place(x=0, y=0, relwidth=1, relheight=1)

		# buttons
		# load button
		b_load_char = ttk.Button(self.f_main, text='Load Character', command=lambda: self.do_load_char(master))
		b_load_char.place(x=100, y=200, relwidth=.63)
		# new button
		b_new_char = ttk.Button(self.f_main, text='New Character', command=lambda: self.do_new_char(master))
		b_new_char.place(x=100, y=240, relwidth=.63)
		# sync
		b_sync = ttk.Button(self.f_main, text='Sync Game Files', command=lambda: self.do_sync_files(master))
		b_sync.place(x=100, y=280, relwidth=.63)

		# exit
		b_exit = ttk.Button(self.f_main, text='Exit Character Tracker', command=lambda: master.destroy())
		b_exit.place(x=100, y=340, relwidth=.63)
	# end draw_components

	def do_load_char(self, master):
		pass
	# end do_load_char

	def do_new_char(self, master):
		pass
	# end do_new_char

	def do_sync_files(self, master):
		self.withdraw()
		downloader = Downloader(master, self)
	# end do_sync_files
# end Splash




if __name__ == "__main__":
	root = tk.Tk()
	root.withdraw()

	# spalsh screen first to ask
	splash = Splash(root)

