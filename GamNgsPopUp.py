from ParentPopUp import ParentPopUp
from AddicionalParamParent import PossibleParamsParent
from tkinter import *

class GamNgsPopUp(ParentPopUp):
	def __init__(self, master, name, possibleParamClassInit):
		super().__init__(master, name, possibleParamClassInit)
		
		#Frame: self.readProperties ----------------------------------------------------------

		# ASSEMBLY LIST
		#("assembly name", "terminalTag")
		self.assemblyList = [("Abyss", "abyss/abyss-contigs.fa"),
							 ("Velvet", "velvet/contigs.fa"),
							 ("Spades", "spades/contigs.fasta")]

		indexAssembly = 0        #index of frame
		self.assemblyMaster = StringVar()   #variable for radioButtons with assemblies
		
		# We put two categories in a row in the frame self.readProperties from ParentPopUp
		for master in self.assemblyList:
			# value of the radioButton is the index in self.assemblyList
			rb = ttk.Radiobutton(self.readProperties, style="1.TRadiobutton", text=master[0], variable=self.assemblyMaster, value=master[1])
			rb.grid(row=int(indexAssembly / 3), column=indexAssembly % 3, sticky='w')
			indexAssembly += 1
			
		self.assemblyMaster.set("abyss/abyss-contigs.fa")

		indexAssembly += 1
		ttk.Separator(self.readProperties, orient="horizontal").grid(row=int(indexAssembly / 3), columnspan=3, sticky='we')
		indexAssembly +=2

		
		self.assemblySlave = StringVar()
		
		for slave in self.assemblyList:
			# value of the radioButton is its terminalTag
			rb = ttk.Radiobutton(self.readProperties, style="1.TRadiobutton", text=slave[0], variable=self.assemblySlave, value=slave[1])
			rb.grid(row=int(indexAssembly / 3), column=indexAssembly % 3, sticky='w')
			indexAssembly += 1

		self.assemblySlave.set("velvet/contigs.fa")

		indexAssembly += 1
		ttk.Separator(self.readProperties, orient="horizontal").grid(row=int(indexAssembly / 3), columnspan=3, sticky='we')
		indexAssembly +=2

		#("read categories", "terminalTag")
		self.readCategList = [("Forward pair", "fp"),
							 ("Reverse pair", "rp")]
		
		self.readCategVar = StringVar()

		for readCateg in self.readCategList:
			# value of the radioButton is its terminalTag
			rb = ttk.Radiobutton(self.readProperties, style="1.TRadiobutton", text=readCateg[0], variable=self.readCategVar, value=readCateg[1])
			rb.grid(row=int(indexAssembly / 3), column=indexAssembly % 3, sticky='w')
			indexAssembly += 1

		self.readCategVar.set("fp")	

	def getFileType(self): #type of input file
		return (self.assemblyMaster.get(), self.assemblyMaster.get(), self.readCategVar.get())

	def whereProgram(self):
		return "."
	
	def runParameterBlocks(self):	
		return [[]]

		


class PossibleParamsGamNgs(PossibleParamsParent):
	def __init__(self):
		

		tags = ["Expected size of the genome:"]

		#("param description", type, isOptionalParam)
		# type: ["flag=1", "int=2", "intlist=3", "file=4", "float=5", "options=6", "text=7", "dir=8"]
		self.paramDesc = {}

		# FIXED PARAMETERS
		self.paramDesc["Expected size of the genome:"] = ("Expected size of the genome:", 2, False)

		super().__init__(tags)
