import sys
import os
import threading
import subprocess

from Tkinter import *
from tkFileDialog import *


def createScript():
  
    index = tbLogFileBinding.get().rfind('/')
    treeFile = tbLogFileBinding.get()[0:index+1] 
    treeFile += '0' + tbOldTreeFileBinding.get()
    
    cmd = "treefix"
    if tbStreeBinding.get() != "":
        cmd += " -s "+ tbStreeBinding.get()
    if tbSmapBinding.get() != "":
        cmd += " -S " + tbSmapBinding.get() 
    if tbAlignmentBinding.get() != "":
        cmd += " -A " + tbAlignmentBinding.get()
    if tbAlignmentBinding.get() != "":
        cmd += " -o " + tbOldTreeFileBinding.get()
    if tbNewTreeFileBinding.get() != "":
        cmd +=" -n " + tbNewTreeFileBinding.get()
    if tbVerbosityBinding.get() > -1 and tbVerbosityBinding.get() < 5:
        cmd += " -V " + str(tbVerbosityBinding.get())
    if tbLogFileBinding.get() != "":
        cmd += " -l " + tbLogFileBinding.get() + " " + treeFile
    if str(tbIterationsBinding.get()) != "":
        cmd += " --niter " + str(tbIterationsBinding.get())
    if tbExtraArgsBinding.get() != "":
        cmd += " -e " + tbExtraArgsBinding.get()
    if ddModel.get() == "MulRF":
        cmd += " --smodule treefix.models.mulrfmodel.MulRFModel"
    tOutput.insert(END, "Running TreeFix:\n" + cmd + "\n")
    
    return cmd

def getSaveFileName(bindingVar):
    bindingVar.set(asksaveasfilename(parent=window) )
        
def getOpenFileName(bindingVar):
    bindingVar.set(askopenfilename(parent=window))

def popenAndCall():

    def runInThread(cmd):
                
        proc = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE,stdout=subprocess.PIPE)
        proc.wait()
        while True:
            line = proc.stderr.readline()
            if line != '':
               tOutput.insert(END , line)
            else:
                break
        tOutput.insert(END , "Completed\n")
        return
    
    cmd = createScript()
    thread = threading.Thread(target=runInThread, args=(cmd,))
    thread.start()
    return thread
 
def showMessage():
    tkMessageBox.askokcancel(window, icon='info', type='ok', title='Message Box Selection', message='You clicked on').show()
 
def saveScript():
    fileName = asksaveasfilename(parent=window) 
    #showMessage()
    file = open(fileName, "a")
    file.write(createScript())
 

window = Tk()
fileName = ""

row = 0;
window.title("TreeFix Script Generator")
#window.geometry("600x600+50+50")

#Binding Vars
tbStreeBinding = StringVar()
tbSmapBinding = StringVar()
tbLogFileBinding = StringVar()
tbIterationsBinding = IntVar()
tbIterationsBinding.set(100)
tbAlignmentBinding = StringVar()
tbOldTreeFileBinding = StringVar()
tbNewTreeFileBinding = StringVar()
tbExtraArgsBinding = StringVar()
tbVerbosityBinding = IntVar()
tbVerbosityBinding.set(1)
ddModel = StringVar()
ddModel.set("DupLoss")
#End of Binding Vars

configScript = LabelFrame(window)
configScript.grid(row=row, columnspan=7, sticky='W', padx=5, pady=5, ipadx=5, ipady=5)

#Species Tree
lblStree = Label(configScript, text="Select Species Tree:")
lblStree.grid(row=row, column=0, sticky='E', padx=5, pady=2)

tbStree = Entry(configScript, textvariable=tbStreeBinding)
tbStree.grid(row=row, column=1, columnspan=7, sticky="WE", pady=3)

btnStree = Button(configScript, text="Browse", command = lambda: getOpenFileName(tbStreeBinding))
btnStree.grid(row=row, column=8, sticky='W', padx=5, pady=2)
row += 1

#Species Map
lblSmap = Label(configScript, text="Select Species Map:")
lblSmap.grid(row=row, column=0, sticky='E', padx=5, pady=2)

tbSmap = Entry(configScript, textvariable=tbSmapBinding)
tbSmap.grid(row=row, column=1, columnspan=7, sticky="WE", pady=2)

