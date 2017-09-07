# This script is to be run as a crontab on login.xenon.ci-connect.net:
#     00 23 * * 5 /xenon/grid_proxy/renew-cron.sh

source /xenon/grid_proxy/setup.sh
python /xenon/grid_proxy/renew-proxy.py
ssh midway.rcc.uchicago.edu '/project/lgrandi/xenon1t/grid_proxy/chgrp-proxy.py'
