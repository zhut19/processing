#######################################
# Fax Production Processes
# by Tianyu tz2263@columbia.edu, Aug 2017
# Changed from Qing and Joey's code
# 
# All processes required for fax production
# CreateFake
# CreateFakeFromPickle
# Simulation
# ProcessRaw
# SortTruth
# BuildMiniTree
# MergeTruth
# BuildMiniTreeArray (not implemented)
# MergeTruthArray (not implemented)
#######################################
# Hard Code Warnings
#
# RunAllProcess.process_list
# PaxerProcess timeout
# BuildMiniTree hax.minitrees.load(..,[Correction])
#######################################
# Run as __main__ with
# python fax_production_process {head_directory} {production_list_file}
# python fax_production_process {head_directory} {production_id}
#
# will initiate and run RunAllProcess() and RunAllProcess.process()
########################################

import sys, os
from configparser import ConfigParser
from contextlib import contextmanager
import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None
from subprocess import Popen, PIPE, STDOUT, TimeoutExpired

import hax

#sys.path.append('/home/zhut/sim/fax_waveform/treemakers')
#from corrections import Corrections

class ProductionProcess():
    '''Generic production process class'''

    process_order = 0
    __version__ = '0.0.0'

    def process(self, head_directory, production_id):
        self.read_config(head_directory, production_id)
        self._process()

    def _process(self):
        raise NotImplementedError()

    def read_config(self, head_directory, production_id):
    # Read the parameters used for production
        if head_directory == '' or production_id == '':
            print ('Must specify head_directory and production_id')
            return 0

        self.production_id = production_id
        self.config_name = production_id[:-7]
        self.head_directory = head_directory

        self.config_path = os.path.join(self.head_directory, self.config_name, '%s.ini' % self.config_name)
        self.config = ConfigParser()
        self.config.read(self.config_path)

    @contextmanager
    def _divert_stdout(self):
        # Dangerous to use but works very nice if all bugs are fixed.
        # Basically works as 1&>${log}
        self.productionlog_path = self.config['DIRECTORY']['productionlog']
        self.productionlog = open('{path}/{name}.log'.format(path = self.productionlog_path, name = self.production_id), 'a+')

        global saved_stdout, saved_stderr
        saved_stdout, saved_stderr = sys.stdout, sys.stderr
        sys.stdout = self.productionlog
        sys.stderr = self.productionlog
        print(saved_stdout)
        print(saved_stderr)
        yield
        sys.stdout = saved_stdout
        sys.stderr = saved_stderr
        self.productionlog.close()


class RunAllProcess(ProductionProcess):
    '''Go through all processes'''

    __version__ = '0.0.1'

    def __init__(self):
        self.process_list = [CreateFake(),
                             Simulation(),
                             ProcessRaw(),
                             SortTruth(),
                             BuildMiniTree(),
                             MergeTruth(),
                            ]

    def process(self, head_directory, production_id):
        for process in self.process_list:
            process.process(head_directory, production_id)


