#!/usr/bin/env python

import argparse
import getpass
import json
import math
import os
import re
import subprocess
import sys

import Pegasus.DAX3
import cStringIO

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
    'optPhot',
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

# pegasus constants
PEGASUSRC_PATH = './pegasusrc'


def update_site_catalogs(site):
    """
    Update the pegasus site catalog to set the local scratch and output
    directories to subdirectories

    :param site: condorpool for osg sites, egi for egi sites
    :return: None
    """

    scratch_re = re.compile('type="shared-scratch" path="(.*?)"')
    output_re = re.compile('type="local-storage" path="(.*?)"')
    url_re = re.compile('operation="all" url="file://(.*?)"')
    if site == 'condorpool':
        catalog_file = 'osg-sites.xml'
    elif site == 'egi':
        catalog_file = 'egi-sites.xml'
    buf = ""
    catalog = open(catalog_file, 'r')
    while True:
        line = catalog.readline()
        if not line:
            break
        match = scratch_re.search(line)
        if match:
            new_path = os.path.join(os.getcwd(), 'scratch')
            buf += scratch_re.sub('type="shared-scratch" path="{0}"'.format(new_path),
                                  line)
            line = catalog.readline()
            buf += url_re.sub('operation="all" url="file://{0}"'.format(new_path),
                              line)
            continue
        match = output_re.search(line)
        if match:
            new_path = os.path.join(os.getcwd(), 'output')
            buf += output_re.sub('type="local-storage" path="{0}"'.format(new_path),
                                 line)
            line = catalog.readline()
            buf += url_re.sub('operation="all" url="file://{0}"'.format(new_path),
                              line)
            continue
        buf += line
    catalog.close()
    open(catalog_file, 'w').write(buf)


def check_macro(macro_name, mc_version):
    """
    Check to see if given macro is present in OASIS

    :param macro_name: name of macro file
    :param mc_version: version of mc code to use
    :return: True if macro is available in OASIS for specified mc version
    """
    macro_location = os.path.join(MC_PATH, mc_version, 'macros', macro_name)
    if os.path.isfile(macro_location):
        return True

    return False


def pegasus_submit(dax, site, output_directory):
    """
    Submit a workflow to pegasus

    :param dax:  path to xml file with DAX, used for submit
    :param site: condorpool for osg, egi for EGI submission
    :param output_directory:  directory for workflow output
    :return: the pegasus workflow id
    """
    try:
        if site == 'condorpool':
            pegasus_rc = './osg-pegasusrc'
        elif site == 'egi':
            pegasus_rc = './egi-pegasusrc'
        else:
            sys.stderr.write("Invalid grid type: {0}\n".format(site))
            sys.exit(1)
        update_site_catalogs(site)
        output = subprocess.check_output(['/usr/bin/pegasus-plan',
                                          '--sites',
                                          site,
                                          '--conf',
                                          pegasus_rc,
                                          '--output-dir',
                                          output_directory,
                                          '--dax',
                                          dax,
                                          '--submit'],
                                         stderr=subprocess.STDOUT)
        match = re.search('running in the base directory:.*?(\d{8}T\d{6}-\d{4})',
                          output,
                          re.MULTILINE|re.DOTALL)
        if match:
            return match.group(1)
    except subprocess.CalledProcessError as err:
        sys.stderr.write("Error with workflow: {0}\n".format(err.output))
        return None
    return None


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

# needs to be set after functions defined
MC_VERSIONS = get_mc_versions()
PAX_VERSIONS = get_pax_versions()


