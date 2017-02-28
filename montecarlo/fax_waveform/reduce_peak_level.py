import numpy as np
import hax
import sys

#truth_filename = '/project/lgrandi/jhowlett/170117_1620/truth_minitrees_170117_1620/FakeWaveform_XENON1T_000000_truth'
#processed_filename = '/project/lgrandi/jhowlett/170117_1620/000000/FakeWaveform_XENON1T_000000_pax.root'
#processed_filename = 'FakeWaveform_XENON1T_000000_pax'


if len(sys.argv)<2:
    print("========== Syntax ===========")
    print("python reduce_peak_level.py <data set name (no extension)> <data path (abs.)>")
    exit()

#with open('datasets.dat', 'r') as dataset_file:
#    datasets = dataset_file.readlines()

#datasets = ['FakeWaveform_XENON1T_000000_pax', 'FakeWaveform_XENON1T_000001_pax']



#hax.init(experiment='XENON1T', main_data_paths=['/project/lgrandi/jhowlett/170117_1620/pax_170117_1620/'], minitree_paths = ['temp_minitrees'], pax_version_policy='loose')

class PeakEfficiency(hax.minitrees.TreeMaker):
    __version__ = '0.0.1'
    uses_arrays = True
    extra_branches = ['peaks.*']

    def extract_data(self, event):
        peak_fields = ['area', 'hit_time_std', 'hit_time_mean', 'area_fraction_top', 'height', 'n_contributing_channels']
        decile = [5, 7, 9]

        result = {}
        result['event_number'] = event.event_number
        result['index'] = event.event_number
        type_ints = {'s1': 1, 's2': 2, 'unknown': 3}
        peaks = [peak for peak in event.peaks if ((peak.type != 'lone_hit') and (peak.detector == 'tpc'))]
        for peak_field in peak_fields:
            result[peak_field] = np.array([getattr(peaks[i], peak_field) for i in range(len(peaks))])
        result['type'] = np.array([type_ints[getattr(peak, 'type')] for peak in peaks])
        for dec in decile:
            result['range_%i0p_area' % dec] = np.array([getattr(peaks[i], 'range_area_decile')[dec] for i in range(len(peaks))])
        return result

dataset = sys.argv[1]
datapath = sys.argv[2]
print("======= To be reduced: "+dataset)
print(datapath)
hax.init(experiment='XENON1T', main_data_paths=[datapath], use_rundb_locations=False, pax_version_policy='loose')# changed @2016-07-06, for the data after 07-03
#hax.init(main_data_paths=[datapath])# changed @2016-07-06, for the data after 07-03
#print(hax.config['main_data_paths'])

data2 = hax.minitrees.load(dataset, treemakers=[PeakEfficiency], force_reload=True)
