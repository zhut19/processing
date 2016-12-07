#!/usr/bin/env python

import argparse
import math
import os
import subprocess
import sys
import shlex
from shutil import copyfile
import time

HTCONDOR_SUBMIT_FILE = '''
executable     = run_sim.sh
universe       = vanilla

Error   = log/err.$(Cluster).$(Process)
Output  = log/out.$(Cluster).$(Process)
Log     = log/log.$(Cluster).$(Process)

Requirements = (HAS_CVMFS_xenon_opensciencegrid_org ) && \\
               (OpSysAndVer =?= "CentOS6" || OpSysAndVer =?= "RedHat6" || OpSysAndVer =?= "SL6") && \\
               (GLIDEIN_ResourceName =!= "BNL-ATLAS") && \\
               (GLIDEIN_ResourceName =!= "BU_ATLAS_Tier2") && \\
               (GLIDEIN_ResourceName =!= "AGLT2")
+WantExperimental = True
+WANT_RCC_ciconnect = True

transfer_executable = True
transfer_output_files = output
when_to_transfer_output = ON_EXIT
arguments = $(id) $(flavor) $(config) $(events) $(mc_version) $(pax_version)
queue 1

'''

MC_PATH = '/cvmfs/xenon.opensciencegrid.org/releases/mc/'
PAX_PATH = "/cvmfs/xenon.opensciencegrid.org/releases/anaconda/2.4/envs/"
MC_FLAVORS = ('G4', 'NEST', 'G4p10')
CONFIGS = (
'AmBe_neutronISO',
'Cryostat_Co60',
'Cryostat_K40',
'Cryostat_neutron',
'Cryostat_Th232',
'Cryostat_U238',
'DDFusion_neutron',
#'Disk15m_muon', # Not yet tested
'ib1sp1_Cs137',
'ib1sp2_Cs137',
#'optPhot', # Not yet tested
'Pmt_Co60',
'Pmt_K40',
'Pmt_neutron',
'Pmt_Th232',
'Pmt_U238',
'TPC_2n2b',
'TPC_ERsolar',
'TPC_Kr83m',
'TPC_Kr85',
'TPC_Rn222',
'TPC_WIMP',
'WholeLXe_Rn220',
'WholeLXe_Rn222'
)

# condor / osg specific constants
HTCONDOR_SUBMIT_FILENAME = 'mc.submit'
DAG_FILE = 'mc.dag'
DAG_RETRIES = 10


def get_mc_versions():
    """
    Return a tuple with mc versions that are available

    :return: tuple with string of mc versions available
    """
    try:
        if os.path.isdir(MC_PATH):
            versions = os.listdir(MC_PATH)
            versions.sort()
            return tuple(versions)
        return ()
    except OSError:
        sys.stderr.write("Can't get mc versions from {0}\n".format(MC_PATH))
        # hard coded for xe-grid
        return ('v0.1.0')


def get_pax_versions():
    """
    Return a tuple with pax versions that are available

    :return: tuple with string of mc versions available
    """
    try:
        versions = []
        if not os.path.isdir(PAX_PATH):
            return ()
        for entry in os.listdir(PAX_PATH):
            if entry.startswith('pax_'):
                versions.append(entry.replace('pax_', ''))
        versions.sort()
        return tuple(versions)
    except OSError:
        sys.stderr.write("Can't get pax versions from {0}\n".format(PAX_PATH))
        # hard coded for xe-grid
        return ('v6.1.1')

# needs to be set after functions defined
MC_VERSIONS = get_mc_versions()
PAX_VERSIONS = get_pax_versions()


def get_num_jobs(total_events, batch_size):
    """
    Get the number of jobs to use for MC simulation

    :param total_events: total number of events to generate
    :param batch_size:  number of events to generate per job
    :return: number of jobs to use
    """
    num_jobs = int(math.ceil(total_events / float(batch_size)))
    return num_jobs


