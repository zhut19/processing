#!/usr/bin/env python

import argparse
import getpass
import json
import math
import os
import re
import subprocess
import sys
import glob

import Pegasus.DAX3
import time

MC_PATH = '/cvmfs/xenon.opensciencegrid.org/releases/mc/'
PAX_PATH = "/cvmfs/xenon.opensciencegrid.org/releases/anaconda/2.4/envs/"
MC_FLAVORS = ('G4', 'NEST', 'G4p10')

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


def macro_in_cvmfs(macro_name, mc_version):
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
                          re.MULTILINE | re.DOTALL)
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

    :return: tuple with string of pax versions available
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


def get_configs():
    """
    Return a tuple with G4 macros that are available
    Warning: reads from latest MC version in /cvmfs

    :return: tuple with string of G4 macros available in latest MC version
    """
    try:
        configs = []
        if os.path.isdir(MC_PATH):
            versions = glob.glob(MC_PATH + '/*')
            latest_dir = max(versions, key=os.path.getctime)

        macros_path = latest_dir + '/macros'

        if os.path.isdir(macros_path):
            configs = glob.glob(macros_path + '/run_*.mac')
            configs = [config.split('run_', 1)[1] for config in configs]
            configs = [config.split('.mac', 1)[0] for config in configs]
            configs.sort()

        print ('Reading G4 macros from ', latest_dir)

        return tuple(configs)

    except OSError:
        sys.stderr.write("Can't get configs from {0}\n".format(MC_PATH))
        return ()


def check_and_add_macro_pfn(macro_filename, mc_version, dax):
    """
    Check to make sure that a macro file is present and
    if that's the case, add the macro as a input file to 
    a given pegasus dax
    
    :param macro_filename: name of macro file (NOT a path)
    :param mc_version: version of MC code the workflow is running
    :param dax: pegasus dax object
    :return: tuple of (bool for success (True for success), pegasus file object)
    """

    if macro_in_cvmfs(macro_filename, mc_version):
        return True, None

    if not os.path.exists(macro_filename):
        return False, None

    # Macro not in OASIS but in present directory
    # add macro as a PFN input file to dax workflow
    macro_input = Pegasus.DAX3.File(macro_filename)
    macro_path = os.path.join(os.getcwd(), macro_filename)
    file_pfn = Pegasus.DAX3.PFN("file://{0}".format(macro_path),
                                "local")
    macro_input.addPFN(file_pfn)
    dax.addFile(macro_input)
    return True, macro_input


# needs to be set after functions defined
MC_VERSIONS = get_mc_versions()
PAX_VERSIONS = get_pax_versions()
CONFIGS = get_configs()


