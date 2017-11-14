#!/usr/bin/env python3
#
# This script should go on Midway here:
#  /project/lgrandi/xenon1t/grid_proxy
# as called by renew-cron.sh

import os
import sys
import subprocess
import shutil

PROXY_LOCATION = '/project/lgrandi/xenon1t/grid_proxy/xenon_service_proxy'

os.chmod(PROXY_LOCATION, 0o640)
shutil.chown(PROXY_LOCATION, group='pi-lgrandi') 
