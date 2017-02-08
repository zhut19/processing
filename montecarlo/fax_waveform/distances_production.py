import subprocess as subp
import sys, os
import time
import numpy as np

from tempfile import mkstemp
from shutil import move
from os import remove, close


def replace_line_in_file(file_path, config_string_commands):
    #Create temp file
    fh, abs_path = mkstemp()
    pattern = "[WaveformSimulator]truth_file_name=\\\"${FAX_FILENAME}\\\""
    subst = pattern + ";" + config_string_commands
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
    production_commands.append('echo "%s" >> %s' % (process['process_description'], os.path.join(dir_header, 'description.txt')))
    production_commands.append('echo "\n%s" >> %s' % (str(process), os.path.join(dir_header, 'description.txt')))
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
    production_commands.append('mv %s %s' % (os.path.join(merged_dirname, 'Merged.p'), dir_header))
    if rm_leftovers:
        production_commands.append('rm -rf %s' % truth_dirname)
        production_commands.append('rm -rf %s' % basics_dirname)
        production_commands.append('rm -rf %s' % pax_dirname)
        production_commands.append('rm -rf %s' % merged_dirname)
        production_commands.append('rm -rf %s' % processed_dirname)
        production_commands.append('rm -rf %s' % peaks_dirname)
    for command in production_commands:
        while len(subp.check_output(['squeue', '-u', username]).splitlines())>1:
            print('waiting for squeue to free up, time = %i' % int(time.time()))
            time.sleep(60)
        #time.sleep(30)
        print('submitting command')
        subp.call(command, shell=True)
        time.sleep(3)

#import setup_production
process_list = []
nb_iter = 1
rl_iter = np.linspace(1.9, 3.0, nb_iter)
ra_iter = np.linspace(.3, .38, nb_iter)
count = 0 
for i in range(nb_iter):
    for j in range(nb_iter):
        process = {}
        process['nb_jobs'] = '5'
        process['events_per_job'] = '10'
        process['pmt_afterpulse'] = '1'
        process['s2_afterpulse'] = '1'
        process['photon_nb_low'] = '50'
        process['photon_nb_high'] = '50'
        process['electron_nb_low'] = '0'
        process['electron_nb_high'] = '200'
        process['correlated'] = '1' # allows drift-time correlation
        process['nodetype'] = '0' # 0 for xenon1t, 1 for public, 2 for kicp
        # loop-dependent fields
        process['process_name'] = '170208_branch_distances_%i' % count # will be directory name, etc
        process['process_description'] = 'rl = %.3f; ra = %.3f' % (rl_iter[i], ra_iter[j]) # will be catted into text file for records
        process['log_file'] = 'distances_%i.log' % count # will log the production
        process['rl'] = rl_iter[i]
        process['ra'] = ra_iter[j]
        process_list.append(process)
        count = count + 1

process_head_dirname = '/project/lgrandi/jhowlett/'
username = 'jh3226'
# make sure run_fax is original
subp.call('cp backups/run_fax.sh run_fax.sh', shell=True)
for process in process_list:
    ### CHANGE THIS FOR DIFFERENT CONFIG STRING ###
    config_string_commands = "elr_gas_gap_length=%.3f*mm;anode_field_domination_distance=%.3f*mm" % (process['rl'], process['ra'])
    #######
    replace_line_in_file('run_fax.sh', config_string_commands)
    subp.call('chmod +x run_fax.sh', shell=True)
    fax_produce(process, process_head_dirname, username) 
    while len(subp.check_output(['squeue', '-u', username]).splitlines())>1:
        print('waiting for squeue to free up, time = %i' % int(time.time()))
        time.sleep(60)
    subp.call('cp backups/run_fax.sh run_fax.sh', shell=True)
    break
    time.sleep(60)
