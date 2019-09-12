from ParentPopUp import ParentPopUp
from AddicionalParamParent import PossibleParamsParent
from ResultPopUp import *
from tkinter import *
import subprocess

class GamNgsPopUp(ParentPopUp):
	def __init__(self, master, name, possibleParamClassInit):
		super().__init__(master, name, possibleParamClassInit)
		
		#Frame: self.readProperties ----------------------------------------------------------

		indexAssembly = 0        #index of frame
		self.myFolderName = name + "/"
		self.genExeptedSize = ""
		self.threadNumber = "4"
				
		ttk.Label(self.readProperties, text="Please choose the Master assembly:", style="HP.TLabel").grid(row=int(indexAssembly / 3), columnspan=3, sticky='w')
		indexAssembly += 3

		# ASSEMBLY LIST
		#("assembly name", "terminalTag")
		self.assemblyList = [("ABySS", "ABySS/abyss-contigs.fa"),
							 ("Velvet", "Velvet/contigs.fa"),
							 ("SPAdes", "SPAdes/contigs.fasta")]

		
		self.assemblyMaster = StringVar()   #variable for radioButtons with assemblies
		
		# We put two categories in a row in the frame self.readProperties from ParentPopUp
		for master in self.assemblyList:
			# value of the radioButton is the index in self.assemblyList
			rb = ttk.Radiobutton(self.readProperties, style="1.TRadiobutton", text=master[0], variable=self.assemblyMaster, value=master[1], command = lambda : self.nameMaster(master[0]))
			rb.grid(row=int(indexAssembly / 3), column=indexAssembly % 3, sticky='w')
			indexAssembly += 1
			
		self.assemblyMaster.set("ABySS/abyss-contigs.fa")
		self.masterName = "ABySS"

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

		self.assemblySlave.set("Velvet/contigs.fa")
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
		
		originalFaMaster = self.assemblyMaster.get()
		originalFaSlave= self.assemblySlave.get()

		
		subprocess.run(["cp", originalFaMaster, self.myFolderName + self.masterName + ".fa"])
		subprocess.run(["cp", originalFaSlave, self.myFolderName + self.slaveName + ".fa"])

		assemblyFileName = [self.masterName, self.slaveName]
		
		faFile = []
		for afn in assemblyFileName:
			faFile.append(afn + ".fa")

		self.nameOfReads = []
		extensionOfReads = []
		readsFile = []
		saiFile1 = []
		saiFile2 = []
		for iFileFull in sorted(self.inputFiles):
			iFile = self.onlyNameOfFile(iFileFull)
			self.nameOfReads.append(iFile)
			extensionOfReads.append(".fq")
			readsFile.append("../" + iFile)
			saiFile1.append(iFile + "1.sai")
			saiFile2.append(iFile + "2.sai")


		#for i in range(2):
		#	print("faFile: " + faFile[i])
		#	print("nameOfReads: " + self.nameOfReads[i])
		#	print("extensionOfReads: " + extensionOfReads[i])
		#	print("readsFile: " + readsFile[i])
		#	print("saiFile1: " + saiFile1[i])
		#	print("saiFile2: " + saiFile2[i])

		for tag in self.parameterLabels.keys():
			if tag == "Expected size":
				self.genExeptedSize = self.parameterValues[tag].get()
			elif tag == "Thread number":
				self.threadNumber = self.parameterValues[tag].get()
		

		
		subprocess.run(["bwa", "index", faFile[0]], cwd = self.name)
		subprocess.run(["bwa", "aln", "-o", "0", "-t", self.threadNumber, faFile[0], readsFile[0]], stdout=open(self.name + "/" + saiFile1[0], "w"), cwd = self.name)
		subprocess.run(["bwa", "aln", "-o", "0", "-t", self.threadNumber, faFile[0], readsFile[1]], stdout=open(self.name + "/" + saiFile2[0], "w"), cwd = self.name)
		sampeOut = subprocess.Popen(["bwa", "sampe", faFile[0], saiFile1[0], saiFile2[0], readsFile[0], readsFile[1]], stdout = subprocess.PIPE, cwd = self.name)
		viewOut = subprocess.Popen(["samtools", "view", "-Shu", "-"], stdin=sampeOut.stdout, stdout = subprocess.PIPE, cwd = self.name)
		sampeOut.stdout.close()
		subprocess.run(["samtools", "sort", "-", assemblyFileName[0] + ".sorted"], stdin=viewOut.stdout, cwd = self.name)
		viewOut.stdout.close()

		subprocess.run(["samtools", "index", assemblyFileName[0] + ".sorted.bam"], cwd = self.name)
		txtFile = open(self.name + "/" +  assemblyFileName[0] + ".list.txt", "w")
		subprocess.run(["echo", "-e", assemblyFileName[0] + ".sorted.bam\n 90 270"], stdout=txtFile, cwd = self.name)
		txtFile.close()

		# Slave -------------------------------------------------------------------------------------------------------------------------------------

		subprocess.run(["bwa", "index", faFile[1]], cwd = self.name)
		subprocess.run(["bwa", "aln", "-o", "0", "-t", self.threadNumber, faFile[1], readsFile[0]], stdout=open(self.name + "/" + saiFile1[1], "w"), cwd = self.name)
		subprocess.run(["bwa", "aln", "-o", "0", "-t", self.threadNumber, faFile[1], readsFile[1]], stdout=open(self.name + "/" + saiFile2[1], "w"), cwd = self.name)
		sampeOut = subprocess.Popen(["bwa", "sampe", faFile[1], saiFile1[1], saiFile2[1], readsFile[0], readsFile[1]], stdout = subprocess.PIPE, cwd = self.name)
		viewOut = subprocess.Popen(["samtools", "view", "-Shu", "-"], stdin=sampeOut.stdout, stdout = subprocess.PIPE, cwd = self.name)
		sampeOut.stdout.close()
		subprocess.run(["samtools", "sort", "-", assemblyFileName[1] + ".sorted"], stdin=viewOut.stdout, cwd = self.name)
		viewOut.stdout.close()

		subprocess.run(["samtools", "index", assemblyFileName[1] + ".sorted.bam"], cwd = self.name)

		txtFile = open(self.name + "/" + assemblyFileName[1] + ".list.txt", "w")
		subprocess.run(["echo", "-e", assemblyFileName[1] + ".sorted.bam\n 90 270"], stdout=txtFile, cwd = self.name)
		txtFile.close()

		# Merge----------------------------------------------------------------------------------------------------------------------------------------
		gamPath = "../../../../../programs/gam-ngs/bin/"
		minBlockSize = "7"

		subprocess.run([gamPath + "gam-create", "--master-bam", assemblyFileName[0] + ".list.txt", "--slave-bam", assemblyFileName[1] + ".list.txt", "--min-block-size", minBlockSize], cwd = self.name)
		subprocess.run([gamPath + "gam-merge", "--blocks-file", "out.blocks", "--master-bam", assemblyFileName[0] + ".list.txt", "--master-fasta", faFile[0],
                        "--slave-bam", assemblyFileName[1] + ".list.txt", "--slave-fasta", faFile[1], "--min-block-size", minBlockSize], cwd = self.name)

		# BAM file for assembled
		outFaFile = "out.gam.fasta"
		gamsaiFile1 = "gam" + self.nameOfReads[0] + ".sai"
		gamsaiFile2 = "gam" + self.nameOfReads[1] + ".sai"

		subprocess.run(["bwa", "index", outFaFile], cwd = self.name)


		subprocess.run(["bwa", "aln", "-o", "0", "-t", self.threadNumber, outFaFile, readsFile[0]], stdout=open(self.name + "/" + gamsaiFile1, "w"), cwd = self.name)
		subprocess.run(["bwa", "aln", "-o", "0", "-t", self.threadNumber, outFaFile, readsFile[1]], stdout=open(self.name + "/" + gamsaiFile2, "w"), cwd = self.name)
		sampeOut = subprocess.Popen(["bwa", "sampe", outFaFile, gamsaiFile1, gamsaiFile2, readsFile[0], readsFile[1]], stdout = subprocess.PIPE, cwd = self.name)
		viewOut = subprocess.Popen(["samtools", "view", "-Shu", "-"], stdin=sampeOut.stdout, stdout = subprocess.PIPE, cwd = self.name)
		sampeOut.stdout.close()
		subprocess.run(["samtools", "sort", "-", "gam.sorted"], stdin=viewOut.stdout, cwd = self.name)
		viewOut.stdout.close()

		subprocess.run(["samtools", "index", "gam.sorted.bam"], cwd = self.name)

		subprocess.run(["rm", "gam.sorted_contigsTable.csv",
						self.masterName + ".sorted_contigsTable.csv",
						self.slaveName + ".sorted_contigsTable.csv"])

		self.openResult()



	def openResult(self):
		root = Toplevel(self.master)
		myResult = ResultPopUp(root, self.masterName, self.slaveName, self.genExeptedSize, self.nameOfReads[0], self.nameOfReads[1])


class PossibleParamsGamNgs(PossibleParamsParent):
	def __init__(self):
		

		tags = ["Expected size", "Thread number"]

		#("label text", "param description", type, isOptionalParam)
		# type: ["flag=1", "int=2", "intlist=3", "file=4", "float=5", "options=6", "text=7", "dir=8"]
		self.paramDesc = {}

		# FIXED PARAMETERS

		# OPTIONAL PARAMETERS
		self.paramDesc["Expected size"] = ("Expected size of the genome:", "Expected size of the genome", 2, True)
		self.paramDesc["Thread number"] = ("Number of threads", "Number of threads", 2, True)
		
		super().__init__(tags)
