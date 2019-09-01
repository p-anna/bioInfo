import tkinter as tk
from tkinter import *
from tkinter import ttk


class AddicionalParamParent:
	def __init__(self, master, possibleParameters, prevWindow):
		self.possibleParameters = possibleParameters
		self.master = master
		self.prevWindow = prevWindow
        
		rowcount = 0 # row index for grid of main frame
        
		frame = ttk.Frame(master, style="M.TFrame")
		frame.pack(fill='both', expand=True)

		#self.possibleParameters.paramDesc[tag][0] first element o f tuple
		for tag in self.possibleParameters.tags:
			ttk.Checkbutton(frame, text = tag + " - " +  self.possibleParameters.paramDesc[tag][0], style = "P.TCheckbutton", variable = self.possibleParameters.params[tag]).grid(column=0, row=rowcount, sticky = "w")
			rowcount += 1


		buttonOk2 = ttk.Button(frame, text = "Ok", command = self.returnToPrevWindow)
		buttonOk2.grid(column=0, row=rowcount)
		rowcount += 1

	def returnToPrevWindow(self):
		self.prevWindow.showAddicionalParams()
		self.master.destroy()
        
class ChosenParams:
	def __init__(self):
		self.tags = ["flag=1", "int=2", "intlist=3", "file=4", "float=5", "options=6", "text=7"]
#					
		self.params = {}

		for tag in self.tags:
			self.params[tag] = IntVar(0) # variable for Checkbutton for every parameter

		self.paramDesc = {}

		# self.paramDesc[oznaka] = ("opis", tip, options) tip: flag=1, int=2, intlist=3, file=4,
		# float=5, options = 6, text=7

		self.paramDesc["flag=1"] = ("", 1)		
		self.paramDesc["int=2"] = ("", 2)
		self.paramDesc["intlist=3"] = ("", 3)
		self.paramDesc["file=4"] = ("", 4)
		self.paramDesc["float=5"] = ("", 5)
		self.paramDesc["options=6"] = ("", 6, ["a", "b", "c"])
		self.paramDesc["text=7"] = ("", 7)
