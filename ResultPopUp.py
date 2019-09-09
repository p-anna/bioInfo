import style
from tkinter import *
from tkinter import ttk
import subprocess
import os
import time


class ResultPopUp:
	def __init__(self, master, masterName, slaveName, expectedGenomeSize):
		self.master = master

		# Statistic  GAGE ----------------------------------------------------------------------------------------------------------------------------------
		gageStatisticPath = "../../../../programs/gage-paper-validation"
		#genomeExpectedSize = "4620000"
       
        # java GetFastaStats -o -min 200 -genomeSize <Genome Expected Size> <Contig Fasta/Scaffold Fasta>
        # Columns of table from GAGE statistics

		commonPath = "../../Documents/MasterRad/python/program/gam-ngs/"

		try:
			genSize = int(expectedGenomeSize)
			gageProc = subprocess.run(["java", "GetFastaStats", "-o", "-min", "200", "-genomeSize", expectedGenomeSize, commonPath + masterName + ".fa"],
									  stdout = subprocess.PIPE, cwd = gageStatisticPath)
		except ValueError:
			gageProc = subprocess.run(["java", "GetFastaStats", "-o", "-min", "200", commonPath + masterName+ ".fa"], stdout = subprocess.PIPE, cwd = gageStatisticPath)

		masterResult = (re.sub(r'\\n', ' ', str(gageProc.stdout))).replace('b\'', '', 1) # '\n' replace with ' ', "b'" remove from the beggining if there is one

		columnNames = re.findall(r'([a-zA-Z_][^:]+):', masterResult) # text until ":" which starts with a letter
		columnWidth = list(map(lambda x: len(x), re.findall(r': ?([\S]+)', masterResult)))


		statTree = ttk.Treeview(self.master, style="mystyle.Treeview", height = 3)
		statTree.tag_configure('odd', background='#9cf767') # different row background color
		statTree.tag_configure('even', background='#92b280')

		statTree['columns'] = ()

		for i in range(len(columnNames)):
			statTree['columns'] = statTree['columns'] + ("ch" + str(i),)

		i = 0
		for v in columnNames:
			statTree.heading("ch" + str(i), text=v)
			statTree.column("ch" + str(i), anchor = CENTER, width = (max(columnWidth[i], len(v)) + 1) * 10, stretch = True)
			i = i+1


		# Values in table of GAGE statistics
		statTree.insert('', 'end', text="Master - " + masterName, values=re.findall(r': ?([\S]+)', masterResult), tag = ("odd", ))
 
		try:
			genSize = int(expectedGenomeSize)
			gageProc = subprocess.run(["java", "GetFastaStats", "-o", "-min", "200", "-genomeSize", expectedGenomeSize, commonPath + slaveName + ".fa"],
									  stdout = subprocess.PIPE, cwd = gageStatisticPath)
		except ValueError:
			gageProc = subprocess.run(["java", "GetFastaStats", "-o", "-min", "200", commonPath + slaveName + ".fa"], stdout = subprocess.PIPE, cwd = gageStatisticPath)

		slaveResult = (re.sub(r'\\n', ' ', str(gageProc.stdout))).replace('b\'', '', 1)
		statTree.insert('', 'end', text="Slave - " + slaveName, values=re.findall(r': ?([\S]+)', slaveResult), tag = ("even", ))

		try:
			genSize = int(expectedGenomeSize)
			gageProc = subprocess.run(["java", "GetFastaStats", "-o", "-min", "200", "-genomeSize", expectedGenomeSize, commonPath + "out.gam.fasta"],
									  stdout = subprocess.PIPE, cwd = gageStatisticPath)
		except ValueError:
			gageProc = subprocess.run(["java", "GetFastaStats", "-o", "-min", "200", commonPath + "out.gam.fasta"], stdout = subprocess.PIPE, cwd = gageStatisticPath)
			
		mergeResult = (re.sub(r'\\n', ' ', str(gageProc.stdout))).replace('b\'', '', 1)
		statTree.insert('', 'end', text="GAM-NGS merger", values=re.findall(r': ?([\S]+)', mergeResult), tag = ("odd", ))

		statTree.pack(fill = "both", expand = True)
		# http://gage.cbcb.umd.edu/results/index.html
		# sh getCorrectnessStats.sh <Reference Fasta> <Contig Fasta> <Scaffold Fasta>

		# Statistic FRC plot ------------------------------------------------------------------------------------------------------------------------------

		subprocess.run(["mkdir", "statistics"])

		#./FRC --pe-sam gam.sorted.bam --output gam
		FRCPath = "../../../../programs/FRC_align-master/bin/FRC"

		subprocess.run([FRCPath, "--pe-sam", "gam-ngs/gam.sorted.bam", "--output", "statistics/gam-ngs"])
		subprocess.run([FRCPath, "--pe-sam", "gam-ngs/" + masterName + ".sorted.bam", "--output", "statistics/" + masterName])
		subprocess.run([FRCPath, "--pe-sam", "gam-ngs/" + slaveName + ".sorted.bam", "--output", "statistics/" + slaveName])

		plotScriptPath = 'statistics/plotScript.gp'
		plotScript = open(plotScriptPath, 'w')

		plotScript.write("#!/usr/bin/gnuplot\n")
		plotScript.write("set terminal png size 800, 600\n")
		plotScript.write("set output \"statistics/FRC.png\"\n")
		plotScript.write("set title \"FRC curve of the assemblies and the marged assembly\" font \",14\"\n")
		plotScript.write("set key right bottom font \",12\"\n")
		plotScript.write("set autoscale\n")
		plotScript.write("files = system('find \"statistics\" -type f -regex \"[^_]*_FRC.txt\"')\n") #find . -type f -regex "[^_]*_FRC\.txt"
		plotScript.write("set ylabel \"Approximate Coverage (%)\"\n")
		plotScript.write("set xlabel \"Feature Threshold\"\n")
		plotScript.write("plot for [data in files] data using 1:2 with lines title data lw 2\n")

		plotScript.close()
		subprocess.run(["gnuplot", plotScriptPath])

		label = ttk.Label(self.master)
		self.master.image1 = PhotoImage(file='statistics/FRC.png')
		label['image'] = self.master.image1
		label.pack(fill = 'both', expand = True, side = 'bottom')

		subprocess.run(["rm", "spades.sorted_contigsTable.csv"])
		subprocess.run(["rm", "abyss.sorted_contigsTable.csv"])
		subprocess.run(["rm", "velvet.sorted_contigsTable.csv"])
		subprocess.run(["rm", "gam.sorted_contigsTable.csv"])


		############ DATASET INFORMATION #########################################################################
		
	
		self.forwardReads = "read1.fq"
		self.reverseReads = "read2.fq"

		frame = ttk.Frame(master, style="M.TFrame")
		frame.pack(fill='both', expand=True)
		
		ttk.Label(frame, text="Dataset Information:", style="N.TLabel").pack(fill = 'both', expand = True, side = 'top')
		dataInfoTree = ttk.Treeview(frame, style="mystyle.Treeview", height = 2)
		dataInfoTree.tag_configure('odd', background='#9cf767') # different row background color
		dataInfoTree.tag_configure('even', background='#92b280')

		dataInfoTree['columns'] = ("Upload files:", "Filesize:", "Created: (when)")

		for ta in dataInfoTree['columns']:
			dataInfoTree.heading(ta, text=ta)
			dataInfoTree.column(ta, anchor = CENTER, width = 200, stretch = True)

		try:
			uploadStats = os.stat(self.forwardReads)		
			dataInfoTree.insert('', 'end', text='[1]',
								values = [self.forwardReads, self.format_bytes(uploadStats.st_size), time.ctime(uploadStats.st_mtime)], tag = ("odd", ))
			uploadStats = os.stat(self.reverseReads)		
			dataInfoTree.insert('', 'end', text='[2]',
								values = [self.reverseReads, self.format_bytes(uploadStats.st_size), time.ctime(uploadStats.st_mtime)], tag = ("even", ))
		except:
			messagebox.showwarning("Problem with the files", "Upload files cannot be found or don't exist!")


		dataInfoTree.pack(fill = "both", expand = True)

		###########################################################################################

		ttk.Label(frame, text="Job information:", style="N.TLabel").pack(fill = 'both', expand = True, side = 'top')
		jobInfoTree = ttk.Treeview(frame, style="mystyle.Treeview", height = 3)
		jobInfoTree.tag_configure('odd', background='#9cf767') # different row background color
		jobInfoTree.tag_configure('even', background='#92b280')

		jobInfoTree['columns'] = ("Tool:", "Tool Version:", "Parameters:")

		for ta in jobInfoTree['columns']:
			jobInfoTree.heading(ta, text=ta)
			jobInfoTree.column(ta, anchor = CENTER, width = 200, stretch = True)

		jobInfoTree.insert('', 'end', values = ["ABySS", "GNU Make 4.1", "k=27"], tag = ("odd", ))
		jobInfoTree.insert('', 'end', values = ["Velet", "Version 1.2.10", "k=27"], tag = ("even", ))
		jobInfoTree.insert('', 'end', values = ["SPAdes", "v3.11.1", "k=27"], tag = ("odd", ))
		
		jobInfoTree.pack(fill = "both", expand = True)


	def format_bytes(self, size):
		# 2**10 = 1024
		power = 2**10
		n = 0
		power_labels = {0 : '', 1: 'kilo', 2: 'mega', 3: 'giga', 4: 'tera'}
		while size > power:
			size /= power
			n += 1
		return "{:.2f}".format(size), power_labels[n]+'bytes'
