from ParentPopUp import ParentPopUp
from AddicionalParamParent import PossibleParamsParent
from tkinter import *

class GamNgsPopUp(ParentPopUp):
	def __init__(self, master, name, possibleParamClassInit):
		super().__init__(master, name, possibleParamClassInit)
		
		#Frame: self.readProperties ----------------------------------------------------------

		indexAssembly = 0        #index of frame
		self.myFolderName = name + "/"
				
		ttk.Label(self.readProperties, text="Please choose the Master assembly:", style="HP.TLabel").grid(row=int(indexAssembly / 3), columnspan=3, sticky='w')
		indexAssembly += 3

		# ASSEMBLY LIST
		#("assembly name", "terminalTag")
		self.assemblyList = [("Abyss", "abyss/abyss-contigs.fa"),
							 ("Velvet", "velvet/contigs.fa"),
							 ("Spades", "spades/contigs.fasta")]

		
		self.assemblyMaster = StringVar()   #variable for radioButtons with assemblies
		
		# We put two categories in a row in the frame self.readProperties from ParentPopUp
		for master in self.assemblyList:
			# value of the radioButton is the index in self.assemblyList
			rb = ttk.Radiobutton(self.readProperties, style="1.TRadiobutton", text=master[0], variable=self.assemblyMaster, value=master[1], command = lambda : self.nameMaster(master[0]))
			rb.grid(row=int(indexAssembly / 3), column=indexAssembly % 3, sticky='w')
			indexAssembly += 1
			
		self.assemblyMaster.set("abyss/abyss-contigs.fa")
		self.masterName = "Abyss"

		indexAssembly += 1
		ttk.Separator(self.readProperties, orient="horizontal").grid(row=int(indexAssembly / 3), columnspan=3, sticky='we')
		indexAssembly +=2

		ttk.Label(self.readProperties, text="Please choose the Slave assembly:", style="HP.TLabel").grid(row=int(indexAssembly / 3), columnspan=3, sticky='w')
		indexAssembly += 3
		
		self.assemblySlave = StringVar()
		
		for slave in self.assemblyList:
			# value of the radioButton is its terminalTag
			rb = ttk.Radiobutton(self.readProperties, style="1.TRadiobutton", text=slave[0], variable=self.assemblySlave, value=slave[1], command = lambda : self.nameSlave(master[0]))
			rb.grid(row=int(indexAssembly / 3), column=indexAssembly % 3, sticky='w')
			indexAssembly += 1

		self.assemblySlave.set("velvet/contigs.fa")
		self.slaveName = "Velvet"

		indexAssembly += 1
		ttk.Separator(self.readProperties, orient="horizontal").grid(row=int(indexAssembly / 3), columnspan=3, sticky='we')
		indexAssembly +=2

		ttk.Label(self.readProperties, text="Orientation of reads in the next input file:", style="HP.TLabel").grid(row=int(indexAssembly / 3), columnspan=3, sticky='w')
		indexAssembly += 3

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
		return (self.assemblyMaster.get(), self.assemblySlave.get(), self.readCategVar.get())

	def nameMaster(self, master):
		self.masterName = master

	def nameSlave(self, slave):
		self.slaveName = slave
		
	def whereProgram(self):
		return "."
	
	def runParameterBlocks(self):
		masterFile = self.assemblyMaster.get()
		slaveFile = self.assemblySlave.get()

		
		paramBlocks = [["cp", masterFile, self.myFolderName + self.masterName],
					   ["cp", slaveFile, self.myFolderName + self.slaveName]]

		#self.assemblies = ["abyss", "velvet", "spades"]
		#self.contigs = ["abyss/abyss-contigs.fa", "velvet/contigs.fa", "spades/contigs.fasta"]


		assemblyFileName1 = self.masterName
		faFile1 = assemblyFileName1 + ".fa"

		assemblyFileName2 = self.slaveName
		faFile2 = assemblyFileName2 + ".fa"

		
		nameOfReads1 = sort(self.inputFiles.keys())[0]
		extensionOfReads1 = ".fq"
		readsFile1 = "../" + nameOfReads1 # U ODNOSU NA GAM-NGS FOLDER MOZDA OVO TREBA MENJATI
		saiFile11 = nameOfReads1 + "1.sai" # readNum + assemblyNum
		saiFile12 = nameOfReads1 + "2.sai"

		nameOfReads2 = sort(self.inputFiles.keys())[1]
		extensionOfReads2 = ".fq"
		readsFile2 = "../" + nameOfReads2
		saiFile21 = nameOfReads2 + "1.sai"
		saiFile22 = nameOfReads2 + "2.sai"

		threadNumber = "4"

		
		return paramBlocks

		


class PossibleParamsGamNgs(PossibleParamsParent):
	def __init__(self):
		

		tags = ["Expected size of the genome:", "Thread number"]

		#("label text", "param description", type, isOptionalParam)
		# type: ["flag=1", "int=2", "intlist=3", "file=4", "float=5", "options=6", "text=7", "dir=8"]
		self.paramDesc = {}

		# FIXED PARAMETERS
		self.paramDesc["Expected size of the genome:"] = ("Expected size of the genome:", "Expected size of the genome", 2, False)

		# OPTIONAL PARAMETERS
		self.paramDesc["Thread number"] = ("Number of threads", "Number of threads", 2, True)
		super().__init__(tags)
