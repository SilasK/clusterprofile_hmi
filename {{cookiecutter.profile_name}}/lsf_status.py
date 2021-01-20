#!/usr/bin/env python3


import os
import sys
import warnings
import subprocess
import time
import logging
logger = logging.getLogger("__name__")

STATUS_ATTEMPTS = 10

jobid = sys.argv[1]

for i in range(STATUS_ATTEMPTS):
    try:
        out= subprocess.run(['bjobs','-noheader',jobid],stdout=subprocess.PIPE).stdout.decode('utf-8')
        break; # If sucessful go out of for loop
           
    except subprocess.CalledProcessError as e:
        logger.error(f"CLUSTER: can't get status for job {jobid}")
        logger.error(e)
           
        if i >= STATUS_ATTEMPTS - 1:
            logger.error(f"CLUSTER: tried {STATUS_ATTEMPTS}, mark as failed.")
            print("failed")
            exit(0)
        else:
            logger.info("CLUSTER: wait and try again")
            time.sleep(5)
try:                      
    state = out.strip().split()[2]
except Exception as e:
    logger.error(f"CLUSTER: Couln't decode bjobs output: {out}")
    logger.error(e)
    print("failed")
    exit(0)

map_state={"PEND":'running',
           "RUN":'running', 
           "PROV":"running",
           "WAIT":'running', 
           "DONE":'success',
           "":'success'}

print(map_state.get(state,'failed'))
