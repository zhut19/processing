####################################
## Code for merging all the pickle under one directory into one
## the output is the Merged.pkl under target directory
## by Qing Lin
####################################
import pickle
import sys, os
import subprocess as subp
import numpy as np
import pandas as pd

if len(sys.argv)<=1:
    print("======== Syntax ========")
    print("python CombinePickles.py <path>")
    exit()

OutputFilename = ""
InputListFilename = ""
InputFiles = []

OperationPath = sys.argv[1]
InputListFilename = OperationPath+"/TmpList.txt"

if os.path.exists(InputListFilename):
    subp.call("rm "+InputListFilename, shell=True)
subp.call(" ls "+OperationPath+"/*.pkl >> "+InputListFilename, shell=True)




fin = open(InputListFilename)
lines = fin.readlines()
fin.close()
for line in lines:
    if len(line)<2:
        continue
    InputFiles.append(line[:-1])
    print(line[:-1])


# Get the base from the first file
Data = pickle.load(open(InputFiles[0], 'rb'))

# add to data
for i, InputFile in enumerate(InputFiles):
    if i==0:
        continue
    AddData = pickle.load(open(InputFile, 'rb'))
    Data = Data.append(AddData, ignore_index=True)
    print("\n finishing"+InputFile+"\n")

# output
OutputFilename = OperationPath+"/Merged.pkl"
pickle.dump(Data, open(OutputFilename,'wb'))

# delete temporary list
subp.call("rm "+InputListFilename, shell=True)
