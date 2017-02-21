import sys
### Edit these three lines ###
with open('sort_processed_files.sh') as bashfile:
    lines = bashfile.readlines()
head_dirname = lines[1].split('=')[1].split()[0] # all data will go under here (under subdir)
username = lines[2].split('=')[1].split()[0] # midway username
interactive = 0 # 1 for terminal prompt options, 0 for hardcoded options below

process_list = []

fields = [
            'process_name', 'process_description', 'log_file', 'nb_jobs',
            'events_per_job', 'pmt_afterpulse', 's2_afterpulse',
            'photon_nb_low', 'photon_nb_high', 'electron_nb_low', 
            'electron_nb_high', 'correlated', 'nodetype', 'minitree_type',
            'use_array_truth'
         ]

process = {}
process['process_name'] = '170221_1339_test'
process['process_description'] = 'making standard s1/s2 basics data for matching pax_v6.4.2'
process['log_file'] = '170221_test.log'
process['nb_jobs'] = '5'
process['events_per_job'] = '2'
process['pmt_afterpulse'] = '1'
process['s2_afterpulse'] = '1'
process['photon_nb_low'] = '0'
process['photon_nb_high'] = '1000'
process['electron_nb_low'] = '0'
process['electron_nb_high'] = '100'
process['correlated'] = '1'
process['nodetype'] = '0'
process['minitree_type'] = '2'
process['use_array_truth'] = '0'
if interactive == 0:
    process_list.append(process)

def setup_process(fields, process_nb):
    process = {}
    for field in fields:
        process[field] = input('set %s for process %i >\t' % (field, process_nb))
    return process

if interactive:
    nb_processes = int(input('How many processes? >\t'))

    for i in range(1, nb_processes+1):
        process_list.append(setup_process(fields, i))

    print('\nConfirm Process List:')
    for (i, process) in enumerate(process_list):
        print('\nProcess %i:' % (i+1))
        for field in fields:
            print('%s:\t%s' % (field, process[field]))
        confirmation = input('\nConfirm (y/n) > ')
        if confirmation=='n':
            print('Edit Process %i:' % (i+1))
            process_list[i] = setup_process(fields, i+1)


