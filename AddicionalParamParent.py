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
			if self.possibleParameters.paramDesc[tag][3]:
				ttk.Checkbutton(frame, text = tag + " - " +  self.possibleParameters.paramDesc[tag][1], style = "P.TCheckbutton", variable = self.possibleParameters.params[tag]).grid(column=0, row=rowcount, sticky = "w")
				rowcount += 1


		buttonOk2 = ttk.Button(frame, text = "Ok", command = self.returnToPrevWindow)
		buttonOk2.grid(column=0, row=rowcount)
		rowcount += 1

	def returnToPrevWindow(self):
		self.prevWindow.showAddicionalParams()
		self.master.destroy()
		

class PossibleParamsParent:
	def __init__(self, tags):
		self.tags = tags
			
		self.params = {}

		for tag in self.tags:
			if self.paramDesc[tag][3]:
				self.params[tag] = IntVar(0) # variable for Checkbutton for every parameter
