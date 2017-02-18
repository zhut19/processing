###########################
## Code for sorting the truth root file(peak-by-peak) format into event-by-event format
## Output is a pickle file
## by Qing Lin
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

import root_pandas

import sys


if len(sys.argv)<2:
    print("============= Syntax =============")
    print("python TruthSorting.py <truth file.root (abs.)> <output file (no ext)> <output format; 0=pickle (default), 1=ROOT, 2=both>")
    exit()


TruthFile = sys.argv[1]
OutputFile = sys.argv[2]
OutputFile = OutputFile.split('.')[0]

OutputFormat=0
if len(sys.argv)>4:
    OutputFormat = float(sys.argv[4])

print ("Input file: ", TruthFile)

#################
## load the root files
## and TTrees
#################
pfile1 = TFile(TruthFile)

truth_tree = pfile1.Get("fax_truth")

if (not truth_tree):
    raise ValueError("Input file not complete")

NumStepsInTruth = truth_tree.GetEntries()

###################
## need to sort and add the truth peak values into Data as well
## In truth file we want to keep both first and second largest peak
## both in time mean, sigma and area
####################
Data = {}

# initialize Data for truth 
Data['index_truth'] = []
Data['s1_time_truth'] = [] 
Data['s1_time_std_truth'] = [] 
Data['s1_area_truth'] = [] 
Data['s1_area_top_fraction_truth'] = []
Data['s2_time_truth'] = [] 
Data['s2_electron_time_truth'] = [] 
Data['s2_first_electron_time_truth'] = [] 
Data['s2_time_std_truth'] = [] 
Data['s2_area_truth'] = [] 
Data['s2_area_top_fraction_truth'] = []
Data['x_truth'] = []
Data['y_truth'] = []

iteration_id = 0
truth_tree.GetEntry(iteration_id)
for event_id in range(10000000):
    if iteration_id>=NumStepsInTruth:
        break
    if (event_id+1)%100==0:
        print("==== processed_file: "+str(event_id+1)+" events finished loading")
    s1_time_truth = -1
    s1_time_std_truth = -1
    s1_area_truth = -1
    s1_area_top_fraction_truth = -1
    s2_electron_time_truth = -1
    s2_first_electron_time_truth = -1
    s2_time_truth = -1
    s2_time_std_truth = -1
    s2_area_truth = -1
    s2_area_top_fraction_truth = -1
    x_truth = -1e10
    y_truth = -1e10
    ifcounteds1 = 0
    while truth_tree.event==event_id:
        tag = 0 # 0 for s1, 1 for s2, 2 for photoionization
        if not str(truth_tree.n_electrons)=='nan':
            tag = 1
        elif ifcounteds1==0:
            tag=0
            ifcounteds1=1
        else:
            tag=2
        if tag==0:
            #print("Iterator: "+str(iteration_id)+" -> S1")
            s1_time_truth = truth_tree.t_mean_photons
            s1_time_std_truth = truth_tree.t_sigma_photons
            s1_area_truth = truth_tree.n_photons
            s1_area_top_fraction_truth = truth_tree.peak_top_fraction
        elif tag==1:
            #print("Iterator: "+str(iteration_id)+" -> S2")
            s2_electron_time_truth = truth_tree.t_mean_electrons
            s2_first_electron_time_truth = truth_tree.t_first_electron
            s2_time_truth = truth_tree.t_mean_photons
            s2_time_std_truth = truth_tree.t_sigma_photons
            s2_area_truth = truth_tree.n_photons
	        s2_area_top_fraction_truth = truth_tree.peak_top_fraction
            x_truth = truth_tree.x
            y_truth = truth_tree.y
        iteration_id += 1
        if iteration_id>=NumStepsInTruth:
            break
        truth_tree.GetEntry(iteration_id)
    Data['index_truth'].append(event_id)
    Data['s1_time_truth'].append(s1_time_truth)
    Data['s1_time_std_truth'].append(s1_time_std_truth)
    Data['s1_area_truth'].append(s1_area_truth)
    Data['s2_electron_time_truth'].append(s2_electron_time_truth)
    Data['s2_first_electron_time_truth'].append(s2_first_electron_time_truth)
    Data['s2_time_truth'].append(s2_time_truth)
    Data['s2_time_std_truth'].append(s2_time_std_truth)
    Data['s2_area_truth'].append(s2_area_truth)
    Data['s1_area_top_fraction_truth'].append(s1_area_top_fraction_truth)
    Data['s2_area_top_fraction_truth'].append(s2_area_top_fraction_truth)
    Data['x_truth'].append(x_truth)
    Data['y_truth'].append(y_truth)

print ("Number of events: ", event_id)

######################
## Convert to data format in pandas
######################
PandasData = {}
for item in Data:
    PandasData[item] = pd.Series(Data[item])
df = pd.DataFrame(PandasData)

#######################
## Save to ROOT
#######################
if OutputFormat == 1 or OutputFormat == 2:
    df.to_root(OutputFile+".root", 'fax_truth_sort')
    print ("Written to: ", OutputFile+".root")


#######################
## Save to pickle
#######################
if OutputFormat == 0 or OutputFormat == 2:
    pickle.dump(df, open(OutputFile+".pkl", 'wb'))
    print ("Written to: ", OutputFile+".pkl")

