# Fax Production Main

# Submitting to midway processing node

import sys, os, getpass

sys.path.append(os.getcwd())

from fax_production_control import Setup, Batch, Submit

if __name__ == '__main__':
    #### Change the parameters in arg to change production directory and batching condition
    ## for changing config: go to fax_production_control
    ## for changing data processing: go to fax_production_process
    head_directory = '/project2/lgrandi/{user}/sim/'.format(user = getpass.getuser()),
    num_group = 3,
    max_num_submit = 5,
       
    crl = Setup()
    crl.execute(head_directory = head_directory)

    crl = Batch()
    crl.execute(head_directory = head_directory, num_group = num_group)

    crl = Submit()
    crl.execute(head_directory = head_directory, max_num_submit = max_num_submit)