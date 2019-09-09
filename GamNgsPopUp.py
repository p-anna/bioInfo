from ParentPopUp import ParentPopUp
from AddicionalParamParent import PossibleParamsParent
from tkinter import *
import subprocess

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
		originalFaMaster = self.assemblyMaster.get()
		originalFaSlave= self.assemblySlave.get()

		
		subprocess.run(["cp", originalFaMaster, self.myFolderName + self.masterName + ".fa"])
		subprocess.run(["cp", originalFaSlave, self.myFolderName + self.slaveName + ".fa"])

		print(self.masterName)
		print(self.slaveName)

		assemblyFileName = [self.masterName, self.slaveName]
		
		faFile = []
		for afn in assemblyFileName:
			faFile.append(afn + ".fa")

		nameOfReads = []
		extensionOfReads = []
		readFile = []
		saiFile1 = []
		saiFile2 = []
		for iFile in sorted(self.inputFiles):
			nameOfReads.append(iFile)
			extensionOfReads.append(".fq")
			readFile.append("../" + iFile)
			saiFile1.append(iFile + "1.sai")
			saiFiel2.append(iFile + "2.sai")

		threadNumber = "4"

		
		subprocess.run(["bwa", "index", faFile[0]], cwd = gamResultPath)
		subprocess.run(["bwa", "aln", "-o", "0", "-t", threadNumber, faFile[0], readsFile[0]], stdout=open(gamResultPath + saiFile1[0], "w"), cwd = gamResultPath)
		subprocess.run(["bwa", "aln", "-o", "0", "-t", threadNumber, faFile[0], readsFile[1]], stdout=open(gamResultPath + saiFile2[0], "w"), cwd = gamResultPath)
		sampeOut = subprocess.Popen(["bwa", "sampe", faFile[0], saiFile1[0], saiFile2[0], readsFile[0], readsFile[1]], stdout = subprocess.PIPE, cwd = gamResultPath)
		viewOut = subprocess.Popen(["samtools", "view", "-Shu", "-"], stdin=sampeOut.stdout, stdout = subprocess.PIPE, cwd = gamResultPath)
		sampeOut.stdout.close()
		subprocess.run(["samtools", "sort", "-", assemblyFileName[0] + ".sorted"], stdin=viewOut.stdout, cwd = gamResultPath)
		viewOut.stdout.close()

		subprocess.run(["samtools", "index", assemblyFileName[0] + ".sorted.bam"], cwd = gamResultPath)
		txtFile = open(gamResultPath + assemblyFileName[0] + ".list.txt", "w")
		subprocess.run(["echo", "-e", assemblyFileName[0] + ".sorted.bam\n 90 270"], stdout=txtFile, cwd = gamResultPath)
		txtFile.close()

		# Slave -------------------------------------------------------------------------------------------------------------------------------------

		subprocess.run(["bwa", "index", faFile[1]], cwd = gamResultPath)
		subprocess.run(["bwa", "aln", "-o", "0", "-t", threadNumber, faFile[1], readsFile[0]], stdout=open(gamResultPath + saiFile1[1], "w"), cwd = gamResultPath)
		subprocess.run(["bwa", "aln", "-o", "0", "-t", threadNumber, faFile[1], readsFile[1]], stdout=open(gamResultPath + saiFile2[1], "w"), cwd = gamResultPath)
		sampeOut = subprocess.Popen(["bwa", "sampe", faFile[1], saiFile1[1], saiFile2[1], readsFile[0], readsFile[1]], stdout = subprocess.PIPE, cwd = gamResultPath)
		viewOut = subprocess.Popen(["samtools", "view", "-Shu", "-"], stdin=sampeOut.stdout, stdout = subprocess.PIPE, cwd = gamResultPath)
		sampeOut.stdout.close()
		subprocess.run(["samtools", "sort", "-", assemblyFileName[1] + ".sorted"], stdin=viewOut.stdout, cwd = gamResultPath)
		viewOut.stdout.close()

		subprocess.run(["samtools", "index", assemblyFileName[1] + ".sorted.bam"], cwd = gamResultPath)

		txtFile = open(gamResultPath + assemblyFileName[1] + ".list.txt", "w")
		subprocess.run(["echo", "-e", assemblyFileName[1] + ".sorted.bam\n 90 270"], stdout=txtFile, cwd = gamResultPath)
		txtFile.close()

		# Merge----------------------------------------------------------------------------------------------------------------------------------------
		gamPath = "../../../../../programs/gam-ngs/bin/"
		minBlockSize = "7"

		subprocess.run([gamPath + "gam-create", "--master-bam", assemblyFileName[0] + ".list.txt", "--slave-bam", assemblyFileName[1] + ".list.txt", "--min-block-size", minBlockSize], cwd = gamResultPath)
		subprocess.run([gamPath + "gam-merge", "--blocks-file", "out.blocks", "--master-bam", assemblyFileName[0] + ".list.txt", "--master-fasta", faFile[0],
                        "--slave-bam", assemblyFileName[1] + ".list.txt", "--slave-fasta", faFile[1], "--min-block-size", minBlockSize], cwd = gamResultPath)

		# BAM file for assembled
		outFaFile = "out.gam.fasta"
		gamsaiFile1 = "gam" + nameOfReads[0] + ".sai"
		gamsaiFile2 = "gam" + nameOfReads[1] + ".sai"

		subprocess.run(["bwa", "index", outFaFile], cwd = gamResultPath)


		subprocess.run(["bwa", "aln", "-o", "0", "-t", threadNumber, outFaFile, readsFile[0]], stdout=open(gamResultPath + gamsaiFile1, "w"), cwd = gamResultPath)
		subprocess.run(["bwa", "aln", "-o", "0", "-t", threadNumber, outFaFile, readsFile[1]], stdout=open(gamResultPath + gamsaiFile2, "w"), cwd = gamResultPath)
		sampeOut = subprocess.Popen(["bwa", "sampe", outFaFile, gamsaiFile1, gamsaiFile2, readsFile[0], readsFile[1]], stdout = subprocess.PIPE, cwd = gamResultPath)
		viewOut = subprocess.Popen(["samtools", "view", "-Shu", "-"], stdin=sampeOut.stdout, stdout = subprocess.PIPE, cwd = gamResultPath)
		sampeOut.stdout.close()
		subprocess.run(["samtools", "sort", "-", "gam.sorted"], stdin=viewOut.stdout, cwd = gamResultPath)
		viewOut.stdout.close()

		subprocess.run(["samtools", "index", "gam.sorted.bam"], cwd = gamResultPath)

		self.openResult()


		
		
		return [[]]


	def openResult(self):
		root = Toplevel(self.master)
		myResult = ResultPopUp(root, self.masterName, self.slaveName, "1")


class PossibleParamsGamNgs(PossibleParamsParent):
	def __init__(self):
		

		tags = ["Expected size of the genome:", "Thread number"]

		#("label text", "param description", type, isOptionalParam)
		# type: ["flag=1", "int=2", "intlist=3", "file=4", "float=5", "options=6", "text=7", "dir=8"]
		self.paramDesc = {}

		# FIXED PARAMETERS

		# OPTIONAL PARAMETERS
		self.paramDesc["Expected size of the genome:"] = ("Expected size of the genome:", "Expected size of the genome", 2, True)
		self.paramDesc["Thread number"] = ("Number of threads", "Number of threads", 2, True)
		
		super().__init__(tags)
