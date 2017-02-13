import subprocess as subp
import sys, os
import time
import numpy as np

from tempfile import mkstemp
from shutil import move
from os import remove, close


squeue_dict = {'0': 'xenon1t', '1': 'sandyb', '2': 'kicp'}

def wait_for_squeue(username, nodetype):
    while len(subp.check_output(['squeue', '-u', username, '--partition', squeue_dict[nodetype]]).splitlines())>1:
        print('waiting for squeue to free up, time = %i' % int(time.time()))
        time.sleep(60)

def replace_line_in_file(file_path, config_string_commands):
    #Create temp file
    fh, abs_path = mkstemp()
    pattern = "[WaveformSimulator]truth_file_name=\\\"${FAX_FILENAME}\\\""
    subst = pattern + config_string_commands
    with open(abs_path,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                new_file.write(line.replace(pattern, subst))
    close(fh)
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)

def fax_produce(process, head_dirname, username, rm_leftovers=True):
    print('beginning process %s' % process['process_name'])
    dir_header = os.path.join(head_dirname, process['process_name'])
    truth_dirname = os.path.join(dir_header, 'truth_minitrees_%s' % process['process_name'])
    basics_dirname = os.path.join(dir_header, 'basics_minitrees_%s' % process['process_name'])
    merged_dirname = os.path.join(dir_header, 'merged_minitrees_%s' % process['process_name'])
    processed_dirname = os.path.join(dir_header, 'processed_minitrees_%s' % process['process_name'])
    peaks_dirname = os.path.join(dir_header, 'peak_minitrees_%s' % process['process_name'])
    pax_dirname = os.path.join(dir_header, 'pax_%s' % process['process_name'])
    production_commands = []
    production_commands.append('mkdir %s' % dir_header)
    production_commands.append('echo "%s\n" >> %s' % (process['process_description'], os.path.join(dir_header, 'description.txt')))
    production_commands.append('echo $PWD >> %s' %  os.path.join(dir_header, 'description.txt'))
    production_commands.append('echo "\n%s" >> %s' % (str(process), os.path.join(dir_header, 'description.txt')))
    production_commands.append('cp run_fax.sh %s' % dir_header)
    midway_batch_options = '%s %s %s %s %s %s %s %s %s %s %s' % (dir_header, process['nb_jobs'],
                                process['events_per_job'], process['pmt_afterpulse'], process['s2_afterpulse'],
                                process['photon_nb_low'], process['photon_nb_high'], process['electron_nb_low'],
                                process['electron_nb_high'], process['correlated'], process['nodetype'])
    production_commands.append('python MidwayBatch.py %s >> %s' % (midway_batch_options, process['log_file']))
    if rm_leftovers:
        production_commands.append('./copy_things_around.sh %s kill >> %s' % (process['process_name'], process['log_file']))
    else:
        production_commands.append('./copy_things_around.sh %s >> %s' % (process['process_name'], process['log_file']))
    production_commands.append('python BatchMergeTruthAndProcessed.py Configs/basics_config %s %s %s 0.68 submission_merge/ %s' % (truth_dirname, basics_dirname, merged_dirname, process['nodetype']))
    production_commands.append('python MergePickles.py %s' % merged_dirname)
    production_commands.append('mv %s %s' % (os.path.join(merged_dirname, 'Merged.pkl'), dir_header))
    if rm_leftovers:
        production_commands.append('rm -rf %s' % truth_dirname)
        production_commands.append('rm -rf %s' % basics_dirname)
        production_commands.append('rm -rf %s' % pax_dirname)
        production_commands.append('rm -rf %s' % merged_dirname)
        production_commands.append('rm -rf %s' % processed_dirname)
        production_commands.append('rm -rf %s' % peaks_dirname)
    for command in production_commands:
        wait_for_squeue(username, process['nodetype'])
        print('submitting command')
        subp.call(command, shell=True)
        time.sleep(3)

process_list = []
count = 0 
#########################
### CHANGE THIS STUFF ###
process_head_dirname = '/project/lgrandi/jhowlett/'
username = 'jh3226'
pars_to_change = {}
# Config parameters to change - each should be a list of the same length
# first process will use first element of each list, etc.
pars_to_change['elr_gas_gap_length'] = [2.66, 2.66]
pars_to_change['anode_field_domination_distance'] = [.372, .372]
#pars_to_change['diffusion_constant_liquid'] = [11.4]
units = 'mm' 
nb_iter = 2
process_name_header = '170211_2000_distances'
rm_leftovers = False # Deletes raw data and individual truth/processed minitrees
for i in range(nb_iter):
    process = {}
    process['nb_jobs'] = '100'
    process['events_per_job'] = '200'
    if i==0:
        process['pmt_afterpulse'] = '1'
    else:
        process['pmt_afterpulse'] = '0'
    process['s2_afterpulse'] = '1'
    process['photon_nb_low'] = '50'
    process['photon_nb_high'] = '50'
    process['electron_nb_low'] = '0'
    process['electron_nb_high'] = '200'
    process['correlated'] = '1' # allows drift-time correlation
    process['nodetype'] = '2' # 0 for xenon1t, 1 for public, 2 for kicp
    # loop-dependent fields
    process['process_name'] = process_name_header + '_%i' % count # will be directory name, etc
    description_string = ''
    for field in list(pars_to_change.keys()):
        description_string = description_string + '%s = %.3f;' % (field, pars_to_change[field][i])
        process[field] = pars_to_change[field][i]
    process['process_description'] = description_string # will be catted into text file for records
    process['log_file'] = 'logs/process_%i.log' % count # will log the production
    process_list.append(process)
    count = count + 1
##############################
##############################

# make sure run_fax is original
subp.call('cp backups/run_fax.sh run_fax.sh', shell=True)
for (i, process) in enumerate(process_list):
    config_string_commands = ""
    for par in list(pars_to_change.keys()):
        config_string_commands = config_string_commands + ";%s=%.3f*%s" % (par, pars_to_change[par][i], units)
    replace_line_in_file('run_fax.sh', config_string_commands)
    subp.call('chmod +x run_fax.sh', shell=True)
    process['log_file'] = os.path.join('logs', process['log_file'])
    fax_produce(process, process_head_dirname, username, rm_leftovers=rm_leftovers) 
    wait_for_squeue(username, process['nodetype'])
    subp.call('cp backups/run_fax.sh run_fax.sh', shell=True)
    time.sleep(60)
