import style
from SpadesPopUp import *
from AbyssPopUp import *
from VelvetPopUp import *
from GamNgsPopUp import *
from tkinter import *
from tkinter import ttk

class BioInfoApp():
	def __init__(self, master):
		
		####  Map of assemblies and their classes ###################

		assemblyClassMaker = {}
		assemblyClassMaker["SPAdes"] = lambda root : SpadesPopUp(root, "SPAdes", lambda : PossibleParamsSpades())
		assemblyClassMaker["ABySS"] = lambda root : AbyssPopUp(root, "ABySS", lambda : PossibleParamsAbyss())
		assemblyClassMaker["Velvet"] = lambda root : VelvetPopUp(root, "Velvet", lambda : PossibleParamsVelvet())

		mergerClassMaker = lambda root : GamNgsPopUp(root, "GAM-NGS", lambda : PossibleParamsGamNgs())

	
		#############################################################
		
		style.styleTheWindow() # style of GUI elements
		self.rowcount = 0      # row index for grid of main frame
		self.master = master   # parent window

		self.frame = ttk.Frame(master, style="M.TFrame") #main frame
		self.frame.pack(fill='both', expand=True)

		ttk.Label(self.frame, text="MainWindow", style="N.TLabel").grid(row=self.rowcount, columnspan=2, sticky='w')
		self.rowcount += 1

		for assemblyName in assemblyClassMaker.keys(): #for every assembly add a button to run it
			self.addButton(assemblyName, assemblyClassMaker[assemblyName])
			
		self.gamNgsButton = ttk.Button(self.frame, text="Merging with GAM-NGS", command= lambda: self.openProgram(mergerClassMaker))
		self.gamNgsButton.grid(row=self.rowcount, columnspan=2, padx = 20, pady = 20)
		self.rowcount += 1
	
		################### end of __init__ function ################
			
		
	def addButton(self, assemblyName, classMaker): #adding a button for an assembly
		ttk.Label(self.frame, text="Run the " + assemblyName + " assembly:", style="C.TLabel").grid(row=self.rowcount, column=0, sticky='w')
		self.abyssInputButt = ttk.Button(self.frame, text=assemblyName, command= lambda: self.openProgram(classMaker))
		self.abyssInputButt.grid(row=self.rowcount, column=1, sticky='w', padx=20)
		self.rowcount += 1

	def openProgram(self, classMaker): #function when assembly button clicked
		root = Toplevel(self.master)    
		myApp = classMaker(root)        #new window for assembly
