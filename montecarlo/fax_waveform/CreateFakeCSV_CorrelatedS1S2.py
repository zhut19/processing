#################################
## Sub-code used in WF simulation
## It creates a csv file for the input of fax
## using the 2d-pdf from an input histogram
## by Qing Lin
## @ 2016-09-12
##
## HARDCODE WARNING: The FV dimensions below need to be modified
##                   according to the detector you wish to simulate
#################################
import sys
import numpy as np
import scipy as sp

if len(sys.argv)<2:
    print("========= Syntax ==========")
    print("python CreateFakeCSV.py ..... ")
    print("<detector: XENON100, XENON1T>")
    print("<pkl file for Log(S2/S1) verse S1>")
    print("<nominal g1 value>")
    print("<nominal g2 value>")
    print("<number of events>")
    print("<recoil type: ER, NR>")
    print("<output file (abs. path)>")
    exit()

Detector = sys.argv[1]
Band2DPDFFilename = sys.argv[2]
NominalG1Value = float(sys.argv[3])
NominalG2Value = float(sys.argv[4])
NumEvents = int(sys.argv[5])
DefaultType = sys.argv[6]
OutputFilename = sys.argv[7]

####################################
## Some nuisance parameters (HARDCODE WARNING):
####################################
MaxDriftTime = 650. # us


####################################
## Some functions (HARDCODE WARNING):
####################################

# Current FV cut for Xe1T
scalecmtomm=1
def radius2_cut(zpos):
    return 1400*scalecmtomm**2+(zpos+100*scalecmtomm)*(2250-1900)*scalecmtomm/100

def IfPassFV(x,y,z):

    if Detector == "XENON100":
        # check if the x,y,z passing X48kg0
        I = np.power( (z+15.)/14.6, 4.)
        I += np.power( (x**2+y**2)/20000., 4.)
        if I<1:
            return True
    elif Detector == "XENON1T": # NEED TO UPDATE THIS
        Zlower, Zupper = -90*scalecmtomm, -15*scalecmtomm
        Zcut = ((z>=Zlower) & (z<=Zupper))
        R2upper=radius2_cut(z)
        Rcut = (x**2+y**2<R2upper)
        if(Zcut & Rcut):
            return True

    return False


def RandomizeFV():

    # randomize the X, Y, Z according to X48kg FV
    if Detector == "XENON100":
        Zlower, Zupper = -14.6-15.0, -14.6+15.0
        Rlower, Rupper = -np.sqrt(200.), np.sqrt(200.)

    elif Detector == "XENON1T": # NEED TO UPDATE THIS
        Zlower, Zupper = -90*scalecmtomm, -15*scalecmtomm
        Rlower, Rupper = -46*scalecmtomm, 46*scalecmtomm

    for i in range(100000):
        x = np.random.uniform(Rlower,Rupper)
        y = np.random.uniform(Rlower,Rupper)
        z = np.random.uniform(Zlower,Zupper)
        if IfPassFV(x,y,z):
            return (x,y,z)
    return (0,0,0)

####################################
## S1&S2 generator loading
####################################
import PhotonChargeGenerator
from PhotonChargeGenerator import MyPhotonChargeGenerator

pGen = MyPhotonChargeGenerator(
                                                          Band2DPDFFilename,
                                                          NominalG1Value,
                                                          NominalG2Value,
                                                         )


####################################
## Starts to create
####################################
# Some default
DefaultEventTime = MaxDriftTime*1000.
##########
fout = open(OutputFilename, 'w')
# headers
fout.write("instruction,recoil_type,x,y,depth,s1_photons,s2_electrons,t\n")
# events loop
for i in range(NumEvents):
    fout.write(str(i)+",")
    fout.write(DefaultType+",")
    X, Y, Z = RandomizeFV()
    fout.write(str(X)+",")
    fout.write(str(Y)+",")
    fout.write(str(-Z)+",")
    NumPhoton, NumElectron = pGen.GetPhotonChargeNum()
    fout.write(str(int(NumPhoton))+",")
    fout.write(str(int(NumElectron))+",")
    fout.write(str(DefaultEventTime)+"\n")

