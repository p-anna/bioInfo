from ParentPopUp import ParentPopUp
from AddicionalParamParent import PossibleParamsParent
from tkinter import *
import subprocess
import os

class QuastPopUp(ParentPopUp):
	def __init__(self, master, name, possibleParamClassInit):
		super().__init__(master, name, possibleParamClassInit)

		#Frame: self.readProperties ----------------------------------------------------------

		indexReadCateg = 0        #index of frame

		ttk.Label(self.readProperties, text= "Please choose the read category of the next input file:", style="HP.TLabel").grid(row=int(indexReadCateg / 3), columnspan=3, sticky='w')
		indexReadCateg += 3
		
		# READ CATEGORY LIST
		#("read categ name", "terminalTag", isReadTypeNeeded)
		self.readCategList = [("single-end", "--single", False), 
							  ("paired-end", "--pe", True),
							  ("mate-pair", "--mp", True),
							  ('PacBio', "--pacbio", False),
							  ('Nanopore', "--nanopore", False),
							  ("BAM (reads against the ref)", "--ref-bam", False),
							  ("SAM (reads against the ref)", "--ref-sam", False),
							  ("BEDPE with structural variations", "--sv-bedpe", False)]

		self.readCateg = StringVar()   #variable for radioButtons with read categories
		
		# We put two categories in a row in the frame self.readProperties from ParentPopUp
		for rc in self.readCategList:
			# value of the radioButton is the index in self.readCategList
			rb = ttk.Radiobutton(self.readProperties, style="1.TRadiobutton", text=rc[0], variable=self.readCateg, value=rc[1])
			rb.grid(row=int(indexReadCateg / 3), column=(indexReadCateg % 3), sticky='w')
			#isReadTypeNeeded
			if rc[2]:
				rb.configure(command=lambda: self.disableEnable(True))
			else:
				rb.configure(command=lambda: self.disableEnable(False))
			
			indexReadCateg += 1
			
		self.readCateg.set("--pe")

		indexReadCateg += 1
		ttk.Separator(self.readProperties, orient="horizontal").grid(row=int(indexReadCateg / 3), columnspan=3, sticky='we')
		indexReadCateg +=3

		ttk.Label(self.readProperties, text="Please choose the type of reads in the next input file:", style="HP.TLabel").grid(row=int(indexReadCateg / 3), columnspan=3, sticky='w')
		indexReadCateg += 3
		
		#READ TYPE LIST
		#("read type name", "terminalTag)
		self.readTypeList = [('forward reads', "1"),
							 ('reverse reads', "2"),
							 ('interlaced reads', "12")]
		
		self.readTypeVar = StringVar()

		self.readTypeRadioButtons = []
		
		for rt in self.readTypeList:
			# value of the radioButton is its terminalTag
			rb = ttk.Radiobutton(self.readProperties, style="1.TRadiobutton", text=rt[0], variable=self.readTypeVar, value=rt[1])
			rb.grid(row=int(indexReadCateg / 3), column=(indexReadCateg % 3), sticky='w')
			self.readTypeRadioButtons.append(rb)
			indexReadCateg += 1

		self.readTypeVar.set("1")
		self.isEnabledReadType = True

	def disableEnable(self, isEnabledReadType):
		self.isEnabledReadType = isEnabledReadType

		if(isEnabledReadType):
			stateText = NORMAL
		else:
			stateText = DISABLED

		for rtrb in self.readTypeRadioButtons:
			rtrb.configure(state = stateText)

	def getFileType(self): #type of input file
		tmpFileType = self.readCateg.get()
		if self.isEnabledReadType:
			tmpFileType += self.readTypeVar.get()
		return tmpFileType


	def whereProgram(self):
		currentDir = str(sys.path[0]).split('/')
		goBack = len(currentDir) - 3 + 1    
		return goBack * "../" + "programs/quast-5.0.2/quast.py"
	

	def runParameterBlocks(self):

		bamFilesForCp = ["ABySS.sorted.bam", "Velvet.sorted.bam", "SPAdes.sorted.bam", "gam.sorted.bam"]
		faFilesForCp = ["ABySS.fa", "Velvet.fa", "SPAdes.fa", "out.gam.fasta"]

		bamList = ""
		for fileCp in bamFilesForCp:
			if os.path.exists("GAM-NGS/" + fileCp):
				subprocess.run(["cp", fileCp, "../" + self.name + "/"], cwd="GAM-NGS")
				bamList += fileCp + ","

		faList = []
		for fileCp in faFilesForCp:
			if os.path.exists("GAM-NGS/" + fileCp):
				subprocess.run(["cp", fileCp, "../" + self.name + "/"], cwd="GAM-NGS")
				faList.append(fileCp)
				
		params = ["python", self.whereProgram(), "-o", "."]

		for fileName, fileType in self.inputType.items():
			params.append(fileType)
			params.append(self.cwdParam(fileName))
				
		for tag in self.parameterLabels.keys():
			# type: ["flag=1", "int=2", "intlist=3", "file=4", "float=5", "options=6", "text=7", "dir=8"]
			tmpType = self.getTypeParam(tag)
			tmpValue = self.parameterValues[tag].get()
			#if paramater is a flag and checkbutton is checked
			if tmpType == 1 and tmpValue == 1:
				params.append(tag)
			#if int, intlist, float, options or text
			elif tmpType == 2 or tmpType == 3 or tmpType == 5 or tmpType == 6 or tmpType == 7:
				params.append(tag)
				params.append(tmpValue)
			#if file or directory
			elif tmpType == 4 or tmpType == 8:
				params.append(tag)
				params.append(self.cwdParam(tmpValue))

		params.append("--bam")
		params.append(bamList[:-1])
		for fL in faList:
			params.append(fL)

		for p in params:
			print(p)
			
		subprocess.run(params, cwd = self.name)



