import subprocess as subp
import sys, os
import time

def fax_produce(process, head_dirname, username):
    print('beginning process %s' % process['process_name'])
    dir_header = os.path.join(head_dirname, process['process_name'])
    truth_dirname = os.path.join(dir_header, 'truth_minitrees_%s' % process['process_name'])
    basics_dirname = os.path.join(dir_header, 'basics_minitrees_%s' % process['process_name'])
    merged_dirname = os.path.join(dir_header, 'merged_minitrees_%s' % process['process_name'])
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
    production_commands.append('./copy_things_around.sh %s >> %s' % (process['process_name'], process['log_file']))
    production_commands.append('python BatchMergeTruthAndProcessed.py Configs/branch_list_config %s %s %s 0.68 submission_merge/ %s' % (truth_dirname, basics_dirname, merged_dirname, process['nodetype']))
    production_commands.append('python MergePickles.py %s' % (merged_dirname))
    for command in production_commands:
        while len(subp.check_output(['squeue', '-u', username]).splitlines())>1:
            print('waiting for squeue to free up, time = %i' % int(time.time()))
            time.sleep(60)
        #time.sleep(30)
        print('submitting command')
        subp.call(command, shell=True)

import setup_production
process_list = setup_production.process_list
for process in process_list:
    fax_produce(process, setup_production.head_dirname, setup_production.username)

