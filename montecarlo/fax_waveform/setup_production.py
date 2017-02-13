import sys
### Edit these three lines ###
head_dirname = '/project/lgrandi/jhowlett/' # all data will go under here (under subdir)
username = 'jh3226' # midway username
interactive = 1 # 1 for terminal prompt options, 0 for hardcoded options below

process_list = []

fields = [
            'process_name', 'process_description', 'log_file', 'nb_jobs',
            'events_per_job', 'pmt_afterpulse', 's2_afterpulse',
            'photon_nb_low', 'photon_nb_high', 'electron_nb_low', 
            'electron_nb_high', 'correlated', 'nodetype'
         ]

process = {}
process['process_name'] = '170213_1347_0'
process['process_description'] = 'testing effect of PMT afterpulse'
process['log_file'] = 'log.log'
process['nb_jobs'] = '100'
process['events_per_job'] = '100'
process['pmt_afterpulse'] = '0'
process['s2_afterpulse'] = '1'
process['photon_nb_low'] = '50'
process['photon_nb_high'] = '50'
process['electron_nb_low'] = '0'
process['electron_nb_high'] = '200'
process['correlated'] = '1'
process['nodetype'] = '2'
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


