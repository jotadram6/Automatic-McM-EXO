#!/usr/bin/env python

import sys
import time
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

def Validator(prepid):
    #usage: Validator(u'prepid string') -> It will check the current stuatus of the 
    #given prepid and will launch validation or set request as defined depending on its status
    mcm = McM(dev=False)
    mod_req = mcm.get(u'requests', prepid)
    #Starting cehcking cases
    if mod_req[u'approval'] == u'none' or (mod_req[u'approval'] == u'validation' and mod_req[u'status'] == u'validation'):
        ValidationOut = mcm.approve(u'requests', prepid)
        if ValidationOut[u'results']:
            print "-------------------------------------------------------------"
            print "Request "+prepid+" moved to approval: "+ValidationOut[u'approval']
            print "-------------------------------------------------------------"
        TrialCounter=1
        TrialMessages=[]
        while not ValidationOut[u'results']:
            TrialMessages.append(ValidationOut[u'message'])
            time.sleep(3)
            ValidationOut = mcm.approve(u'requests', prepid)
            TrialCounter+=1
            if TrialCounter>4: 
                print "-------------------------------------------------------------"
                print "Not able to validate "+prepid
                print "Failed validation messages: ", TrialMessages
                print "Please check!!!!!!"
                print "-------------------------------------------------------------"
    else:
        print "-------------------------------------------------------------"
        print "The request "+prepid+" is currently in status: "+mod_req[u'approval']+", "+mod_req[u'status']
        print "No action taken. Nothing to be done."
        print "-------------------------------------------------------------"

if __name__ == '__main__':
    ToCheck=[u'EXO-RunIIFall18GS-01778',u'EXO-RunIIFall18GS-01290',u'EXO-RunIIFall18GS-01291',u'EXO-RunIIFall18GS-01292']
    for i in ToCheck:
        print "Starting validation on: "+i
        Validator(i)
