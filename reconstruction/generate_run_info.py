#!/usr/bin/env python

import argparse
import csv
import glob
import os
import sys


def run_main():
    """
    Main function to process user input and then generate the description files for each run

    :return: exit code -- 0 on success, 1 otherwise
    """

    parser = argparse.ArgumentParser(description="Scan a run directory and create files to ")
    parser.add_argument('--run-directory', dest='run_directory',
                        action='store', default='',
                        help='path to directory with xed files to process')
    args = parser.parse_args(sys.argv[1:])
    if not os.path.isdir(args.run_directory):
        sys.stderr.write("{0} is not a directory, exiting\n".format(args.run_directory))
        return 1
    run_name = os.path.abspath(args.run_directory)
    if os.path.basename(run_name):
        run_name = os.path.basename(run_name)
    else:
        run_name = os.path.split(run_name)[0].split('/')[-1]

    for directory in os.listdir(args.run_directory):
        if not os.path.isdir(os.path.join(args.run_directory, directory)):
            continue
        csv_filename = "{0}_{1}_files.csv".format(run_name, directory)
        entries = glob.glob(os.path.join(args.run_directory, directory, '*.xed'))
        if len(entries) == 0:
            continue
        with open(csv_filename, 'w') as file_obj:
            csv_writer = csv.writer(file_obj)
            csv_writer.writerow(['Run', 'Data Set', 'File'])
            for entry in entries:
                uri = "srm://ceph-se.osgconnect.net:8443/srm/v2/" + \
                      "server?SFN=/cephfs/srm/xenon/" + \
                      entry.replace('/xenon/', '')
                csv_writer.writerow([run_name, directory, uri])


if __name__ == '__main__':
    sys.exit(run_main())