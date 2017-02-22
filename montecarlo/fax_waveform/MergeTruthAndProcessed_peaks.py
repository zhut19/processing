###########################
## Code for merging the truth & processed info from simulated data
## by Qing Lin
## 1) Truth info from the output pickle by TruthSorting.py
## 2) Processed info from any minitree, but need to specify which branches to keep in the merged file
## Notice that the external file is needed for this specification
## And for the convenience of the user, it is better to name the branch in output the same way
#########
## @ 2017-01-09
## Please NOTE the code can only be used with single S1&S2 simulation
## Double/Multiple peak simulation is not available in merging/minitree yet
###########################

import pickle 
import pandas as pd

import ROOT
from ROOT import TFile
from ROOT import TTree

import sys


if len(sys.argv)<2:
    print("============= Syntax =============")
    print("python MergeTruthAndProcessed.py <configuration file> <truth file.pkl (abs.)> <processed file.root (abs.)> <output file.pkl>")
    exit()


ConfigFile = sys.argv[1]
TruthFile = sys.argv[2]
ProcessedFile = sys.argv[3]
OutputFile = sys.argv[4]

#################
## load the config file
#################
fin = open(ConfigFile)
lines = fin.readlines()
fin.close()

processedTreeName = ""
BranchesToKeep = [['index', 'index_processed']] # default put index there for merging

for i, line in enumerate(lines):
    if i==0:
        contents = line[:-1].split('Name: ')
        if len(contents)<=1:
             raise ValueError("Tree name not properly defined")
        processedTreeName = contents[1]
    else:
        line = line.replace("\t", " ")
        line = line.replace("\n", " ")
        contents = line.split(" ")
        for content in list(contents):
            if content=='':
                contents.remove(content)
        BranchesToKeep.append(
                                                 [
                                                  contents[0],
                                                  contents[1],
                                                 ]
                                                 )



#################
## load the input files
## and pandas and TTrees
#################
truthData = pickle.load( open(TruthFile, 'rb') )

pfile2 = TFile(ProcessedFile)
processed_tree = pfile2.Get(processedTreeName)

#if (not processed_tree):
#    raise ValueError("Input file not complete")

#NumEventsInData = processed_tree.GetEntries()
NumStepsInTruth = 0
for i, item in enumerate(truthData):
    NumStepsInTruth = int(len(truthData[item]))
    if i==0:
        break


###################
## load the data dict from processed root file
###################
#df = pd.DataFrame(processedPandasData)
import root_numpy
df = pd.DataFrame.from_records(root_numpy.root2rec(ProcessedFile))
for branch_name in list(df):
    if ('length' in branch_name) and (branch_name != 'peaks_length'):
        df.drop(branch_name, 1)

#####################
## Merge the new dictionary to existing dataframe
#####################

df = df.merge(truthData, left_on='event_number', right_on='index_truth', how='outer')

#######################
## Save to pickle
#######################
#pickle.dump(df, open(OutputFile, 'wb'))
df.to_pickle(OutputFile)
