from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import subprocess
from tkinter import messagebox
import re


class AbyssPopUp:
    def __init__(self, master):

        rowcount = 0 # row index for grid of main frame
        
        frame = ttk.Frame(master, style="M.TFrame")
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="ABySS", style="N.TLabel").grid(row=rowcount, columnspan=2, sticky='w')
        rowcount += 1
        
        ttk.Label(frame, text="Files for assembly:", style="C.TLabel").grid(row=rowcount, column=0, sticky='w')
        self.buttonUlaz = ttk.Button(frame, text='Choose the input files', command=self.openFileName)
        self.buttonUlaz.grid(row=rowcount, column=1, sticky='w', padx=20)
        rowcount += 1

        self.radioButtFrame = ttk.Frame(frame, style="P.TFrame", padding=(10, 10, 10, 10))
        self.radioButtFrame.grid(row=rowcount, columnspan=2, pady=10)
        rowcount += 1

        #-------- radioButtFrame
        self.endType = StringVar()
        ttk.Radiobutton(self.radioButtFrame, style="1.TRadiobutton", text='single-end reads',
                        variable=self.endType, value=1).pack(side=LEFT)
        ttk.Radiobutton(self.radioButtFrame, style="2.TRadiobutton", text='paired-end reads',
                        variable=self.endType, value=2).pack(side=LEFT)
        self.endType.set(1)
        #--------

        self.inputFrame = ttk.Frame(frame, style="P.TFrame", padding=(10, 10, 10, 10))
        self.inputFrame.grid(row=rowcount, columnspan=2, pady=10)
        rowcount += 1
            
        #-------- inputFrame
        self.inputFiles = {}
        self.inputType = {}
        #--------

        ttk.Label(frame, text='Parameters:', style="C.TLabel").grid(row=rowcount, columnspan=2, sticky='w')
        rowcount += 1

        self.paramFrame = ttk.Frame(frame, style="P.TFrame", padding=(10, 10, 10, 10))
        self.paramFrame.grid(row=rowcount, columnspan=2)
        rowcount += 1
        
        #--------- paramFrame
        ttk.Label(self.paramFrame, text='K-mer length:', style="P.TLabel").grid(row=0, column=0, sticky='e')
        self.kMerEntry = ttk.Entry(self.paramFrame)
        self.kMerEntry.grid(row=0, column=1, sticky='w')

        ttk.Label(self.paramFrame, text='Name of the assembly:', style="P.TLabel").grid(row=1, column=0, sticky='e')
        self.nameEntry = ttk.Entry(self.paramFrame)
        self.nameEntry.grid(row=1, column=1, sticky='w')
        #---------
        
        self.buttonStart = ttk.Button(frame, text='Run the assembly!', command=self.runScript)
        self.buttonStart.grid(row=rowcount, columnspan=2, sticky='s', pady=20)
        rowcount += 1

        self.assemblyProg = ttk.Progressbar(frame, orient="horizontal", length=300, mode="determinate")
        self.assemblyProg.grid(row=rowcount, columnspan=2, pady=10)
        rowcount += 1
        
    # ---- end of init ------------------------------------------------------------------- 
    
# ---- Functionality  -----------------------------------------------------------------------


    def runScript(self):
        print('Validating the parameters')
        try:
            tmpKmer = int(self.kMerEntry.get())
            tmpName = self.nameEntry.get().strip()
            if tmpKmer<15 or tmpKmer>64:
                messagebox.showwarning("Problem with the parameters", "K-mer entry must be between 15 and 64!")
            elif tmpName == "":
                messagebox.showwarning("Problem with the parameters", "Name entry cannot be empty")
            elif not(tmpName.isalnum()):
                messagebox.showwarning("Problem with the parameters",
                                       "Name entry can contain only alphabetical or numeric characters")
            elif len(self.inputFiles)==0:
                messagebox.showwarning("Problem with the input files", "No input file is choosen")
            else:
                self.assemblyProg.start()
                print('Running of the assembly...')
                tmpDic = self.determineCommonDict()
                tmpFiles1 = self.determineFileList(tmpDic, 1)
                tmpFiles2 = self.determineFileList(tmpDic, 2)
                tmpDic = self.cwdParam(tmpDic)

                #print("tmpDic: "+tmpDic)
                #print("tmpFiles1: " + tmpFiles1)
                #print("tmpFiles2: " + tmpFiles2)

                #NEM MUKODIK RENDESEN + kikerdezni hogz a tmpFiles ures-e
                if tmpDic == '':
                    subprocess.run(["abyss-pe", "k="+str(tmpKmer), "name="+tmpName, "in="+tmpFiles2])
                    
                #else:
                #    subprocess.run(["abyss-pe", " k="+str(tmpKmer), " name="+tmpName, " in="+tmpFiles2,
                #                    " se="+tmpFiles1], cwd=tmpDic) 
        except ValueError:
            messagebox.showwarning("Problem with the parameters", "K-mer entry was no valid number!")

            
    def openFileName(self):
        filename = askopenfilename()
        if not(filename in self.inputFiles) and str(filename) != "()":
            self.inputFiles[filename]=ttk.Button(self.inputFrame, text=self.buttonText(filename),
                                                 style=str(self.endType.get()) + "I.TButton",
                                                 command=lambda: self.deleteInputFile(filename))
            self.inputFiles[filename].pack(fill=BOTH, expand=1)
            self.inputType[filename] = self.endType.get()
            

    def deleteInputFile(self, text):
        try:
            self.inputFiles[text].destroy()
            del  self.inputFiles[text]
        except:
            messagebox.showwarning("Error", "Unexpected error deleteInputFile")


# ---------------------------- Helping methods -------------------------------------------------------
        
    def buttonText(self, filename):
        try:
            m = re.search('.*/(.*)', filename)
            return "x   " + m.group(1)
        except:
            messagebox.showwarning("Error", "Unexpected error buttonText")

    def determineCommonDict(self):
        lista = str(next(iter(self.inputFiles))).split('/')[:-1] #apsoluth path directories
        for key in self.inputFiles.keys(): #for every input file find the common parant dictionary
            tmp = str(key).split('/') 
            n = min(len(lista), len(tmp))
            i = 0
            while i<n and lista[i] == tmp[i] :
                i+=1
            lista = lista[:i]
        return "/".join(lista)              #make an apsoluth path from list of directories
            
    def determineFileList(self, dic, endType):
        tmpFiles = ""
        for k in self.inputFiles.keys():
            if int(self.inputType[k]) == endType:
                tmpFiles += "\ ".join(re.search(dic+'/(.*)', str(k)).group(1).split(" ")) + " "
        tmpFiles = tmpFiles.strip() #+ "'"
        return tmpFiles

    def cwdParam(self, dic):
        currentDir = str(sys.path[0]).split('/')
        #print("current: " + "|".join(currentDir))
        destenDir = str(dic).split('/')
        #print("desteny: " + "|".join(destenDir))
        n = min(len(currentDir), len(destenDir))
        i = 0
        while i<n and currentDir[i] == destenDir[i] :
            i+=1
        return '../'*(len(currentDir)-i) + "/".join(destenDir[i:])
