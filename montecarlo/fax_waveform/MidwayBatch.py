####################################
## batch code for WF simulation
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
    print("<If use Public node (0 for no(xenon1t nodes); 1 for yes; 2 for kicp nodes)>")
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
IfUsePublicNodes = int(sys.argv[11])

MaxNumJob = 64
if not IfUsePublicNodes:
    MaxNumJob=200


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
    SubmitFile = OutputPath+"/submit_"+ RunString + ".sh"
    SubmitOutputFilename = OutputPath+"/submit_"+ RunString + ".log"
    SubmitErrorFilename = OutputPath+"/submit_"+ RunString + ".log"

    # create the basic submit 
    subp.call("echo '#!/bin/bash\n' >> "+SubmitFile, shell=True)
    subp.call("echo '#SBATCH --output="+SubmitOutputFilename+"' >> "+SubmitFile, shell=True)
    subp.call("echo '#SBATCH --error="+SubmitErrorFilename+"' >> "+SubmitFile, shell=True)
    subp.call("echo '#SBATCH --time=03:59:00' >> "+SubmitFile, shell=True)
    subp.call("echo '#SBATCH --account=pi-lgrandi' >> "+SubmitFile, shell=True)
    if IfUsePublicNodes==0:
        subp.call("echo '#SBATCH --qos=xenon1t' >> "+SubmitFile, shell=True)
        subp.call("echo '#SBATCH --partition=xenon1t\n' >> "+SubmitFile, shell=True)
    elif IfUsePublicNodes==2:
        subp.call("echo '#SBATCH --qos=xenon1t-kicp' >> "+SubmitFile, shell=True)
        subp.call("echo '#SBATCH --partition=kicp\n' >> "+SubmitFile, shell=True)

    Command = CurrentPath+"/./run_fax.sh "+str(PhotonNumLower)+" "+str(PhotonNumUpper)+" "+str(ElectronNumLower)+" "+str(ElectronNumUpper)+" "+str(PMTAfterpulseFlag)+" "+str(S2AfterpulseFlag)+" "+str(NumEvents)+" "+OutputGeneralPath+" "+RunString+" "+str(IfEnableS1S2Correlation)
    subp.call("echo '"+Command+"\n' >> "+SubmitFile, shell=True)

    SubmitPath = OutputPath

    #submit
    IfSubmitted=0
    while IfSubmitted==0:
        Partition = "sandyb" # public
        if not IfUsePublicNodes:
            Partition = "xenon1t"
        elif IfUsePublicNodes==2:
            Partition = "kicp"
        p1 = Popen(["squeue","--partition="+Partition, "--user="+CurrentUser], stdout=PIPE)
        p2 = Popen(["wc", "-l"], stdin=p1.stdout, stdout=PIPE)
        p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
        output = p2.communicate()[0]
        Status=subp.call("squeue --partition="+Partition+" --user="+CurrentUser +" | wc -l", shell=True)
        Output=int(output)
        #print(Status)
        
        print("Current job running number "+str(Output))            

        #if Status==0 and Output<MaxNumJob:
        if Status<=MaxNumJob:
            #sbatch it 
            subp.call("cd "+SubmitPath+";sbatch "+SubmitFile+";cd -", shell=True)
            IfSubmitted=1
            time.sleep(2.0)
        else:
            time.sleep(30) 