def generate_mc_workflow(mc_config,
                         mc_flavor,
                         mc_version,
                         fax_version,
                         pax_version,
                         start_job,
                         num_events,
                         batch_size,
                         preinit_macro,
                         optical_setup,
                         source_macro):
    """
    Generate a Pegasus workflow to do X1T MC processing

    :param mc_config: MC config to use
    :param mc_flavor: MC flavor to use
    :param mc_version: version of MC code to use
    :param fax_version: version of FAX code to use
    :param pax_version: version of PAX code to use
    :param start_job: starting job id number
    :param num_events: total number of events to generate
    :param batch_size: number of events to generate per job
    :param preinit_macro: macro to use to preinitialize MC
    :param optical_setup: macro to setup optics
    :param source_macro: macro to use for MC generation
    :return: number of jobs in the workflow
    """
    dax = Pegasus.DAX3.ADAG('montecarlo')
    run_sim = Pegasus.DAX3.Executable(name="run_sim.sh", arch="x86_64", installed=False)
    run_sim.addPFN(Pegasus.DAX3.PFN("file://{0}".format(os.path.join(os.getcwd(), "run_sim.sh")), "local"))
    dax.addExecutable(run_sim)

    num_jobs = get_num_jobs(num_events, batch_size)
    sys.stdout.write("Generating {0} events ".format(num_events) +
                     "using {0} jobs\n".format(num_jobs))

    if fax_version is None:
        fax_version = pax_version

    if preinit_macro is None:
        if "Cs137" in mc_config:
            preinit_macro = 'preinit_{0}.mac'.format(mc_config)
        elif "muon" in mc_config or "MV" in mc_config:
            preinit_macro = 'preinit_MV.mac'
        else:
            preinit_macro = 'preinit.mac'
    if optical_setup is None:
        optical_setup = 'setup_optical_S1.mac'
    if source_macro is None:
        source_macro = "run_{0}.mac".format(mc_config)

    source_macro_input = None
    if not check_macro(source_macro, mc_version):
        if not os.path.exists(source_macro):
            sys.stderr.write("Source macro not in OASIS or current "
                             "directory, exiting.\n")
            sys.exit(1)
        source_macro_input = Pegasus.DAX3.File(source_macro)
        macro_path = os.path.join(os.getcwd(), source_macro)
        file_pfn = Pegasus.DAX3.PFN("file://{0}".format(macro_path),
                                    "local")
        source_macro_input.addPFN(file_pfn)
        dax.addFile(source_macro_input)

    optical_macro_input = None
    if not check_macro(optical_setup, mc_version):
        if not os.path.exists(optical_setup):
            sys.stderr.write("Optical setup macro not in OASIS or current "
                             "directory, exiting.\n")
            sys.exit(1)
        optical_macro_input = Pegasus.DAX3.File(optical_setup)
        macro_path = os.path.join(os.getcwd(), optical_setup)
        file_pfn = Pegasus.DAX3.PFN("file://{0}".format(macro_path),
                                    "local")
        optical_macro_input.addPFN(file_pfn)
        dax.addFile(optical_macro_input)

    preinit_macro_input = None
    if not check_macro(preinit_macro, mc_version):
        if not os.path.exists(preinit_macro):
            sys.stderr.write("Preinit macro not in OASIS or current "
                             "directory, exiting.\n")
            sys.exit(1)
        preinit_macro_input = Pegasus.DAX3.File(preinit_macro)
        macro_path = os.path.join(os.getcwd(), preinit_macro)
        file_pfn = Pegasus.DAX3.PFN("file://{0}".format(macro_path),
                                    "local")
        preinit_macro_input.addPFN(file_pfn)
        dax.addFile(preinit_macro_input)

    try:
        for job in range(start_job, start_job+num_jobs):
            run_sim_job = Pegasus.DAX3.Job(id="{0}".format(job), name="run_sim.sh")
            if job == (num_jobs - 1):
                left_events = num_events % batch_size
                if left_events == 0:
                    left_events = batch_size
                run_sim_job.addArguments(str(job),
                                         mc_flavor,
                                         mc_config,
                                         str(left_events),
                                         mc_version,
                                         fax_version,
                                         pax_version,
                                         '0',  # don't save raw data
                                         preinit_macro,
                                         optical_setup,
                                         source_macro)
            else:
                run_sim_job.addArguments(str(job),
                                         mc_flavor,
                                         mc_config,
                                         str(batch_size),
                                         mc_version,
                                         fax_version,
                                         pax_version,
                                         '0',  # don't save raw data
                                         preinit_macro,
                                         optical_setup,
                                         source_macro)
            if preinit_macro_input:
                run_sim_job.uses(preinit_macro_input, link=Pegasus.DAX3.Link.INPUT)
            if optical_macro_input:
                run_sim_job.uses(optical_macro_input, link=Pegasus.DAX3.Link.INPUT)
            if source_macro_input:
                run_sim_job.uses(source_macro_input, link=Pegasus.DAX3.Link.INPUT)
            output = Pegasus.DAX3.File("{0}_output.tar.bz2".format(job))
            run_sim_job.uses(output, link=Pegasus.DAX3.Link.OUTPUT, transfer=True)
            dax.addJob(run_sim_job)
        with open('mc_process.xml', 'w') as f:
            dax.writeXML(f)
    except:
        return 0
    return num_jobs


