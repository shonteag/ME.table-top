import Tkinter as tk


class StatusBar(tk.Frame):
	def __init__(self, master):
		tk.Frame.__init__(self, master)
		self.weblabel = tk.Label(self, bd=1, relief=tk.SUNKEN, anchor=tk.W, width=30)
		self.weblabel.pack(side=tk.RIGHT)
		self.label = tk.Label(self, bd=1, relief=tk.SUNKEN, anchor=tk.W)
		self.label.pack(fill=tk.X)

	def set(self, format, *args):
		self.label.config(text=format % args)
		self.label.update_idletasks()

	def clear(self):
		self.label.config(text="")
		self.label.update_idletasks()

	def set_weblabel(self, format, *args):
		self.weblabel.config(text=format % args)
		self.weblabel.update_idletasks()
# end StatusBar
