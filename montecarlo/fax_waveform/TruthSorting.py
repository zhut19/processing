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
    print("python TruthSorting.py <truth file.csv (abs.)> <output file (no ext)> <output format; 0=pickle (default), 1=ROOT, 2=both>")
    exit()


TruthFile = sys.argv[1]
OutputFile = sys.argv[2]
if '.root' in OutputFile:
    OutputFile = OutputFile.split('.root')[0]
else:
    OutputFile = OutputFile.split('.pkl')[0]
OutputFormat=0
if len(sys.argv)>3:
    OutputFormat = float(sys.argv[3])

print ("Input file: ", TruthFile)

#################
## load the root files
## and TTrees
#################

###################
## need to sort and add the truth peak values into Data as well
## In truth file we want to keep both first and second largest peak
## both in time mean, sigma and area
####################
Data = {}


# load the truth data from csv
truth_data = pd.read_csv(TruthFile)
NumStepsInTruth = len(truth_data.index)

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
    while truth_data['event'][iteration_id]==event_id:
        tag = 2 # 0 for s1, 1 for s2, 2 for photoionization
        if truth_data['peak_type'][iteration_id] == 's1':
            tag = 0
        if truth_data['peak_type'][iteration_id] == 's2':
            tag = 1
        elif ifcounteds1==0:
            tag=0
            ifcounteds1=1
        else:
            tag=2
        if tag==0:
            #print("Iterator: "+str(iteration_id)+" -> S1")
            s1_time_truth = truth_data['t_mean_photons'][iteration_id]
            s1_time_std_truth = truth_data['t_sigma_photons'][iteration_id]
            s1_area_truth = truth_data['n_photons'][iteration_id]
            s1_area_top_fraction_truth = truth_data['top_fraction'][iteration_id]
        elif tag==1:
            #print("Iterator: "+str(iteration_id)+" -> S2")
            s2_electron_time_truth = truth_data['t_mean_electrons'][iteration_id]
            s2_first_electron_time_truth = truth_data['t_first_electron'][iteration_id]
            s2_time_truth = truth_data['t_mean_photons'][iteration_id]
            s2_time_std_truth = truth_data['t_sigma_photons'][iteration_id]
            s2_area_truth = truth_data['n_photons'][iteration_id]
            s2_area_top_fraction_truth = truth_data['top_fraction'][iteration_id]
            x_truth = truth_data['x'][iteration_id]
            y_truth = truth_data['y'][iteration_id]
        iteration_id += 1
        if iteration_id>=NumStepsInTruth:
            break
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