class PossibleParamsQuast(PossibleParamsParent):
	def __init__(self):
		
		tags = ["--k-mer-size", "-r", "--features", "--gene-finding", "--min-contig",
				"--threads", "--large", "--k-mer-stats", "--gene-finding", "--gene-threshold",
				"--est-ref-size", "--use-all-alignments", "--min-alignment",
				"--ambiguity-usage", "--ambiguity-score", "--fragmented",
				"--upper-bound-assembly", "--est-insert-size", "--memory-efficient",
				"--space-efficient", "--no-check", "--no-html", "--no-sv", "--no-gzip",
				"--no-snps", "--no-gc"]
		#       "--eukaryote", "--fungus", "--circos", "--mgm", "--glimmer", "--rna-finding",
		#       "--conserved-genes-finding", "--scaffold-gap-max-size", "--upper-bound-min-con"
		#       "--plots-format", "--no-icarus", "--no-plots", "--split-scaffolds", "--operons"
		#       "--min-identity", "--strict-NA", "--extensive-mis-size", "--unaligned-part-size",
		#		"--skip-unaligned-mis-contigs", "--fragmented-max-indent", "--no-read-stats"

		#("label text", "param description", type, isOptionalParam)
		# type: ["flag=1", "int=2", "intlist=3", "file=4", "float=5", "options=6", "text=7", "dir=8"]
		self.paramDesc = {}

		# FIXED PARAMETERS
		self.paramDesc["--k-mer-size"] = ("K-mer length", "K-mer length [default is 101 bp] Use smaller values for genomes with high levels of heterozygosity, too small k-mer sizes may give irrelevant results.", 2, False)

		# OPTIONAL PARAMETERS
		self.paramDesc["-r"] = ("Reference genome", "Reference genome file.", 4, True)
		self.paramDesc["--features"] = ("Genomic feature positions", "File with genomic feature positions in the reference genome.", 4, True)
		self.paramDesc["--gene-finding"] = ("QUAST predict genes", "If you do not have the annotated positions, you can make QUAST predict genes.", 1, True)
		self.paramDesc["--min-contig"] = ("Min contig length", "Lower threshold for a contig length (in bp). Shorter contigs won't be taken into account [500].", 2, True)
		self.paramDesc["--threads"] = ("Number of threads", "Maximum number of threads. [default is 25% of all available CPUs but minimum 1].", 2, True)
		#self.paramDesc["--split-scaffolds"] = ("Assemblies are scaffolds", "The assemblies are scaffolds (rather than contigs).", 1, True)
		#self.paramDesc["--eukaryote"] = ("Eukaryotic", "Genome is eukaryotic. Affects gene finding, GeneMark-ES is used.", 1, True)
		#self.paramDesc["--fungus"] = ("Fungal", "Genome is fungal. Affects gene finding, GeneMark-ES is used.", 1, True)
		self.paramDesc["--large"] = ("Genome is large", "Genome is large ( > 100 Mbp). Affects speed and accuracy.", 1, True)
		self.paramDesc["--k-mer-stats"] = ("K-mer-based quality metrics", "Compute k-mer-based quality metrics, such as k-mer-based completeness, # k-mer-based misjoins.", 1, True)
		#self.paramDesc["--circos"] = ("Plot Circos version", "Plot Circos version of Icarus contig alignment viewer.", 1, True)
		self.paramDesc["--gene-finding"] = ("Enables gene finding", "Enables gene finding. [disabled].", 1, True)
		#self.paramDesc["--mgm"] = ("Force use of MetaGeneMark", "Force use of MetaGeneMark for gene finding instead of the default.", 1, True)
		#self.paramDesc["--glimmer"] = ("Use GlimmerHMM", "Use GlimmerHMM for gene finding (instead of GeneMark). Note: you may skip --gene-finding option if --glimmer is specified.", 1, True)
		self.paramDesc["--gene-threshold"] = ("List of thresholds for gene lengths", "Comma-separated list of thresholds (in bp) for gene lengths to find with a finding tool. [0,300,1500,3000].", 3, True)
		#self.paramDesc["--rna-finding"] = ("Enables ribosomal RNA gene finding", "Enables ribosomal RNA gene finding. Disabled by default.", 1, True)
		#self.paramDesc["--conserved-genes-finding"] = ("Search for Universal Single-Copy Orthologs", "Enables search for Universal Single-Copy Orthologs using BUSCO [disabled].", 1, True)
		#self.paramDesc["--operons"] = ("File with operon positions", "File with operon positions in the reference genome.", 4, True)
		self.paramDesc["--est-ref-size"] = ("Estimated reference genome size", "Estimated reference genome size (in bp) for computing NG50 statistics, if a reference genome file is not specified.", 2, True)
		self.paramDesc["--use-all-alignments"] = ("Compute all alignments", "Compute all alignments genome fraction, # genomic features, # operons metrics [ambiguous and redundant alignments filtered out].", 1, True)
		self.paramDesc["--min-alignment"] = ("Min length of alignment", "Minimum length of alignment (in bp). Alignments shorter will be filtered.", 2, True)
		#self.paramDesc["--min-identity"] = ("Min IDY% of a proper alignment", "Minimum IDY% considered as proper alignment. Alignments with IDY% worse will be filtered. [95.0 %].", 5, True)
		self.paramDesc["--ambiguity-usage"] = ("Processing equally good alignments", "Processing equally good alignments of a contig: \"none\" skip all such alignments; \"one\" take only one (the best); \"all\" use all alignments. [default is \"one\"].", 6, True, ["none", "one", "all"])
		self.paramDesc["--ambiguity-score"] = ("Equally good alignments (0.8 - 1.0)", "When defining equally good alignments of a single contig with LEN × IDY%, options less than S × best(LEN × IDY%) are discarded. S between 0.8 and 1.0. [0.99].", 5, True)
		#self.paramDesc["--strict-NA"] = ("Break contigs at every misassembly", "Break contigs at every misassembly event (including local ones) to compute NAx and NGAx statistics. [breaks contigs only at extensive misassemblies (not local ones)].", 1, True)
		#self.paramDesc["--extensive-mis-size"] = ("Threshold for the relocation size", "Threshold for the relocation size (gap or overlap size between left and right flanking sequence). Shorter relocations are considered as local misassemblies. Greater then 85 [1000 bp]", 2, True)
		#self.paramDesc["--scaffold-gap-max-size"] = ("", "Max allowed scaffold gap length difference for detecting corresponding type of misassemblies. Longer inconsistencies are considered as extensive misassemblies. Greater than extensive misassembly size. [10000 bp]", 2, True)
		#self.paramDesc["--unaligned-part-size"] = ("Unaligned part size", "Lower threshold for detecting partially unaligned contigs. [500 bp]", 2, True)
		#self.paramDesc["--skip-unaligned-mis-contigs"] = ("Do not distinguish contigs*", "Do not distinguish contigs with more than 50% unaligned bases as a separate group of contigs. [QUAST does not count misassemblies in them]", 1, True)
		self.paramDesc["--fragmented"] = ("Reference genome is fragmented", "Reference genome is fragmented. QUAST will try to detect misassemblies caused by the fragmentation and mark them fake (will be excluded from # misassemblies)..", 1, True)
		#self.paramDesc["--fragmented-max-indent"] = ("Fake translocation if alignments are further", "Mark translocation as fake if both alignments are located no further than N bases from the ends of the reference fragments. Less than extensive misassembly size, requires --fragmented option. [50]", 2, True)
		self.paramDesc["--upper-bound-assembly"] = ("Simulate upper bound assembly", "Simulate upper bound assembly based on the reference genome and a given set reads (mate-pairs or long reads). This assembly is added to the comparison.", 1, True)
		#self.paramDesc["--upper-bound-min-con"] = ("Upper bound for connecting", "Minimal number of 'connecting reads' needed for joining upper bound contigs into a scaffold. [2 for mate-pairs and 1 for long reads] (PacBio or Nanopore libraries).", 2, True)
		self.paramDesc["--est-insert-size"] = ("Paired-reads insert size", "Paired-reads insert size used in the upper bound assembly construction, for detecting minimal repeat size that spans assembly into contigs. [median insert size of paired-end reads or 255].", 2, True)
		#self.paramDesc["--plots-format"] = ("File format for plots", "File format for plots. Supported formats: emf, eps, pdf, png, ps, raw, rgba, svg, svgz. [PDF].", 7, True)
		self.paramDesc["--memory-efficient"] = ("One thread per assembly", "Use one thread, separately per each assembly and each chromosome. This may significantly reduce memory consumption for large genomes.", 1, True)
		self.paramDesc["--space-efficient"] = ("Only primary output", "Create only primary output items (reports, plots, quast.log, etc). All auxiliary files will not be created.", 1, True)
		self.paramDesc["--no-check"] = ("No check of fasta", "Do not check and correct input FASTA files (both reference genome and assemblies). [QUAST corrects them] Incorrect FASTA files may cause failing.", 1, True)
		#self.paramDesc["--no-plots"] = ("No plots", "Do not draw plots.", 1, True)
		self.paramDesc["--no-html"] = ("No HTML report", "Do not build HTML reports and Icarus viewers.", 1, True)
		#self.paramDesc["--no-icarus"] = ("No Icarus viewers", "Do not build Icarus viewers.", 1, True)
		self.paramDesc["--no-snps"] = ("No SNPs statistics", "Do not report SNPs statistics. This may significantly reduce memory consumption on large genomes and speed up computation.", 1, True)
		self.paramDesc["--no-gc"] = ("No GC computation", "Do not compute GC% and do not produce GC-distribution plots (both in HTML report and in PDF).", 1, True)
		self.paramDesc["--no-sv"] = ("No structural variant", "Do  not run structural variant calling and processing (make sense only if reads are specified).", 1, True)
		self.paramDesc["--no-gzip"] = ("No gzip", "Do not compress large output files (files containing SNP information and predicted genes). This may speed up computation, but more disk space is required.", 1, True)
		#self.paramDesc["--no-read-stats"] = ("No read stats", "Do not align reads against assemblies and do not report the corresponding metrics.", 1, True)

		super().__init__(tags)