btnSmap = Button(configScript, text="Browse", command = lambda: getOpenFileName(tbSmapBinding))
btnSmap.grid(row=row, column=8, sticky='W', padx=5, pady=2)
row += 1


#Log File
lblLogFile = Label(configScript, text="Select/Create Log File:")
lblLogFile.grid(row=row, column=0, sticky='E', padx=5, pady=2)

tbLogFile = Entry(configScript, textvariable=tbLogFileBinding)
tbLogFile.grid(row=row, column=1, columnspan=7, sticky="WE", pady=2)

btnLogFile= Button(configScript, text="Browse", command = lambda: getOpenFileName(tbLogFileBinding))
btnLogFile.grid(row=row, column=8, sticky='W', padx=5, pady=2)
row += 1

#Alignment File Extension 
lblAlignment = Label(configScript, text="Alignment File Extension:")
lblAlignment.grid(row=row, column=0, sticky='E', padx=5, pady=2)

tbAlignment = Entry(configScript, textvariable=tbAlignmentBinding)
tbAlignment.grid(row=row, column=1, sticky='E', pady=2)

#Cost Model
lblCostModel = Label(configScript, text="Cost Model:")
lblCostModel.grid(row=row, column=5, sticky='E', padx=5, pady=2)

ddCostModel = OptionMenu(configScript, ddModel, "DupLoss","MulRF")
ddCostModel.grid(row=row, column=7, sticky='WE', padx=5)
row += 1

#Old Tree File Extension
lblOldTreeFileExtension = Label(configScript, text="Old Tree File Extension:")
lblOldTreeFileExtension.grid(row=row, column=0, padx=5, pady=2)

tbOldTreeFileExtension = Entry(configScript, textvariable=tbOldTreeFileBinding)
tbOldTreeFileExtension.grid(row=row, column=1, pady=2)

#New Tree File Extension
lblNewTreeFileExtension = Label(configScript, text="New Tree File Extension:")
lblNewTreeFileExtension.grid(row=row, column=5, sticky='E', padx=5, pady=2)

tbNewTreeFileExtension = Entry(configScript, textvariable=tbNewTreeFileBinding)
tbNewTreeFileExtension.grid(row=row, column=7, sticky='E', pady=2)
row += 1

#Iterations
lblIterations = Label(configScript, text="Iterations:")
lblIterations.grid(row=row, column=0, padx=5, pady=2)

tbIterations= Entry(configScript, textvariable = tbIterationsBinding)
tbIterations.grid(row=row, column=1, pady=2)

#Verbosity Level
lblVerbosity = Label(configScript, text="Verbosity Level:")
lblVerbosity.grid(row=row, column=5, sticky='E', padx=5, pady=2)

tbVerbosity = Entry(configScript, textvariable=tbVerbosityBinding)
tbVerbosity.grid(row=row, column=7, sticky='E', pady=2)
row += 1

#Extra Args
lblExtraArgs = Label(configScript, text="Extra Arguments:")
lblExtraArgs.grid(row=row, column=0, sticky='E', padx=5, pady=2)

tbExtraArgs = Entry(configScript, textvariable=tbExtraArgsBinding)
tbExtraArgs.grid(row=row, column=1, columnspan=7, sticky="WE", pady=3)
row += 1

#Output Panel
outputPanel = LabelFrame(window, text="Output Panel")
outputPanel.grid(row=1, columnspan=7, sticky='W', padx=5, pady=5, ipadx=5, ipady=5)

tOutput = Text(outputPanel, height=5)
tOutput.grid(row = 0, columnspan=7, sticky='E', padx=5, pady=5, ipadx=5, ipady=5)

#cmd = "treefix -s config/fungi.stres -S config/fungi.smap -A .nt.align -o .nt.raxml.tree -n .nt.raxml.treefix.tree -V 1 -l sim-fungi/0/0.nt.raxml.treefix.log sim-fungi/0/0.nt.raxml.tree --smodule treefix.models.mulrfmodel.MulRFModel"
btnExecute= Button(window, text= "Execute", command = popenAndCall).grid()
btnSaveAs = Button(window, text="Save Script As", command=saveScript).grid()
window.mainloop()







