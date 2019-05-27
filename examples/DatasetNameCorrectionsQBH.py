#!/usr/bin/env python

import sys
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')

from rest import *

pwg = 'EXO'
username = 'jruizalv'

database_location = 'MC_Requests.db'
html_location = ''

mcm = McM(dev=False)

def ListOfRequests(Initial,Final):
    Base=Initial.split("-")[0]+"-"+Initial.split("-")[1]+"-"
    Inum=int(Initial.split("-")[-1])
    Fnum=int(Final.split("-")[-1])
    FinalList=[]
    for i in xrange(Inum,Fnum+1):
        HowManyDigits=len(str(i))
        ZerosString='00000'
        FinalList.append(Base+ZerosString[:len(ZerosString)-HowManyDigits]+str(i))
    return FinalList

RequestsToClone=ListOfRequests('EXO-RunIIWinter15pLHE-03948','EXO-RunIIWinter15pLHE-04013')

for request_prepid_to_clone in RequestsToClone:
    request = mcm.get('requests', request_prepid_to_clone)
    request[u'dataset_name'] = request[u'dataset_name']+'_TuneCUETP8M1_13TeV-QBH-pythia8'
    update_answer = mcm.update('requests', request) 
    print(request_prepid_to_clone)
    print(update_answer)
    #if update_answer.get('results'):
    #    print('Modified PrepID: %s' % (clone_answer['prepid']))
    #else:
    #    print('Something went wrong while cloning a request. %s' % (dumps(clone_answer)))



