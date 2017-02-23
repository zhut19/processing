####################################
## batch code for WF simulation
## @ 2017-02-22
## by Qing Lin
## On OSG
####################################
import sys, array, os, getpass
from subprocess import call
import subprocess as subp
import time
import math as math
from subprocess import Popen, PIPE

if len(sys.argv)<2:
    print("========= Syntax ========")
    print("python BatchSimulation.py ....")
    print("<Output path (abs.)>")
    print("<number of jobs>")
    print("<number of events in each job>")
    print("<enable PMT after pulses ?(0 for disable)>")
    print("<enable S2 after pulses ?(0 for disable)>")
    print("<photon number lower>")
    print("<photon number upper>")
    print("<electron number lower>")
    print("<electron number upper>")
    print("<If enable S1-S2 correlation (0 for no, 1 for yes)>")
    exit()

OutputGeneralPath = sys.argv[1]
NumJobs = int(sys.argv[2])
NumEvents = int(sys.argv[3])
PMTAfterpulseFlag = int(sys.argv[4])
S2AfterpulseFlag = int(sys.argv[5])
PhotonNumLower = int(sys.argv[6])
PhotonNumUpper = int(sys.argv[7])
ElectronNumLower = int(sys.argv[8])
ElectronNumUpper = int(sys.argv[9])
IfEnableS1S2Correlation = int(sys.argv[10])



##### Start batching #########
CurrentPath = os.getcwd()
print (CurrentPath)
CurrentUser = getpass.getuser()
for i in range(NumJobs):

    RunString = "%06d" % i
    
    # create folder
    OutputPath = OutputGeneralPath + "/" + RunString
    if os.path.exists(OutputPath):
        subp.call("rm -r "+OutputPath, shell=True)
    subp.call("mkdir -p "+OutputPath, shell=True)
    
    # define filenames
    Executable = CurrentPath+"/run_fax.sh"
    SubmitFile = OutputPath+"/submit_"+ RunString + ""
    SubmitOutputFilename = OutputPath+"/submit_"+ RunString + ".out"
    SubmitErrorFilename = OutputPath+"/submit_"+ RunString + ".err"
    SubmitLogFilename = OutputPath+"/submit_"+ RunString + ".log"

    # create the basic submit 
    subp.call("echo '############################\n' >> "+SubmitFile, shell=True)
    subp.call("echo '## for osg submission\n' >> "+SubmitFile, shell=True)
    subp.call("echo '############################\n' >> "+SubmitFile, shell=True)
    subp.call("echo '\n\n\n\n' >> "+SubmitFile, shell=True)
    subp.call("echo 'executable = "+Executable+"' >> "+SubmitFile, shell=True)
    subp.call("echo 'universe = vanilla' >> "+SubmitFile, shell=True)
    subp.call("echo '\n\n\n\n' >> "+SubmitFile, shell=True)
    
    Arguments = str(PhotonNumLower)+" "+str(PhotonNumUpper)+" "+str(ElectronNumLower)+" "+str(ElectronNumUpper)+" "+str(PMTAfterpulseFlag)+" "+str(S2AfterpulseFlag)+" "+str(NumEvents)+" "+OutputGeneralPath+" "+RunString+" "+str(IfEnableS1S2Correlation)
    subp.call("echo 'arguments = "+Arguments+"' >> "+SubmitFile, shell=True)
    subp.call("echo 'output = "+SubmitOutputFilename+"' >> "+SubmitFile, shell=True)
    subp.call("echo 'error = "+SubmitErrorFilename+"' >> "+SubmitFile, shell=True)
    subp.call("echo 'log = "+SubmitLogFilename+"' >> "+SubmitFile, shell=True)
    subp.call("echo '\n\n\nqueue\n' >> "+SubmitFile, shell=True)
    
    subp.call("cd "+OutputPath+"; condor_submit "+SubmitFile+";", shell=True)
    time.sleep(0.5)