class CreateFake(ProductionProcess):
    '''Create fake data and write to {production_id}.csv at {csv} directory'''

    process_order = 1
    __version__ = '0.0.1'

    def __init__(self):
        ####################################
        ## Some nuisance parameters (HARDCODE WARNING):
        ####################################
        self.DriftVelocity = 1.440e-1 # cm/us
        self.default_event_time = 1000. # Where we put S1

    def _process(self):
        self.csv_path = self.config['DIRECTORY']['csv'] # Where the csv will be save to
        self.detector = self.config['BASICS']['detector']
        self.number_event_per_job = int(self.config['BASICS']['number_event_per_job'])
        self.photon_number_low = int(self.config['BASICS']['photon_number_low'])
        self.photon_number_high = int(self.config['BASICS']['photon_number_high'])
        self.electron_number_low = int(self.config['BASICS']['electron_number_low'])
        self.electron_number_high = int(self.config['BASICS']['electron_number_high'])
        self.recoil_type = self.config['BASICS']['recoil_type']

        S1, S2 = 'S1', 'S2' # Allow eval to work
        self.correlated = eval(self.config['BASICS']['correlated'])

        # Actual creation
        self._randomize_FV()
        self._randomize_photon_number()
        self._randomize_electron_number()

        self.csv = pd.DataFrame(columns = ['instruction', 'recoil_type', 'x', 'y', 'z', 
                                           's1_photons', 's2_electrons', 't'])

        if self.correlated == False:
            self.csv['instruction'] = np.asarray([(n+((-1)**n-1)/2)/2 for n in range(2*self.number_event_per_job)],dtype = int)
            self.csv['recoil_type'] = self.recoil_type
            self.csv['temp'] = [n%2+1 for n in range(2*self.number_event_per_job)]

            self.csv.loc[self.csv.temp == 1,'t'] = self.default_event_time
            self.csv.loc[self.csv.temp == 1,'s1_photons'] = self.photon_number
            self.csv.loc[self.csv.temp == 1,'s2_electrons'] = 0

            self.csv.loc[self.csv.temp == 2,'t'] = self.default_event_time+self.z/self.DriftVelocity
            self.csv.loc[self.csv.temp == 2,'s1_photons'] = 0
            self.csv.loc[self.csv.temp == 2,'s2_electrons'] = self.electron_number

            for field in ['x', 'y', 'z']:
                for t in [1, 2]:
                    self.csv.loc[self.csv.temp == t, field] = getattr(self, field)

            self.csv.drop('temp',inplace = True)

        else:
            self.csv['instruction'] = list(range(self.number_event_per_job))
            self.csv['recoil_type'] = self.recoil_type

            for field in ['x', 'y', 'z']:
                self.csv[field] = getattr(self, field)

            if self.correlated == True:
                self.csv['t'] = self.default_event_time
                self.csv['s1_photons'] = self.photon_number
                self.csv['s2_electrons'] = self.electron_number

            elif self.correlated == 'S1':
                self.csv['t'] = self.default_event_time
                self.csv['s1_photons'] = self.photon_number
                self.csv['s2_electrons'] = 0

            elif self.correlated == 'S2':
                self.csv['t'] = self.default_event_time+self.z/self.DriftVelocity
                self.csv['s1_photons'] = 0
                self.csv['s2_electrons'] = self.electron_number

        # Write to csv file
        self.csv.rename(columns = {'z':'depth'}, inplace = True)
        self.csv.to_csv('{csv_path}/{production_id}.csv'.format(csv_path = self.csv_path, production_id = self.production_id), 
                        sep = ',', index = False)

    def _randomize_FV(self):
        self.cm2mm = 1

        ####################################
        ## FV definitions (HARDCODE WARNING):
        ####################################

        # randomize the X, Y, Z according to X48kg FV
        if self.detector == 'XENON100':
            Zlower, Zupper = -14.6-15.0, -14.6+15.0
            Rlower, Rupper = -np.sqrt(200.), np.sqrt(200.)

        elif self.detector == 'XENON1T': # NEED TO UPDATE THIS
            Zlower, Zupper, Rupper = -92.9, -9, 36.94

        r2 = np.random.uniform(0, Rupper*Rupper, self.number_event_per_job)
        angle = np.random.uniform(-np.pi, np.pi, self.number_event_per_job)

        self.r = np.sqrt(r2)
        self.x = self.r * np.cos(angle) * self.cm2mm
        self.y = self.r * np.sin(angle) * self.cm2mm
        self.z = - 1 * np.random.uniform(Zlower,Zupper,self.number_event_per_job) * self.cm2mm
        return (self.x, self.y, self.z)

    def _randomize_photon_number(self):
        self.photon_number = np.random.randint(self.photon_number_low, self.photon_number_high, self.number_event_per_job)
        return self.photon_number

    def _randomize_electron_number(self):        
        self.electron_number = np.random.randint(self.electron_number_low, self.electron_number_high, self.number_event_per_job)
        return self.electron_number

