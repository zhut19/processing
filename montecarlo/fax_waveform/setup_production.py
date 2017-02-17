import sys
### Edit these three lines ###
head_dirname = '/project/lgrandi/jhowlett/' # all data will go under here (under subdir)
username = 'jh3226' # midway username
interactive = 0 # 1 for terminal prompt options, 0 for hardcoded options below

process_list = []

fields = [
            'process_name', 'process_description', 'log_file', 'nb_jobs',
            'events_per_job', 'pmt_afterpulse', 's2_afterpulse',
            'photon_nb_low', 'photon_nb_high', 'electron_nb_low', 
            'electron_nb_high', 'correlated', 'nodetype', 'make_peak_trees'
         ]
'''
process = {}
process['process_name'] = '170214_2206_0'
process['process_description'] = 'checking data matching'
process['log_file'] = 'log.log'
process['nb_jobs'] = '100'
process['events_per_job'] = '1000'
process['pmt_afterpulse'] = '1'
process['s2_afterpulse'] = '1'
process['photon_nb_low'] = '0'
process['photon_nb_high'] = '1000'
process['electron_nb_low'] = '0'
process['electron_nb_high'] = '100'
process['correlated'] = '1'
process['nodetype'] = '0'
if interactive == 0:
    process_list.append(process)

process = {}
process['process_name'] = '170214_2206_1'
process['process_description'] = 'checking data matching pmt off'
process['log_file'] = 'log.log'
process['nb_jobs'] = '100'
process['events_per_job'] = '1000'
process['pmt_afterpulse'] = '0'
process['s2_afterpulse'] = '1'
process['photon_nb_low'] = '0'
process['photon_nb_high'] = '1000'
process['electron_nb_low'] = '0'
process['electron_nb_high'] = '100'
process['correlated'] = '1'
process['nodetype'] = '0'
if interactive == 0:
    process_list.append(process)

process = {}
process['process_name'] = '170215_1830_s1'
process['process_description'] = 's1 only for efficiency'
process['log_file'] = 'log.log'
process['nb_jobs'] = '100'
process['events_per_job'] = '1000'
process['pmt_afterpulse'] = '1'
process['s2_afterpulse'] = '1'
process['photon_nb_low'] = '0'
process['photon_nb_high'] = '2000'
process['electron_nb_low'] = '0'
process['electron_nb_high'] = '0'
process['correlated'] = '1'
process['nodetype'] = '0'
process['make_peak_trees'] = '1'
if interactive == 0:
    process_list.append(process)

process = {}
process['process_name'] = '170215_1830_s2'
process['process_description'] = 's2 only for efficiency'
process['log_file'] = 'log.log'
process['nb_jobs'] = '100'
process['events_per_job'] = '1000'
process['pmt_afterpulse'] = '1'
process['s2_afterpulse'] = '1'
process['photon_nb_low'] = '0'
process['photon_nb_high'] = '0'
process['electron_nb_low'] = '0'
process['electron_nb_high'] = '200'
process['correlated'] = '1'
process['nodetype'] = '0'
process['make_peak_trees'] = '1'
if interactive == 0:
    process_list.append(process)
'''

process = {}
process['process_name'] = '170217_1241_testing_peak'
process['process_description'] = 's2 only for efficiency'
process['log_file'] = 'log.log'
process['nb_jobs'] = '5'
process['events_per_job'] = '5'
process['pmt_afterpulse'] = '1'
process['s2_afterpulse'] = '1'
process['photon_nb_low'] = '0'
process['photon_nb_high'] = '1000'
process['electron_nb_low'] = '0'
process['electron_nb_high'] = '50'
process['correlated'] = '1'
process['nodetype'] = '0'
process['make_peak_trees'] = '1'
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


