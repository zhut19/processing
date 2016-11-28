#!/usr/bin/env python

import argparse
import math
import os
import sys

SUBMIT_FILE = '''
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

MC_FLAVORS = ('G4', 'NEST', 'G4p10')
CONFIGS = ('TPC_Kr83m', 'TPC_Kr85', 'WholeLXe_Rn220', 'WholeLXe_Rn222')
MC_PATH = '/cvmfs/xenon.opensciencegrid.org/releases/mc/'
PAX_PATH = "/cvmfs/xenon.opensciencegrid.org/releases/anaconda/2.4/envs/"


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
        return ()


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
        return ()


MC_VERSIONS = get_mc_versions()
PAX_VERSIONS = get_pax_versions()


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
                        choices=MC_VERSIONS,
                        action='store', required=True,
                        help='version of MC code to use')
    parser.add_argument('--pax-version', dest='pax_version',
                        choices=PAX_VERSIONS,
                        action='store', required=True,
                        help='version of pax to use')
    parser.add_argument('--dagfile-file', dest='dag_file',
                        action='store', default='mc.dag',
                        help='file to write dag to')
    parser.add_argument('--submit-file', dest='submit_file',
                        action='store', default='mc.submit',
                        help='name of submit to write out')
    parser.add_argument('--retries', dest='retries',
                        action='store', default=10, type=int,
                        help='max number of times to retry a job '
                             '(default is 10)')

    args = parser.parse_args(sys.argv[1:])
    if args.num_events == 0:
        sys.stdout.write("No events to generate, exiting")
        return 0
    num_jobs = int(math.ceil(args.num_events / float(args.batch_size)))
    sys.stdout.write("Generating {0} events ".format(args.num_events) +
                     "using {0} jobs\n".format(num_jobs))

    if os.path.exists(args.submit_file):
        sys.stderr.write("Submit file at {0} ".format(args.submit_file) +
                         "already exists, exiting!\n")
        return 1

    if os.path.exists(args.dag_file):
        sys.stderr.write("DAG file at {0} ".format(args.dag_file) +
                         "already exists, exiting!\n")
        return 1

    with open(args.dag_file, 'wt') as dag_file:
        for job in range(0, num_jobs):
            dag_file.write("JOB MC.{0} {1}\n".format(job, args.submit_file))
            dag_file.write('VARS MC.{0} flavor="{1}" '.format(job, args.mc_flavor))
            dag_file.write('config="{0}" '.format(args.mc_config))
            dag_file.write('pax_version="{0}" '.format(args.pax_version))
            dag_file.write('mc_version="{0}" '.format(args.mc_version))
            dag_file.write('events="{0}" '.format(args.batch_size))
            dag_file.write('id="{0}" '.format(job))

            dag_file.write("\n")
            dag_file.write("Retry MC.{0} {1}\n".format(job, args.retries))
    with open(args.submit_file, 'wt') as submit_file:
        submit_file.write(SUBMIT_FILE)

    if not os.path.exists('output'):
        os.mkdir('output')
    if not os.path.exists('log'):
        os.mkdir('log')
    sys.stdout.write("Generated DAG file at {0} ".format(args.dag_file) +
                     "and submit file at {0}, run\n".format(args.submit_file) +
                     "\t\t\tcondor_submit_dag {0}\n".format(args.dag_file) +
                     "to submit.\n")
    return 0

if __name__ == '__main__':
    sys.exit(run_main())