class CreateFakeFromPickle(ProductionProcess):
    ''' Read a pickled real data from {cwd}/{config_name}.pkl
        Create fake data and write to {production_id}.csv at {csv} directory'''

    process_order = 1
    __version__ = '0.0.1'

    def __init__(self):
        self.default_event_time = 1000. # Where we put S1

    def _process(self):
        self.csv_path = self.config['DIRECTORY']['csv'] # Where the csv will be save to
        self.detector = self.config['BASICS']['detector']
        self.number_event_per_job = int(self.config['BASICS']['number_event_per_job'])
        self.recoil_type = self.config['BASICS']['recoil_type']

        self.csv = pd.DataFrame(columns = ['instruction', 'recoil_type', 'x', 'y', 'depth', 
                                           's1_photons', 's2_electrons', 't'])

        self.original = pd.read_pickle(os.path.join(self.config['DIRECTORY']['cwd'],'%s.pkl'%self.config_name))
        self.original = self.original.reset_index(drop=True)
        self.order = int(self.production_id[-6:])

        self.original = self.original.ix[self.order*self.number_event_per_job : (self.order+1)*self.number_event_per_job-1, :]
        self.original = self.original.loc[:, ['event_number', 'x', 'y', 'z', 'cs1', 'cs2']]

        self.original.rename(columns = {'event_number':'instruction'}, inplace = True)

        for field in ['instruction', 'x', 'y']:
            self.csv[field] = self.original[field]
   
        self.csv['depth'] = - self.original['z']
        self.csv['s1_photons'] = np.array(np.around(self.original['cs1'].values / 0.12), dtype = np.int)
        self.csv['s2_electrons'] = np.array(np.around(self.original['cs2'].values / 23), dtype = np.int)
        self.csv['recoil_type'] = 'NR'
        self.csv['t'] = self.default_event_time

        self.csv.to_csv('{csv_path}/{production_id}.csv'.format(csv_path = self.csv_path, production_id = self.production_id), 
                        sep = ',', index = False)


class PaxerProcess(ProductionProcess):
    '''Use commend line submition to run paxer'''
    def _generate_commend(self):
        raise NotImplementedError()

    def _process(self):
        self._generate_commend()
        with Popen(self.cmd, shell = True, stderr = STDOUT, stdout = PIPE) as self.proc:
            # Here redirct 2&>1
            with self._divert_stdout():
                try:
                    self.stdout, self.stderr = self.proc.communicate(timeout=1800)
                    self.stdout = self.stdout.decode('utf-8')
                    self.productionlog.write(self.stdout)
                except TimeoutExpired:
                    print ('Subprocess timed out at 1800s')
                    self.proc.kill()
                    self.stdout, self.stderr = self.proc.communicate()
                    self.stdout = self.stdout.decode('utf-8')
                    self.productionlog.write(self.stdout)


class Simulation(PaxerProcess):
    '''Use paxer simulation to generate both fax_truth and pax_raw data'''

    process_order = 2
    __version__ = '0.0.1'

    def _generate_commend(self):
        self.no_pmt_afterpulse = not eval(self.config['BASICS']['pmt_afterpulse'])
        self.no_s2_afterpulse = not eval(self.config['BASICS']['s2_afterpulse'])
        self.personalize = eval(self.config['BASICS']['personalize_config'])

        self.map = dict(production_id = self.production_id,
                        csv_path = self.config['DIRECTORY']['csv'],
                        truth_raw_path = self.config['DIRECTORY']['truth_raw'],
                        raw_path = self.config['DIRECTORY']['raw'],
                        detector = self.config['BASICS']['detector'],
                        NoPmtAP_config = os.path.join(self.config['DIRECTORY']['cwd'], 'configs', 'NoPMTAfterpulses.ini'),
                        NoS2AP_config = os.path.join(self.config['DIRECTORY']['cwd'], 'configs', 'NoS2Afterpulses.ini'),
                        Personalize_config = os.path.join(self.config['DIRECTORY']['cwd'], 'configs', 'Personalize.ini'),
                       )

        cmds = ['paxer', 
                '--input {csv_path}/{production_id}.csv',
                '--config {detector} reduce_raw_data Simulation',
                '--config_string "[WaveformSimulator]truth_file_name=\'{truth_raw_path}/{production_id}\'"',
                '--output {raw_path}/{production_id}']

        # Make out put directory
        if not os.path.exists('{raw_path}/{production_id}'.format(**self.map)):
            os.makedirs('{raw_path}/{production_id}'.format(**self.map))

        additional_cmd = ''
        keys = ['NoPmtAP_config', 'NoS2AP_config', 'Personalize_config']
        for iy, ac in enumerate([self.no_pmt_afterpulse, self.no_s2_afterpulse, self.personalize]):
            if ac:
                if additional_cmd == '':
                    additional_cmd += '--config_path'

                additional_cmd += ' {%s}'%keys[iy]
        cmds.append(additional_cmd)

        self.cmd = ' '.join(cmds)
        self.cmd = self.cmd.format(**self.map)


