#!/usr/bin/env python

import sys
import os.path
import argparse
import csv
import pprint
import time
import urllib2
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import *

# Physics working group for manageRequests.py
# Options: B2G BPH BTW EGM EWK EXO FSQ FWD HCA HIG HIN JME L1T MUO QCD SMP SUS
#          TAU TOP TRK TSG
pwg = 'EXO'

# McM username
username = 'jruizalv'

# Automatically remove color when piping or redirecting output
auto_bw = False

# Database
database_location = 'MC_Requests.db'
html_location = ''

mcm = McM(dev=False)
mod_req = mcm.get(u'requests', u'EXO-RunIIWinter15pLHE-04044')

print mod_req

#mod_req = mcm.get('requests', 'EXO-PhaseIISummer17wmLHEGENOnly-00015')

#print mod_req

#mod_req = mcm.get('requests', 'EXO-RunIIFall17GS-00041')
#
#print mod_req
