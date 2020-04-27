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

modifications17 = {'member_of_campaign': 'RunIIFall17pLHE',
                 'fragment': 'import FWCore.ParameterSet.Config as cms\n\nfrom Configuration.Generator.Pythia8CommonSettings_cfi import *\nfrom Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *\n\ngenerator = cms.EDFilter("Pythia8HadronizerFilter",\n    maxEventsToPrint = cms.untracked.int32(1),\n    pythiaPylistVerbosity = cms.untracked.int32(1),\n    filterEfficiency = cms.untracked.double(1.0),\n    pythiaHepMCVerbosity = cms.untracked.bool(False),\n    comEnergy = cms.double(13000.),\n    PythiaParameters = cms.PSet(\n        pythia8CommonSettingsBlock,\n        pythia8CP5SettingsBlock,\n        parameterSets = cms.vstring(\'pythia8CommonSettings\',\n                                    \'pythia8CP5Settings\'\n                                    )\n    )\n)\n\n'}

modifications18 = {'member_of_campaign': 'RunIIFall18pLHE',
                 'fragment': 'import FWCore.ParameterSet.Config as cms\n\nfrom Configuration.Generator.Pythia8CommonSettings_cfi import *\nfrom Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *\nfrom Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *\n\ngenerator = cms.EDFilter("Pythia8HadronizerFilter",\n    maxEventsToPrint = cms.untracked.int32(1),\n    pythiaPylistVerbosity = cms.untracked.int32(1),\n    filterEfficiency = cms.untracked.double(1.0),\n    pythiaHepMCVerbosity = cms.untracked.bool(False),\n    comEnergy = cms.double(13000.),\n    PythiaParameters = cms.PSet(\n        pythia8CommonSettingsBlock,\n        pythia8CP5SettingsBlock,\n        pythia8PSweightsSettingsBlock,\n        parameterSets = cms.vstring(\'pythia8CommonSettings\',\n                                    \'pythia8CP5Settings\',\n                                    \'pythia8PSweightsSettings\'\n                                    )\n    )\n)\n\n'}

RequestsToClone=ListOfRequests('EXO-RunIIWinter15pLHE-04044','EXO-RunIIWinter15pLHE-04067')

for request_prepid_to_clone in RequestsToClone:
    request = mcm.get('requests', request_prepid_to_clone)
    request[u'dataset_name'] = request[u'dataset_name'].replace("TuneCUETP8M1","TuneCP5")
    for key in modifications17: request[key] = modifications17[key]
    clone_answer = mcm.clone_request(request)
    print(clone_answer)
    #if clone_answer.get('results'):
    #    print('Clone PrepID: %s' % (clone_answer['prepid']))
    #else:
    #    print('Something went wrong while cloning a request. %s' % (dumps(clone_answer)))

for request_prepid_to_clone in RequestsToClone:
    request = mcm.get('requests', request_prepid_to_clone)
    request[u'dataset_name'] = request[u'dataset_name'].replace("TuneCUETP8M1","TuneCP5")
    for key in modifications18: request[key] = modifications18[key]
    clone_answer = mcm.clone_request(request)
    print(clone_answer)