class ProcessRaw(PaxerProcess):
    '''User paxer to process raw data into processed data'''

    process_order = 3
    __version__ = '0.0.1'

    def _generate_commend(self):
        self.map = dict(production_id = self.production_id,
                        raw_path = self.config['DIRECTORY']['raw'],
                        processed_path = self.config['DIRECTORY']['processed'],
                        detector = self.config['BASICS']['detector'],
                       )

        cmds = ['paxer',
                '--ignore_rundb',
                '--input {raw_path}/{production_id}',
                '--config {detector}',
                '--output {processed_path}/{production_id}']

        self.cmd = ' '.join(cmds)
        self.cmd = self.cmd.format(**self.map)


class SortTruth(ProductionProcess):
    '''Sort peak infomation in fax_truth from peak to event level'''

    process_oerder = 4
    __version__ = '0.0.1'

    def _process(self):
        # Read in the csv file
        self.truth_raw_path = self.config['DIRECTORY']['truth_raw']
        self.truth_sorted_path = self.config['DIRECTORY']['truth_sorted']

        self.truth_file = open(os.path.join(self.truth_raw_path, '{name}.csv'.format(name = self.production_id)))
        self.truth_peak = pd.read_csv(self.truth_file)
        self.truth_peak.drop(['fax_truth_peak_id','g4_id','instruction','repetition','n_electrons',
                              't_first_electron','t_last_electron','t_sigma_electrons','t_mean_electrons','t_interaction',
                              't_first_photon','t_last_photon','z',
                             ], axis = 1, inplace = True)

        # Separate out s1, s2, and other peaks
        tmp = []
        for i, peak_type in enumerate(['s1', 's2', 'other_s2']):
            if peak_type == 'other_s2':
                _df = self.truth_peak[~self.truth_peak.peak_type.isin(['s1', 's2'])]
                tmp.append(_df.loc[_df.groupby('event').n_photons.idxmax()])
            else:
                tmp.append(self.truth_peak[self.truth_peak.peak_type == peak_type])

            replace_dict = {
                            'n_photons' : '%s' % peak_type,
                            't_mean_photons' : '%s_hit_time_mean' % peak_type,
                            't_sigma_photons' : '%s_width' % peak_type,
                            'top_fraction' : '%s_area_fraction_top' % peak_type,
                            'x' : '%s_x' % peak_type,
                            'y' : '%s_y' % peak_type,
                           }

            tmp[i].rename(columns = replace_dict, inplace = True)
            tmp[i].drop('peak_type', axis = 1, inplace = True)

        # Create a new dataframe on event level,  
        # Merge s1, s2 and other peaks accroding to 'event' columns
        self.truth_event = pd.DataFrame()
        self.truth_event['event_number'] = self.truth_peak.event.unique()

        for t in tmp:
            self.truth_event = self.truth_event.merge(t, left_on = 'event_number', 
                                                      right_on = 'event', how = 'left').drop('event', axis = 1)

        # Doing some refining jobs
        self.truth_event.drop(['s1_x', 's1_y', 'other_s2_x', 'other_s2_y'], axis = 1, inplace = True)
        self.truth_event.rename(columns = {'s2_x':'x', 's2_y':'y'}, inplace = True)

        # Save the sorted dataframe to pickle
        self.truth_event.to_pickle(os.path.join(self.truth_sorted_path, '{name}.pkl'.format(name = self.production_id)))
        self.truth_event.to_csv(os.path.join(self.truth_sorted_path, '{name}.csv'.format(name = self.production_id)),index = False)


