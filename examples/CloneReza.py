#!/usr/bin/env python

import sys
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')

from rest import *

pwg = 'EXO'
username = 'jruizalv'

database_location = 'MC_Requests.db'
html_location = ''

mcm = McM(dev=False)

#modifications = {'member_of_campaign': 'RunIIFall18pLHE',
#                 'fragment': 'import FWCore.ParameterSet.Config as cms\n\nfrom Configuration.Generator.Pythia8CommonSettings_cfi import *\nfrom Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *\nfrom Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *\n\ngenerator = cms.EDFilter("Pythia8HadronizerFilter",\n    maxEventsToPrint = cms.untracked.int32(1),\n    pythiaPylistVerbosity = cms.untracked.int32(1),\n    filterEfficiency = cms.untracked.double(1.0),\n    pythiaHepMCVerbosity = cms.untracked.bool(False),\n    comEnergy = cms.double(13000.),\n    PythiaParameters = cms.PSet(\n        pythia8CommonSettingsBlock,\n        pythia8CP5SettingsBlock,\n        pythia8PSweightsSettingsBlock,\n        parameterSets = cms.vstring(\'pythia8CommonSettings\',\n                                    \'pythia8CP5Settings\',\n                                    \'pythia8PSweightsSettings\'\n                                    )\n    )\n)\n\n'}

#modifications = {'member_of_campaign': 'RunIIWinter15pLHE',
#                 'fragment': 'import FWCore.ParameterSet.Config as cms\n\nfrom Configuration.Generator.Pythia8CommonSettings_cfi import *\nfrom Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *\n\ngenerator = cms.EDFilter("Pythia8HadronizerFilter",\n    maxEventsToPrint = cms.untracked.int32(1),\n    pythiaPylistVerbosity = cms.untracked.int32(1),\n    filterEfficiency = cms.untracked.double(1.0),\n    pythiaHepMCVerbosity = cms.untracked.bool(False),\n    comEnergy = cms.double(13000.),\n    PythiaParameters = cms.PSet(\n        pythia8CommonSettingsBlock,\n        pythia8CUEP8M1SettingsBlock,\n        parameterSets = cms.vstring(\'pythia8CommonSettings\',\n                                    \'pythia8CUEP8M1Settings\'\n                                    )\n    )\n)\n\nProductionFilterSequence = cms.Sequence(generator)'}

modifications = {'member_of_campaign': 'RunIIFall18wmLHEGS'}

RequestsToClone=[
'EXO-RunIIFall17wmLHEGS-00012',
'EXO-RunIIFall17wmLHEGS-00013',
'EXO-RunIIFall17wmLHEGS-00014',
'EXO-RunIIFall17wmLHEGS-00015',
'EXO-RunIIFall17wmLHEGS-00016',
'EXO-RunIIFall17wmLHEGS-00017',
'EXO-RunIIFall17wmLHEGS-00018',
'EXO-RunIIFall17wmLHEGS-00019',
'EXO-RunIIFall17wmLHEGS-00020',
'EXO-RunIIFall17wmLHEGS-00021'
]

for request_prepid_to_clone in RequestsToClone:
    request = mcm.get('requests', request_prepid_to_clone)
    for key in modifications: request[key] = modifications[key]
    clone_answer = mcm.clone_request(request)
    if clone_answer.get('results'):
        print('Clone PrepID: %s' % (clone_answer['prepid']))
    else:
        print('Something went wrong while cloning a request. %s' % (clone_answer))



