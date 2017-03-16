import subprocess as subp
import sys, os
import time

squeue_dict = {'0': 'xenon1t', '1': 'sandyb', '2': 'kicp'}
configs = {'0': 'basics_config', '1' : 's1s2_preserve_all', '2' : 'PeakEfficiency'}

def wait_for_squeue(username, nodetype):
    while len(subp.check_output(['squeue', '-u', username, '--partition', squeue_dict[nodetype]]).splitlines())>1:
        print('waiting for squeue to free up, time = %i' % int(time.time()))
        time.sleep(60)

def make_processed_list(head_dirname, datetime, batchlist = 'processed_dataset_list.dat'):
    dir_header = os.path.join(head_dirname, datetime)
    pax_dir = os.path.join(dir_header, 'pax_%s/' % datetime)
    print(pax_dir)
    reduced_dir = os.path.join(dir_header, 'reduced_minitrees_%s/' % datetime)
    batchlist_file = open(batchlist, 'w')
    for subdir, dirs, files in os.walk(pax_dir):
        for filename in files:
            if '_pax.root' in filename:
                batchlist_file.write(filename.split('.')[0] + '\n')
    batchlist_file.close()

def fax_produce(process, head_dirname, username):
    dir_header = os.path.join(head_dirname, process['process_name'])
    truth_dirname = os.path.join(dir_header, 'truth_minitrees_%s' % process['process_name'])
    basics_dirname = os.path.join(dir_header, 'basics_minitrees_%s' % process['process_name'])
    merged_dirname = os.path.join(dir_header, 'merged_minitrees_%s' % process['process_name'])
    reduced_dirname = os.path.join(dir_header, 'reduced_minitrees_%s' % process['process_name'])
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
    production_commands.append('./sort_processed_files.sh %s >> %s' % (process['process_name'], process['log_file']))
    if process['minitree_type'] != '0':
        batchlist = 'processed_dataset_list.dat'
        production_commands.append('python BatchReduceDataSubmission.py %s %s %s %s %s 0 %s >> %s' % (batchlist, pax_dirname,
                                        reduced_dirname, os.path.join(os.getcwd(), 'submission_reduce/'), process['nodetype'], process['minitree_type'], process['log_file']))
        production_commands.append('python BatchMergeTruthAndProcessed.py Configs/%s %s %s %s submission_merge/ %s 0 %s %s' % (configs[process['minitree_type']], 
                                            truth_dirname, reduced_dirname, merged_dirname, process['nodetype'], process['use_array_truth'], process['minitree_type']))
    else:
        production_commands.append('python BatchMergeTruthAndProcessed.py Configs/%s %s %s %s submission_merge/ %s 0 %s %s' % (configs[process['minitree_type']], 
                                            truth_dirname, basics_dirname, merged_dirname, process['nodetype'], process['use_array_truth'], process['minitree_type']))
    production_commands.append('python MergePickles.py %s' % (merged_dirname))
    for command in production_commands:
        wait_for_squeue(username, process['nodetype'])
        if process['minitree_type']!='0':
            if 'BatchReduce' in command:
                time.sleep(10)
                make_processed_list(head_dirname, process['process_name'], batchlist=batchlist)
        print('submitting command')
        print(command)
        subp.call(command, shell=True)

import setup_production
process_list = setup_production.process_list
for process in process_list:
    process['log_file'] = os.path.join('logs', process['log_file'])
    fax_produce(process, setup_production.head_dirname, setup_production.username)