class BuildMiniTree(ProductionProcess):
    '''Run hax to create minitree'''

    process_oerder = 5
    __version__ = '0.0.1'

    def hax_init(self, force_reload = False):
        self.main_data_path = self.config['DIRECTORY']['processed']
        self.minitree_path = self.config['DIRECTORY']['minitree']

        # Trick learned from Daniel Coderre's DAQVeto lichen
        if (not len(hax.config)) or force_reload:
            # User didn't init hax yet... let's do it now
            hax.init(experiment = 'XENON1T',
                     main_data_paths = [self.main_data_path],
                     minitree_paths = [self.minitree_path],
                     version_policy = 'loose'
                    )

        elif not (self.main_data_path in hax.config['main_data_paths']):
            hax.config['main_data_paths'] = ['.', self.main_data_path]

        elif not (self.minitree_path == hax.config['minitree_paths'][0]):
            hax.config['minitree_paths'] = [self.minitree_path]

    def _process(self):
        self.hax_init(force_reload = False)
        self.minitree_pickle_path = self.config['DIRECTORY']['minitree_pickle']

        with self._divert_stdout():
            self.df = hax.minitrees.load(self.production_id,['Basics', 'Fundamentals', 'Extended'])
            self.df.to_pickle(os.path.join(self.minitree_pickle_path, '{name}.pkl'.format(name = self.production_id)))
            print ('{production_id} minitrees building success :)'.format(production_id = self.production_id))


class MergeTruth(ProductionProcess):
    '''Merge sorted fax truth with minitree pickle give every column in fax truth prefix: truth_{column_name}'''

    process_oerder = 6
    __version__ = '0.0.1'

    def _process(self):
        self.truth_sorted_path = self.config['DIRECTORY']['truth_sorted']
        self.minitree_pickle_path = self.config['DIRECTORY']['minitree_pickle']
        self.merged_path = self.config['DIRECTORY']['merged']

        self.truth = pd.read_pickle('{path}/{name}.pkl'.format(path = self.truth_sorted_path, name = self.production_id))
        self.data = pd.read_pickle('{path}/{name}.pkl'.format(path = self.minitree_pickle_path, name = self.production_id))

        # Change column name for truth
        name_replace_dict = {col : 'truth_' + col for col in self.truth.columns}
        self.truth.rename(columns = name_replace_dict, inplace = True)

        self.merged = self.data.merge(self.truth, left_on='event_number', right_on='truth_event_number', how='outer')
        self.merged.drop('truth_event_number', axis = 1, inplace = True)
        self.merged.to_pickle('{path}/{name}.pkl'.format(path = self.merged_path, name = self.production_id))


# When called upon, run RunAllProcess.process
if __name__ == '__main__':
    arg = sys.argv
    if not (len (arg) == 3):
        sys.exit(1)

    head_directory = arg[1]
    production_list_file = arg[2]
    
    # Process a list of productions
    if 'txt' in production_list_file:
        errors = []
        production_list = np.array(np.genfromtxt(production_list_file, dtype='<U32'), ndmin=1)
        for prod in production_list:
            try:
                production_process = RunAllProcess()
                production_process.process(head_directory = head_directory, production_id = prod)
            except Exception as e:
                err = dict(production_id = prod,
                           error_type = e.__class__.__name__,
                           error_message = str(e),
                          )
                print (str(e))
                errors.append(err)

        print ('Enconter %d exceptions' %len(errors))
        if len(errors) != 0:
            errors = pd.DataFrame(errors)
            errors.to_pickle(production_list_file[:-11]+'err_msg.pkl')

    # Process a single prodution
    else:
        prod = production_list_file
        production_process = RunAllProcess()
        production_process.process(head_directory = head_directory, production_id = prod)