def get_num_jobs(total_events, batch_size):
    """
    Get the number of jobs to use for MC simulation

    :param total_events: total number of events to generate
    :param batch_size:  number of events to generate per job
    :return: number of jobs to use
    """
    num_jobs = int(math.ceil(total_events / float(batch_size)))
    return num_jobs


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
    parser.add_argument('--start_job', dest='start_job',
                        action='store', default=0, type=int,
                        help='starting number for job')
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
    parser.add_argument('--fax-version', dest='fax_version',
                        choices=PAX_VERSIONS,
                        action='store', default=None,
                        help='version of fax to use')
    parser.add_argument('--pax-version', dest='pax_version',
                        choices=PAX_VERSIONS,
                        action='store', required=True,
                        help='version of pax to use')
    parser.add_argument('--grid-type', dest='grid_type',
                        choices=['osg', 'egi'],
                        action='store', required=True,
                        help='Grid to submit to')
    parser.add_argument('--preinit-macro', dest='preinit_macro',
                        action='store', default=None,
                        help='preinit macro to use')
    parser.add_argument('--optical-setup', dest='optical_setup',
                        action='store', default=None,
                        help='macro to use to setup optical properties')
    parser.add_argument('--source-macro', dest='source_macro',
                        action='store', default=None,
                        help='macro to use for MC')

    args = parser.parse_args(sys.argv[1:])
    if args.num_events == 0:
        sys.stdout.write("No events to generate, exiting")
        return 0

    output_directory = os.path.join(os.getcwd(), 'output')
    workflow_info = [0,
                     args.num_events,
                     args.mc_flavor,
                     args.mc_config,
                     args.batch_size,
                     args.mc_version,
                     args.fax_version,
                     args.pax_version,
                     args.preinit_macro,
                     args.optical_setup,
                     args.source_macro]

    workflow_info[0] = generate_mc_workflow(args.mc_config,
                                            args.mc_flavor,
                                            args.mc_version,
                                            args.fax_version,
                                            args.pax_version,
                                            args.start_job,
                                            args.num_events,
                                            args.batch_size,
                                            args.preinit_macro,
                                            args.optical_setup,
                                            args.source_macro)
    if workflow_info[0] == 0:
        sys.stderr.write("Can't generate workflow, exiting\n")
        try:
            os.unlink('mc_process.xml')
        except OSError:
            sys.stderr.write("Can't remove mc_process.xml\n")
        return 1
    pegasus_id = None
    if args.grid_type == 'osg':
        pegasus_id = pegasus_submit('mc_process.xml',
                                    'condorpool',
                                    output_directory)
        workflow_info.append(pegasus_id)
    elif args.grid_type == 'egi':
        pegasus_id = pegasus_submit('mc_process.xml',
                                    'egi',
                                    output_directory)
    if pegasus_id:
        workflow_dir = os.path.join(os.getcwd(),
                                    getpass.getuser(),
                                    "pegasus",
                                    "montecarlo",
                                    pegasus_id)
        sys.stdout.write("MC workflow started:\n")
        sys.stdout.write("Run 'pegasus-status -l " +
                         "{0}' to monitor\n".format(workflow_dir))
        sys.stdout.write("Run 'pegasus-remove " +
                         "{0}' to stop\n".format(workflow_dir))
    try:
        os.unlink('mc_process.xml')
    except OSError:
        sys.stderr.write("Can't remove mc_process.xml\n")
    if pegasus_id is None:
        sys.stderr.write("Couldn't start pegasus workflow")
        return 1
    workflow_info.append(pegasus_id)
    with open('mc_workflow.json', 'w') as f:
        f.write(json.dumps(workflow_info))
    return 0

if __name__ == '__main__':
    # workaround missing subprocess.check_output
    if "check_output" not in dir(subprocess):  # duck punch it in!
        def check_output(*popenargs, **kwargs):
            """
            Run command with arguments and return its output as a byte string.

            Backported from Python 2.7 as it's implemented as pure python
            on stdlib.

            """
            process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
            output, unused_err = process.communicate()
            retcode = process.poll()
            if retcode:
                cmd = kwargs.get("args")
                if cmd is None:
                    cmd = popenargs[0]
                error = subprocess.CalledProcessError(retcode, cmd)
                error.output = output
                raise error
            return output
        subprocess.check_output = check_output

    sys.exit(run_main())
