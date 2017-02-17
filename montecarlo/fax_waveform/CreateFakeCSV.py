#################################
## Sub-code used in WF simulation
## It creates a csv file for the input of fax
## by Qing Lin
## @ 2016-09-12
##
## HARDCODE WARNING: The FV dimensions below need to be modified
##                   according to the detector you wish to simulate
##
## Ref: http://xenon1t.github.io/pax/simulator.html#instruction-file-format
## Code: https://github.com/XENON1T/pax/blob/master/pax/plugins/io/WaveformSimulator.py#L244
##
#################################
import sys
import numpy as np
import scipy as sp

if len(sys.argv)<2:
    print("========= Syntax ==========")
    print("python CreateFakeCSV.py ..... ")
    print("<detector: XENON100, XENON1T>")
    print("<number of events>")
    print("<photon number lower>")
    print("<photon number upper>")
    print("<electron number lower>")
    print("<electron number upper>")
    print("<recoil type: ER, NR>")
    print("<output file (abs. path)>")
    print("<If force S1-S2 correlation (0 for no; 1 for yes)>")
    exit()

Detector = sys.argv[1]
NumEvents = int(sys.argv[2])
PhotonNumLower = float(sys.argv[3])
PhotonNumUpper = float(sys.argv[4])
ElectronNumLower = float(sys.argv[5])
ElectronNumUpper = float(sys.argv[6])
DefaultType = sys.argv[7]
OutputFilename = sys.argv[8]
IfS1S2Correlation = True
if int(sys.argv[9])==0:
    IfS1S2Correlation = False

####################################
## Some nuisance parameters (HARDCODE WARNING):
####################################
MaxDriftTime = 675. # us


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
        #Zlower, Zupper = -90*scalecmtomm, -15*scalecmtomm
        Zlower, Zupper = -120*scalecmtomm, -1*scalecmtomm
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
        #Zlower, Zupper = -90*scalecmtomm, -15*scalecmtomm
        Zlower, Zupper = -90*scalecmtomm, -1*scalecmtomm
        Rlower, Rupper = -46*scalecmtomm, 46*scalecmtomm

    for i in range(100000):
        x = np.random.uniform(Rlower,Rupper)
        y = np.random.uniform(Rlower,Rupper)
        z = np.random.uniform(Zlower,Zupper)
        if IfPassFV(x,y,z):
            return (x,y,z)
    return (0,0,0)

def RandomizeFVS1():

    # randomize the X, Y, Z according to X48kg FV
    if Detector == "XENON100":
        Zlower, Zupper = -14.6-15.0, -14.6+15.0
        Rlower, Rupper = -np.sqrt(200.), np.sqrt(200.)

    elif Detector == "XENON1T": # NEED TO UPDATE THIS
        #Zlower, Zupper = -90*scalecmtomm, -15*scalecmtomm
        Zlower, Zupper = -103*scalecmtomm, -101*scalecmtomm
        Rlower, Rupper = -46*scalecmtomm, 46*scalecmtomm

    for i in range(100000):
        x = np.random.uniform(Rlower,Rupper)
        y = np.random.uniform(Rlower,Rupper)
        z = np.random.uniform(Zlower,Zupper)
        if IfPassFV(x,y,z):
            return (x,y,z)
    return (0,0,0)


####################################
## Starts to create
####################################
# Some default
DefaultEventTime = MaxDriftTime*1000.
##########
fout = open(OutputFilename, 'w')
# headers
fout.write("instruction,recoil_type,x,y,depth,s1_photons,s2_electrons,t\n")
if IfS1S2Correlation:
    # events loop
    for i in range(NumEvents):
        fout.write(str(i)+",")
        fout.write(DefaultType+",")
        X, Y, Z = RandomizeFV()
        fout.write(str(X)+",")
        fout.write(str(Y)+",")
        #fout.write("random,")
        #fout.write("random,")
        fout.write(str(-Z)+",")
        NumPhoton = int( np.random.uniform(PhotonNumLower, PhotonNumUpper) )
        fout.write(str(NumPhoton)+",")
        NumElectron = int( np.random.uniform(ElectronNumLower, ElectronNumUpper) )
        fout.write(str(NumElectron)+",")
        fout.write(str(DefaultEventTime)+"\n")
else:
    # events loop S1-S2 no correlation
    for i in range(NumEvents):
        # first for S1
        fout.write(str(i)+",")
        fout.write(DefaultType+",")
        X, Y, Z = RandomizeFVS1()
        fout.write(str(X)+",")
        fout.write(str(Y)+",")
        fout.write(str(-Z)+",")
        NumPhoton = int( np.random.uniform(PhotonNumLower, PhotonNumUpper) )
        fout.write(str(NumPhoton)+",")
        fout.write("0,")
        fout.write(str(DefaultEventTime)+"\n")
        # second for S2
        fout.write(str(i)+",")
        fout.write(DefaultType+",")
        X, Y, Z = RandomizeFV()
        fout.write(str(X)+",")
        fout.write(str(Y)+",")
        fout.write(str(-Z)+",")
        fout.write("0,")
        NumElectron = int( np.random.uniform(ElectronNumLower, ElectronNumUpper) )
        fout.write(str(NumElectron)+",")
        TimeOffset = np.random.uniform(0, MaxDriftTime*1000.)
        S2EventTime = DefaultEventTime+TimeOffset
        fout.write(str(S2EventTime)+"\n")
fout.close()