def generate_mc_workflow(mc_config,
                         mc_flavor,
                         mc_version,
                         fax_version,
                         pax_version,
                         start_job,
                         num_events,
                         batch_size,
                         macro_sources):
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
    :param macro_sources: dictionary with information about macros to use
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

    if macro_sources['preinit_macro']['name'] is None:
        if "muon" in mc_config or "MV" in mc_config:
            macro_sources['preinit_macro']['name'] = 'preinit_MV.mac'
        else:
            macro_sources['preinit_macro']['name'] = 'preinit_TPC.mac'

    if macro_sources['belt_macro']['name'] is None:
        belt_pos = "none"
        for belt_type in ["ib", "ub", "NGpos"]:
            if "_" + belt_type in mc_config:
                belt_pos = mc_config[mc_config.index(belt_type):]
        macro_sources['belt_macro']['name'] = "preinit_B_{0}.mac".format(belt_pos)

    if macro_sources['efield_macro']['name'] is None:
        macro_sources['efield_macro']['name'] = "preinit_EF_C15kVA4kV.mac"

    if macro_sources['optical_macro']['name'] is None:
        macro_sources['optical_macro']['name'] = 'setup_optical.mac'

    if macro_sources['source_macro']['name'] is None:
        macro_sources['source_macro']['name'] = "run_{0}.mac".format(mc_config)

    for macro in macro_sources.keys():
        success, macro_file = check_and_add_macro_pfn(macro['name'],
                                                      mc_version,
                                                      dax)
        if not success:
            sys.stderr.write("{0} {1} not in OASIS ".format(macro,
                                                            macro['name']) +
                             "or current directory, exiting.\n")
            sys.exit(1)
        macro['pegasus_file'] = macro_file

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
                                         macro_sources['preinit_macro']['name'],
                                         macro_sources['belt_macro']['name'],
                                         macro_sources['efield_macro']['name'],
                                         macro_sources['optical_macro']['name'],
                                         macro_sources['source_macro']['name'])
            else:
                run_sim_job.addArguments(str(job),
                                         mc_flavor,
                                         mc_config,
                                         str(batch_size),
                                         mc_version,
                                         fax_version,
                                         pax_version,
                                         '0',  # don't save raw data
                                         macro_sources['preinit_macro']['name'],
                                         macro_sources['belt_macro']['name'],
                                         macro_sources['efield_macro']['name'],
                                         macro_sources['optical_macro']['name'],
                                         macro_sources['source_macro']['name'])
            if macro_sources['preinit_macro']['pegasus_file']:
                run_sim_job.uses(macro_sources['preinit_macro']['pegasus_file'],
                                 link=Pegasus.DAX3.Link.INPUT)
            if macro_sources['belt_macro']['pegasus_file']:
                run_sim_job.uses(macro_sources['belt_macro']['pegasus_file'],
                                 link=Pegasus.DAX3.Link.INPUT)
            if macro_sources['efield_macro']['pegasus_file']:
                run_sim_job.uses(macro_sources['efield_macro']['pegasus_file'],
                                 link=Pegasus.DAX3.Link.INPUT)
            if macro_sources['optical_macro']['pegasus_file']:
                run_sim_job.uses(macro_sources['optical_macro']['pegasus_file'],
                                 link=Pegasus.DAX3.Link.INPUT)
            if macro_sources['source_macro']['pegasus_file']:
                run_sim_job.uses(macro_sources['source_macro']['pegasus_file'],
                                 link=Pegasus.DAX3.Link.INPUT)
            run_sim_job.addProfile(Pegasus.DAX3.Profile(Pegasus.DAX3.Namespace.CONDOR, "request_disk", "1G"))
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


def save_workflow_info(filename=None, workflow_info=None):
    """
    Save workflow information to a json file
    
    :param filename: string with file to write to 
    :param workflow_info: tuple or list with workflow info
    :return: True on success, False otherwise
    """

    if filename is None or workflow_info is None:
        return True
    if os.path.isfile(filename):
        workflow = json.loads(open(filename, 'r'))
        if type(workflow) != dict:
            workflow = {}
    else:
        workflow = {}
    times_string = time.strftime("%Y%M%d-%H%M%S", time.localtime())
    workflow[times_string] = workflow_info

    with open('mc_workflow.json', 'w') as f:
        f.write(json.dumps(workflow))


def run_main():
    """
    Main function to process user input and then generate the appropriate 
    submit files

    :return: exit code -- 0 on success, 1 otherwise
    """

    parser = argparse.ArgumentParser(description="Create a set of files for "
                                                 "doing MC simulation for X1T",
                                     fromfile_prefix_chars='@')

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
    parser.add_argument('--macro', dest='macro_list',
                        action='store', default=None,
                        help='macro specification given as macro,filename ')

    args = parser.parse_args(sys.argv[1:])
    if args.num_events == 0:
        sys.stdout.write("No events to generate, exiting")
        return 0

    macro_sources = {'preinit_macro': {'name': None,
                                       'pegasus_file': None},
                     'belt_macro': {'name': None,
                                    'pegasus_file': None},
                     'efield_macro': {'name': None,
                                      'pegasus_file': None},
                     'optical_macro': {'name': None,
                                       'pegasus_file': None},
                     'source_macro': {'name': None,
                                      'pegasus_file': None}, }
    for entry in args.macro_list:
        macro_fields = entry.split(',')
        if len(macro_fields) != 2:
            sys.stderr.write("Macro {0} defined incorrectly\n")
            sys.stderr.write("Macro must be specified as "+
                             "{0},filename\n".format(macro_fields[0]))
            sys.exit(1)
        macro_name, macro_file = entry.split(',')
        if macro_name not in macro_sources:
            sys.stderr.write("Unknown macro {0} defined!\n")
            sys.exit(1)

    output_directory = os.path.join(os.getcwd(), 'output')
    workflow_info = [0,
                     args.num_events,
                     args.mc_flavor,
                     args.mc_config,
                     args.batch_size,
                     args.mc_version,
                     args.fax_version,
                     args.pax_version,
                     macro_sources,
                     args.preinit_macro,
                     args.preinit_belt,
                     args.preinit_efield,
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
                                            macro_sources)
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
    save_workflow_info('mc_workflow.json', workflow_info)
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
