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

modifications18 = {'member_of_campaign': 'RunIIFall18wmLHEGS'}

RequestsToClone=ListOfRequests('EXO-RunIIFall17wmLHEGS-00576','EXO-RunIIFall17wmLHEGS-00616')

for request_prepid_to_clone in RequestsToClone:
    request = mcm.get('requests', request_prepid_to_clone)
    request[u'fragment'] = request[u'fragment'].replace("from Configuration.Generator.MCTunes2017.PythiaCP3Settings_cfi import *\n","from Configuration.Generator.MCTunes2017.PythiaCP3Settings_cfi import *\nfrom Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *\n")
    request[u'fragment'] = request[u'fragment'].replace("pythia8CP3SettingsBlock,\n","pythia8CP3SettingsBlock,\n        pythia8PSweightsSettingsBlock,\n")
    request[u'fragment'] = request[u'fragment'].replace("\'pythia8CP3Settings\',\n","\'pythia8CP3Settings\',\n                                    \'pythia8PSweightsSettings\'\n")
    for key in modifications18: request[key] = modifications18[key]
    clone_answer = mcm.clone_request(request)
    print(clone_answer)
    #if clone_answer.get('results'):
    #    print('Clone PrepID: %s' % (clone_answer['prepid']))
    #else:
    #    print('Something went wrong while cloning a request. %s' % (dumps(clone_answer)))
