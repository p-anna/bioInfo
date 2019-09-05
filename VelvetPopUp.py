from ParentPopUp import ParentPopUp
from AddicionalParamParent import PossibleParamsParent
from tkinter import *


class VelvetPopUp(ParentPopUp):
	def __init__(self, master, name, possibleParamClassInit):
		super().__init__(master, name, possibleParamClassInit)
		
		#Frame: self.readProperties ----------------------------------------------------------

		# READ CATEGORY LIST
		#("read categ name", "terminalTag", isLibraryNumberNeeded)
		self.readCategList = [('short single-end reads', "-short", True),
							  ('short paired-end reads', "-shortPaired", True),
							  ('long single-end reads', "-long", False),
							  ('long paired-end reads', "-longPaired", False)]
							  
		indexReadCateg = 0        #index of read cateogry frame
		self.readCateg = StringVar()   #variable for radioButtons with read categories
		
		# We put two categories in a row in the frame self.readProperties from ParentPopUp
		for rc in self.readCategList:
			# value of the radioButton is the index in self.readCategList
			rb = ttk.Radiobutton(self.readProperties, style="1.TRadiobutton", text=rc[0], variable=self.readCateg, value=rc[1])
			rb.grid(row=int(indexReadCateg / 2), column=(indexReadCateg % 2), sticky='w')

			#should the "library number" group be enabled for this read category?
			#isLibraryNumberNeeded
			if rc[2]:
				rb.configure(command=lambda: self.disableEnable(True))
			else:
				rb.configure(command=lambda: self.disableEnable(False))
			
			indexReadCateg += 1
			
		self.readCateg.set("-shortPaired")

		indexReadCateg += 1
		ttk.Separator(self.readProperties, orient="horizontal").grid(row=int(indexReadCateg / 2), columnspan=2, sticky='we')
		indexReadCateg += 1

		#READ TYPE LIST
		#("read type name", "terminalTag)
		self.readTypeList = [('fasta', '-fasta'),
							 ('fastq', '-fastq'),
							 ('fasta.gz', '-fasta.gz'),
							 ('fastq.gz', '-fastq.gz'),
							 ('sam', '-sam'),
							 ('bam', '-bam'),
							 ('eland', '-eland'),
							 ('gerald', '-gerald')]
		
		self.readTypeVar = StringVar()

		indexReadType = 0 #index of read type
		
		for rt in self.readTypeList:
			# value of the radioButton is the index in self.readTypeList
			rb = ttk.Radiobutton(self.readProperties, style="1.TRadiobutton", text=rt[0], variable=self.readTypeVar, value=rt[1])
			rb.grid(row=int(indexReadCateg / 2), column=(indexReadCateg % 2), sticky='w')
			indexReadCateg += 1
			indexReadType += 1

		self.readTypeVar.set('-fastq')

		indexReadCateg += 1
		ttk.Separator(self.readProperties, orient="horizontal").grid(row=int(indexReadCateg / 2), columnspan=2, sticky='we')
		indexReadCateg += 1

		#LIBRARY NUMBER
		self.libraryNumberChoices = [('1', ''),
									 ('2', '2')]

		self.libraryNumberVar = StringVar()

		indexLibraryNum = 1 #index of library number
		self.libraryNumRadioButtons = []
		
		for lnc in self.libraryNumberChoices:
			# value of the radioButton is the index in self.libraryNumberChoices
			rb = ttk.Radiobutton(self.readProperties, style="1.TRadiobutton", text=lnc[0], variable=self.libraryNumberVar, value=lnc[1])
			rb.grid(row=int(indexReadCateg / 2), column=(indexReadCateg % 2), sticky='w')
			self.libraryNumRadioButtons.append(rb)
			indexReadCateg += 1
			indexLibraryNum += 1

		self.libraryNumberVar.set('')
		self.isEnabledLibraryNumber = True

	# Helping function -----------------------------------------------

	def disableEnable(self, isEnabledLibraryNumber):
		self.isEnabledLibraryNumber = isEnabledLibraryNumber
		
		if(isEnabledLibraryNumber):
			stateText = NORMAL
		else:
			stateText = DISABLED
			
		for lnrb in self.libraryNumRadioButtons:
			lnrb.configure(state = stateText)
			

	def getFileType(self): #type of input file
		tmpCateg = self.readCateg.get()
		if self.isEnabledLibraryNumber:
			tmpCateg += self.libraryNumberVar.get()
		return [tmpCateg, self.readTypeVar.get()]

	def whereProgram(self, progName):
		currentDir = str(sys.path[0]).split('/')
		goBack = len(currentDir) - 3 + 1    
            
		if progName == "H": #velveth
			return goBack * "../" + "programs/velvet/velveth"
		elif progName == "G": #velvetg
			return goBack * "../" + "programs/velvet/velvetg"
		else:
			messagebox.showwarning("Error", "Unexpected error whereProgram") 

	def runParameterBlocks(self):
		paramsH = [self.whereProgram("H"), ".", self.parameterValues["-k"].get()]
		
		for fileName, fileType in self.inputType.items(): #### CHECK THIS
			paramsH.extend(fileType)
			paramsH.append(self.cwdParam(fileName))

			
		paramsG = [self.whereProgram("G"), "."]
		
		for tag in self.parameterLabels.keys():
			# type: ["flag=1", "int=2", "intlist=3", "file=4", "float=5", "options=6", "text=7", "dir=8"]
			tmpType = self.possibleParameters.paramDesc[tag][1]
			tmpValue = self.parameterValues[tag].get()
			#if paramater is a flag and checkbutton is checked
			if tmpType == 1 and tmpValue == "1":
				paramsG.apped(tag)
			#if int, intlist, float, options or text
			elif tmpType == 2 or tmpType == 3 or tmpType == 5 or tmpType == 6 or tmpType == 7:
				paramsG.append(tag)
				paramsG.append(tmpValue)
			#if file or directory
			elif tmpType == 4 or tmpType == 8:
				paramsG.append(tag)
				paramsG.append(self.cwdParam(tmpValue)) #### CHECK THIS
				
		return [paramsH, paramsG]
		


		