def osg_submit(mc_config, mc_flavor, mc_version, pax_version, num_events, batch_size):
    """
    Generate and submit jobs to OSG

    :param mc_config: MC config to use
    :param mc_flavor: MC flavor to use
    :param mc_version: version of MC code to use
    :param pax_version: version of PAX code to use
    :param num_events: total number of events to generate
    :param batch_size: number of events to generate per job
    :return: True on success, False otherwise
    """

    if os.path.exists(HTCONDOR_SUBMIT_FILENAME):
        sys.stderr.write("Submit file at {0} ".format(HTCONDOR_SUBMIT_FILENAME) +
                         "already exists, exiting!\n")
        return 1

    if os.path.exists(DAG_FILE):
        sys.stderr.write("DAG file at {0} ".format(DAG_FILE) +
                         "already exists, exiting!\n")
        return 1

    num_jobs = get_num_jobs(num_events, batch_size)
    sys.stdout.write("Generating {0} events ".format(num_events) +
                     "using {0} jobs\n".format(num_jobs))

    with open(DAG_FILE, 'wt') as dag_file:
        for job in range(0, num_jobs):
            dag_file.write("JOB MC.{0} {1}\n".format(job,
                                                     HTCONDOR_SUBMIT_FILENAME))
            dag_file.write('VARS MC.{0} flavor="{1}" '.format(job, mc_flavor))
            dag_file.write('config="{0}" '.format(mc_config))
            dag_file.write('pax_version="{0}" '.format(pax_version))
            dag_file.write('mc_version="{0}" '.format(mc_version))
            if job == (num_jobs - 1):
                left_events = num_events % batch_size
                if left_events == 0:
                    left_events = batch_size
                dag_file.write('events="{0}" '.format(left_events))
            else:
                dag_file.write('events="{0}" '.format(batch_size))
            dag_file.write('id="{0}" '.format(job))

            dag_file.write("\n")
            dag_file.write("Retry MC.{0} {1}\n".format(job, DAG_RETRIES))
    with open(HTCONDOR_SUBMIT_FILENAME, 'wt') as submit_file:
        submit_file.write(HTCONDOR_SUBMIT_FILE)

    if not os.path.exists('output'):
        os.mkdir('output')
    if not os.path.exists('log'):
        os.mkdir('log')
    try:
        subprocess.check_call(['condor_submit_dag', 'mc.dag'])
        sys.stdout.write("Submitted jobs to OSG\n")
        return True
    except subprocess.CalledProcessError as e:
        sys.stderr.write("Exception while submitting dag: {0}\n".format(e))
        return False


def set_folders(ids_directory, jdl_directory):

    if not os.path.exists(ids_directory):
        os.makedirs(ids_directory)

    if not os.path.exists(jdl_directory):
        os.makedirs(jdl_directory)

    return 0

def set_jdl_arguments(mc_config, mc_flavor, mc_version, pax_version, str_job_nb, jdl_directory, jdl_name, num_events):

    command_line = "sed -i s/RUN_NUMBER/" + str_job_nb + "/g " + jdl_directory + "/" + jdl_name
    args = shlex.split(command_line)
    execute = subprocess.Popen(args,
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               shell=False,
                               universal_newlines=False)
    execute.communicate()

    command_line = "sed -i s/MC_FLAVOR/" + mc_flavor + "/g " + jdl_directory + "/" + jdl_name
    args = shlex.split(command_line)
    execute = subprocess.Popen(args,
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               shell=False,
                               universal_newlines=False)
    execute.communicate()

    command_line = "sed -i s/MC_CONFIG/" + mc_config + "/g " + jdl_directory + "/" + jdl_name
    args = shlex.split(command_line)
    execute = subprocess.Popen(args,
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               shell=False,
                               universal_newlines=False)
    execute.communicate()

    command_line = "sed -i s/NB_EVENTS/" + str(num_events) + "/g " + jdl_directory + "/" + jdl_name
    args = shlex.split(command_line)
    execute = subprocess.Popen(args,
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               shell=False,
                               universal_newlines=False)
    execute.communicate()

    command_line = "sed -i s/MC_VERSION/" + mc_version + "/g " + jdl_directory + "/" + jdl_name
    args = shlex.split(command_line)
    execute = subprocess.Popen(args,
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               shell=False,
                               universal_newlines=False)
    execute.communicate()

    command_line = "sed -i s/PAX_VERSION/" + pax_version + "/g " + jdl_directory + "/" + jdl_name
    args = shlex.split(command_line)
    execute = subprocess.Popen(args,
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               shell=False,
                               universal_newlines=False)
    execute.communicate()

    return 0

