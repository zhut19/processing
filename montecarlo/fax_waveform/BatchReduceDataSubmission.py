########################################################
## Code for batching the reduction of minitree S1S2Properties
## by Qing Lin @ 2017-01-12
########################################################
#!/usr/bin/python
import sys, array, os, getpass
from subprocess import call
import subprocess as subp
import time
import math as math
from subprocess import Popen, PIPE
import glob

if len(sys.argv)<=1:
    print("======== Usage =========")
    print("python ReduceDataNormal.py <filelist> <data path> <output path> <absolute path for submission> <if use public node (1) optional (2 for use kicp nodes)> <Submit ID>")
    print("======== List file format: ==========")
    print("ex.:")
    print("FakeWaveform_XENON1T_000000_pax")
    print("FakeWaveform_XENON1T_000001_pax")
    print("FakeWaveform_XENON1T_000002_pax")
    print(".....")
    exit()

EXE_Path = sys.argv[0].split("BatchReduceDataSubmission.py")[0]
ListFile = sys.argv[1]
DataPath = sys.argv[2]
OutputPath = sys.argv[3]
IfPublicNode = 1
AbsoluteSubmitPath = "Submit"
if len(sys.argv)>4:
    AbsoluteSubmitPath = sys.argv[4]
if len(sys.argv)>5:
    IfPublicNode = int(sys.argv[5])
SubmitID = 0
if len(sys.argv)>6:
    SubmitID = int(sys.argv[6])

##########################
## Some nuisance settings
##########################
CurrentPath = os.getcwd()
CurrentUser = getpass.getuser()
EXE = CurrentPath+"/"+EXE_Path+"/ReduceDataNormal.py"
#EXE = CurrentPath + EXE_Path+"/reduce_peak_level_more_info.py"
MaxNumJob = 64
if not IfPublicNode:
    MaxNumJob = 200

##########################
## Open/load list file
##########################
fin = open(ListFile)
lines = fin.readlines()
fin.close()

##########################
## Job submission
##########################

for j, line in enumerate(lines):
    # create submit directory
    SubmitPath = AbsoluteSubmitPath + "/" + str(j) + "_" + str(SubmitID)
    if os.path.exists(SubmitPath):
        subp.call("rm -r "+SubmitPath, shell=True)
    subp.call("mkdir "+SubmitPath, shell=True)
    # create submit file
    SubmitFile = SubmitPath + "/submit"
    if os.path.exists(SubmitFile):
        subp.call("rm "+SubmitFile, shell=True)
    # start to fill in submit 
    filename = line[:-1]
    if len(filename)<2:
        continue
    print("To process -> "+filename)
    # create the submit 
    subp.call("echo '#!/bin/bash\n' >> "+SubmitFile, shell=True)
    subp.call("echo '#SBATCH --output="+SubmitPath+"/myout_"+str(SubmitID)+"_"+str(j)+".txt \n' >> "+SubmitFile, shell=True)
    subp.call("echo '#SBATCH --error="+SubmitPath+"/myerr_"+str(SubmitID)+"_"+str(j)+".txt\n' >> "+SubmitFile, shell=True)
    subp.call("echo '#SBATCH --time=04:59:00\n' >> "+SubmitFile, shell=True)
    if not IfPublicNode:
        subp.call("echo '#SBATCH --account=pi-lgrandi\n' >> "+SubmitFile, shell=True)
        subp.call("echo '#SBATCH --qos=xenon1t\n' >> "+SubmitFile, shell=True)
        subp.call("echo '#SBATCH --partition=xenon1t\n' >> "+SubmitFile, shell=True)
    elif IfPublicNode==2:
        subp.call("echo '#SBATCH --account=pi-lgrandi\n' >> "+SubmitFile, shell=True)
        subp.call("echo '#SBATCH --qos=xenon1t-kicp\n' >> "+SubmitFile, shell=True)
        subp.call("echo '#SBATCH --partition=kicp\n' >> "+SubmitFile, shell=True)
    #subp.call("echo '. /home/mcfate/Env/GlobalPAXEnv.sh\n\n' >> "+SubmitFile, shell=True)
    subp.call("echo 'export PATH=/project/lgrandi/anaconda3/bin:$PATH' >> "+SubmitFile, shell=True)
    subp.call("echo 'source activate pax_head' >> "+SubmitFile, shell=True)
    print("python "+EXE+" "+filename+" "+DataPath)
    subp.call("echo 'python "+EXE+" "+filename+" "+DataPath+"' >> "+SubmitFile, shell=True)
    #subp.call("echo 'cp "+SubmitFile+" /home/jh3226/
    subp.call("echo 'mv "+SubmitPath+"/"+filename+"_S1S2Properties.root  "+OutputPath+"' >> "+SubmitFile, shell=True)
    #subp.call("echo 'mv "+SubmitPath+"/"+filename+"_PeakEfficiency.root  "+OutputPath+"' >> "+SubmitFile, shell=True)
    
    #submit
    IfSubmitted=0
    while IfSubmitted==0:
        Partition = "sandyb" # public
        if not IfPublicNode:
            Partition = "xenon1t"
        elif IfPublicNode==2:
            Partition = "kicp"
        p1 = Popen(["squeue","--partition="+Partition,"--user="+CurrentUser], stdout=PIPE)
        p2 = Popen(["wc", "-l"], stdin=p1.stdout, stdout=PIPE)
        p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
        output = p2.communicate()[0]
        Status=subp.call("squeue --partition="+Partition+" --user="+CurrentUser+" | wc -l", shell=True)
        Output=int(output)
        #print(Status)
        print("Current job running number "+str(Output))            
        if Status==0 and Output<MaxNumJob:
            #sbatch it 
            subp.call("cd "+SubmitPath+";sbatch "+SubmitFile+";cd -", shell=True)
            IfSubmitted=1   
            subp.call("rm "+SubmitFile, shell=True) 
            time.sleep(1)
        else:
            time.sleep(30) 




