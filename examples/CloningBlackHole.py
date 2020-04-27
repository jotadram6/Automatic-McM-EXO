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

modifications18 = {'member_of_campaign': 'RunIIWinter15pLHE'}

RequestsToClone=ListOfRequests('EXO-RunIIFall17pLHE-00368','EXO-RunIIFall17pLHE-00392')

for request_prepid_to_clone in RequestsToClone:
    request = mcm.get('requests', request_prepid_to_clone)
    request[u'fragment'] = request[u'fragment'].replace("from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *\n","from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *\n")
    request[u'fragment'] = request[u'fragment'].replace("pythia8CP5SettingsBlock,\n","pythia8CUEP8M1SettingsBlock,\n")
    request[u'fragment'] = request[u'fragment'].replace("\'pythia8CP5Settings\'\n","\'pythia8CUEP8M1Settings\'\n")
    for key in modifications18: request[key] = modifications18[key]
    clone_answer = mcm.clone_request(request)
    print(clone_answer)
    #if clone_answer.get('results'):
    #    print('Clone PrepID: %s' % (clone_answer['prepid']))
    #else:
    #    print('Something went wrong while cloning a request. %s' % (dumps(clone_answer)))