def egi_submit(mc_config, mc_flavor, mc_version, pax_version, num_events, batch_size):
    """
    Generate and submit jobs to EGI

    :param mc_config: MC config to use
    :param mc_flavor: MC flavor to use
    :param mc_version: version of MC code to use
    :param pax_version: version of PAX code to use
    :param num_events: total number of events to generate
    :param batch_size: number of events to generate per job
    :return: True on success, False otherwise
    """

    ids_directory = "./job_id"
    jdl_directory = "./jdl_files"
    set_folders(ids_directory, jdl_directory)

    filelist = [f for f in os.listdir(jdl_directory) if f.endswith(".bak")]
    for f in filelist:
        os.remove(f)

    num_jobs = get_num_jobs(num_events, batch_size)
    job_nb = 1

    while (job_nb <= num_jobs):

        str_job_nb = str(job_nb)

        jdl_template_name = "job_template.jdl"
        jdl_name = "job_" + str_job_nb + ".jdl"

        destination_file = jdl_directory + "/" + jdl_name
        copyfile(jdl_template_name, destination_file)

        set_jdl_arguments(mc_config, mc_flavor, mc_version, pax_version, str_job_nb, jdl_directory, jdl_name, num_events)

        jdl_path = jdl_directory + "/" + jdl_name
        id_file  = "id_" + str_job_nb + ".txt"
        id_path  = ids_directory + "/" + id_file

        command_line_2 = "glite-wms-job-submit -a -e " \
                         "https://wms-multi.grid.cnaf.infn.it:7443/glite_wms_wmproxy_server " \
                         "-o " + id_path + " " + jdl_path
        args2 = shlex.split(command_line_2)
        execute2 = subprocess.Popen(args2,
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT,
                                   shell=False,
                                   universal_newlines=False)
        stdout_value, stderr_value = execute2.communicate()
        stdout_value = stdout_value.decode("utf-8")
        stdout_value = stdout_value.split("\n")
        stdout_value = list(filter(None,
                                   stdout_value))
        print stdout_value, stderr_value

        time.sleep(3)
        job_nb += 1

    return True

def run_main():
    """
    Main function to process user input and then generate the appropriate submit files

    :return: exit code -- 0 on success, 1 otherwise
    """

    parser = argparse.ArgumentParser(description="Create a set of files for doing MC simulation for X1T")

    parser.add_argument('--flavor', dest='mc_flavor',
                        action='store', required=True,
                        choices=MC_FLAVORS,
                        help='MC flavor to use')
    parser.add_argument('--config', dest='mc_config',
                        action='store', required=True,
                        choices=CONFIGS,
                        help='configuration to use')
    parser.add_argument('--events', dest='num_events',
                        action='store', required=True,
                        type=int,
                        help='number of events to generate')
    parser.add_argument('--batch-size', dest='batch_size',
                        action='store', default=2000, type=int,
                        help='max number of events to generate per job '
                             '(default is 2000)')
    parser.add_argument('--mc-version', dest='mc_version',
                        choices=MC_VERSION,
                        action='store', required=True,
                        help='version of MC code to use')
    parser.add_argument('--pax-version', dest='pax_version',
                        choices=PAX_VERSION,
                        action='store', required=True,
                        help='version of pax to use')
    parser.add_argument('--grid-type', dest='grid_type',
                        choices=['osg', 'egi'],
                        action='store', required=True,
                        help='Grid to submit to')

    args = parser.parse_args(sys.argv[1:])
    if args.num_events == 0:
        sys.stdout.write("No events to generate, exiting")
        return 0

    if args.grid_type == 'osg':
        if osg_submit(args.mc_config,
                      args.mc_flavor,
                      args.mc_version,
                      args.pax_version,
                      args.num_events,
                      args.batch_size):
            return 0
        return 1
    elif args.grid_type == 'egi':
        if egi_submit(args.mc_config,
                      args.mc_flavor,
                      args.mc_version,
                      args.pax_version,
                      args.num_events,
                      args.batch_size):
            return 0
        return 1
    else:
        return 1

if __name__ == '__main__':
    sys.exit(run_main())