class PossibleParamsVelvet(PossibleParamsParent):
	def __init__(self):
		tags = ["-k", "cov_cutoff", "max_coverage", "exp_cov", "ins_length", "ins_length2", "ins_length_long", "ins_length_sd", "ins_length2_sd", "ins_length_long_sd", "scaffolding", "shortMatePaired", "min_contig_lgth", "read_trkg", "amos_file",  "unused_reads", "max_branvh_length", "max_divergence", "max_gap_count", "min_pair_count"]


		#("param description", type, isOptionalParam)
		# type: ["flag=1", "int=2", "intlist=3", "file=4", "float=5", "options=6", "text=7", "dir=8"]	
		self.paramDesc = {}

		# FIXED PARAMETERS
		self.paramDesc["-k"] = ("K-mer length", 2, False)

		# OPTIONAL PARAMETERS
		self.paramDesc["cov_cutoff"] = ("Delete nodes shorter than this value. (for removing low-coverage nodes left over from the intial correction) or \"auto\"", 7, True)

		self.paramDesc["max_coverage"] = ("Delete nodes longer than this value. (exclude highly covered data from your assembly e.g. plasmid, mitochondrial..)", 2, True)

		self.paramDesc["exp_cov"] = ("This value is the estimate of the expected coverage in short reads of unique sequence, for resolving repeats with long reads, or \"auto\".", 7, True)
        
        #If you have a sufficient coverage of short reads, and any quantity of long reads, you can use the long reads to resolve repeats in a greedy fashion. The simplest way to obtain this value is simply to observe the distribution of contig coverages. and see around which value the coverages of nodes seem to cluster (especially the longer nodes in your dataset)

		self.paramDesc["ins_length"] = ("This value is the insert length. (length of the sequenced fragment, it icludes the length of the reads themselves.", 2, True)
        
        #To activate the use of read pairs, you must specify two parameters: the expected (i.e.  average) insert length (or at least a rough estimate), and the expected short-read k-mer coverage (see 5.2 for more information).

		self.paramDesc["ins_length2"] = ("If you have two paired-end experiments, with different insert lengths. This value indicates the insert length of the second set.", 2, True)

        #Using multiple categories: You can be interested in keeping several kinds of short read sets separate. For example, if you have two paired-end experiments, with different insert lengths, mixing the two together would be a loss of information. This is why Velvet allows for the use of 2 short read channels (plus the long reads, which are yet another category). To do so, you simply need to use the appropriate options when hashing the reads (see 3.1 ). Put the shorter inserts in the first category. Supposing your first readset has an insert length around 400bp and the second one a insert length around 10,000bp, you should type:"

		self.paramDesc["ins_length_long"] = ("This value is the insert length for long paired reads, if they are available. (it is used at scaffolding)", 2, True)

        #If you happen to have hashed paired long reads and you ordered them as explained in 4.1 you can also tell Velvet to use this information for scaffolding by indicating the corresponding insert length (remember that you still need to indicate the short-read k-mer coverage):"


		self.paramDesc["ins_length_sd"] = ("Standard deviation for the insert length", 5, True)
		self.paramDesc["ins_length2_sd"] = ("Standard deviations for the other insert length. (if you have to sets of reads with different lengths)", 5, True)
		self.paramDesc["ins_length_long_sd"] = ("Standard deviation for the long paired reads (if long paired reads are available)", 5, True)

		self.paramDesc["scaffolding"] = ("If you do not want scaffolding, you can turn it off.", 1, True)

        #By default, Velvet will try to scaffold contigs that it cannot quite connect.  This results in sequences of N-s in the contigs.fa file, which correspond to the estimated distance between two neighbouring contigs. If you do not want this scaffolding, you can turn it off with the following switch.
        
		self.paramDesc["shortMatePaired"] = ("Flag if one of the libraries is a mate-pair library made by circularization, and you suspect the presence of read pair contamination.", 1, True)

        #Velvet will then use any available (short) paired-end library to filter out paired-end contamination within the mate-pair library.
        
		self.paramDesc["min_contig_lgth"] = ("You can request that the contigs for output in the contigs.fa file be longer than this value.", 2, True)

		self.paramDesc["read_trkg"] = ("Flag for turning on the read tracking. This costs more memory and calculation time, but produces a more detailed description of the assembly.", 1, True)

		self.paramDesc["amos_file"] = ("Flag for producing an .afg with all the assembly information in one datastructure.", 1, True)

		self.paramDesc["unused_reads"] = ("Flag for obtaining reads unused in the assembly into the file UnusedReads.fa", 1, True)

		self.paramDesc["max_branvh_length"] = ("Maximum branch length is the limit as to how long two paths must be before simplification. (default 100bp).\n Two sequences will not be merged togethe if they are sufficiently divergent.", 2, True)

		self.paramDesc["max_divergence"] = ("Maximum divergence rate is a percentage of aligned pairs of nucleotides to the length of the longest of two sequences.\n By default, Velvet will not simplify two sequences if they are more diverged then this value. (default, 0.2)", 5, True)

		self.paramDesc["max_gap_count"] = ("Maximum gap count is a percentage of aligned pairs of nucleotides to the length of the longest of the two sequences.\n By default, Velvet will not simplify two sequences if more basepaires than this value of the longest sequence are unaligned. (default 3)", 2, True)

		self.paramDesc["min_pair_count"] = ("Minimum read-pair validation is the required number of mate pairs corroborating a connection between two contigs. (default 10)", 2, True)

		super().__init__(tags)
