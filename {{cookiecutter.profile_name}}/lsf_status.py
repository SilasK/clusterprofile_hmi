#!/usr/bin/env python3


import os
import sys
import warnings
import subprocess
import time
import logging
logger = logging.getLogger("__name__")

STATUS_ATTEMPTS = 20

jobid = sys.argv[1]

for i in range(STATUS_ATTEMPTS):
    try:
        out= subprocess.run(['bjobs','-noheader',jobid],stdout=subprocess.PIPE).stdout.decode('utf-8')
        break; # If sucessful go out of for loop
           
    except sp.CalledProcessError as e:
        logger.error("sacct process error")
        logger.error(e)
           
        if i >= STATUS_ATTEMPTS - 1:
            print("failed")
            exit(0)
        else:
            time.sleep(5)
                      
state = out.strip().split()[2]


map_state={"PEND":'running',
           "RUN":'running', 
           "PROV":"running",
           "WAIT":'running', 
           "DONE":'success',
           "":'success'}

print(map_state.get(state,'failed'))
