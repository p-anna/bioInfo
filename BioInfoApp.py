import style
from SpadesPopUp import SpadesPopUp
from AbyssPopUp import AbyssPopUp
from VelvetPopUp import VelvetPopUp
from tkinter import *
from tkinter import ttk

class BioInfoApp():
	def __init__(self, master):
		
		####  Map of assemblies and their classes ###################

		assemblyClassMaker = {}
		assemblyClassMaker["Spades"] = lambda root : SpadesPopUp(root, "Spades")
		assemblyClassMaker["ABySS"] = lambda root : AbyssPopUp(root, "ABySS")
		assemblyClassMaker["Velvet"] = lambda root : VelvetPopUp(root, "Velvet")

	
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

		ttk.Label(self.frame, text = "").grid(row=self.rowcount) # instead of a vertical placeholder
		
		################### end of __init__
			
		
	def addButton(self, assemblyName, classMaker): #adding a button for an assembly
		ttk.Label(self.frame, text="Run the " + assemblyName + " assembly:", style="C.TLabel").grid(row=self.rowcount, column=0, sticky='w')
		self.abyssInputButt = ttk.Button(self.frame, text=assemblyName, command= lambda: self.openAssembly(classMaker))
		self.abyssInputButt.grid(row=self.rowcount, column=1, sticky='w', padx=20)
		self.rowcount += 1

	def openAssembly(self, classMaker): #function when assembly button clicked
		root = Toplevel(self.master)    
		myApp = classMaker(root)        #new window for assembly
