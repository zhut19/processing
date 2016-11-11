#############################################
#
# Function is to convert the fax truth output to a pickle file.
# Warning: Selects the largest peak of each type
#
# Ref: http://xenon1t.github.io/pax/simulator.html#implementation-details
#
##############################################
import numpy as np
import pickle
import sys

if len(sys.argv)<2:
    print("========== Syntax =========")
    print("python ConvertFaxTruthToPickle.py .....")
    print("<fax truth csv (abs. path)>")
    print("<output pickle file (abs. path)>")
    exit()

InputFile = sys.argv[1]
OutputFile = sys.argv[2]

fin = open(InputFile)
lines = fin.readlines()
fin.close()

lines = lines[1:]

Data = {}
for line in lines:
    contents = line.split(",")
    event_id = int(contents[1])
    recoil_type = contents[6]
    area = float(contents[5])
    time = float(contents[14])
    if event_id in Data:
        # meaning already filled
        if Data[event_id][recoil_type]>area:
            continue
        else:
            Data[event_id][recoil_type]=area
            Data[event_id][recoil_type+"_time"]=time
            continue
    NewDict = {}
    NewDict['s1']=-1
    NewDict['s1_time']=0
    NewDict['s2']=-1
    NewDict['s2_time']=-1
    NewDict[recoil_type]=area
    NewDict[recoil_type+"_time"]=time
    Data[event_id]=NewDict

pickle.dump(Data, open(OutputFile,'wb'))
    
        
