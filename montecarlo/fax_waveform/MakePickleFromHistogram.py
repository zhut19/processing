####################################
## This code translate the histogram to pickle format
####################################

import numpy as np
import pickle

import ROOT
from ROOT import TFile
from ROOT import TH2D

import sys, os

if len(sys.argv)<2:
    print("========== Syntax ===========")
    print("python MakePickleFromHistogram.py .....")
    print("<input root file>")
    print("<histogram name>")
    print("<output pickle file>")
    exit()

InputROOTFilename = sys.argv[1]
HistogramName = sys.argv[2]
OutputPickleFilename = sys.argv[3]


####################################
# Open the root file and load the TH2D
####################################
pfile = TFile(InputROOTFilename)
hist = pfile.Get(HistogramName)

####################################
# translate into a dictionary
####################################
data = {}
data['s1nbins'] = int( hist.GetXaxis().GetNbins() )
data['s1lower'] = float( hist.GetXaxis().GetXmin() )
data['s1upper'] = float( hist.GetXaxis().GetXmax() )
data['lognbins'] = int( hist.GetYaxis().GetNbins() )
data['loglower'] = float( hist.GetYaxis().GetXmin() )
data['logupper'] = float( hist.GetYaxis().GetXmax() )
data['map'] = []

for i in range(data['s1nbins']):
    TmpList = []
    for j in range(data['lognbins']):
        cont = float(hist.GetBinContent(i+1, j+1) )
        TmpList.append(cont)
    data['map'].append( list(TmpList) )

####################################
## output to pickle
####################################

pickle.dump( data, open(OutputPickleFilename, 'wb') )
