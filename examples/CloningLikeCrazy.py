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

modifications = {'member_of_campaign': 'RunIIWinter15pLHE',
                 'fragment': 'import FWCore.ParameterSet.Config as cms\n\nfrom Configuration.Generator.Pythia8CommonSettings_cfi import *\nfrom Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *\n\ngenerator = cms.EDFilter("Pythia8HadronizerFilter",\n    maxEventsToPrint = cms.untracked.int32(1),\n    pythiaPylistVerbosity = cms.untracked.int32(1),\n    filterEfficiency = cms.untracked.double(1.0),\n    pythiaHepMCVerbosity = cms.untracked.bool(False),\n    comEnergy = cms.double(13000.),\n    PythiaParameters = cms.PSet(\n        pythia8CommonSettingsBlock,\n        pythia8CUEP8M1SettingsBlock,\n        parameterSets = cms.vstring(\'pythia8CommonSettings\',\n                                    \'pythia8CUEP8M1Settings\'\n                                    )\n    )\n)\n\nProductionFilterSequence = cms.Sequence(generator)'}

RequestsToClone=[
'EXO-RunIIFall17pLHE-00007',
'EXO-RunIIFall17pLHE-00008',
'EXO-RunIIFall17pLHE-00009',
'EXO-RunIIFall17pLHE-00010',
'EXO-RunIIFall17pLHE-00011',
'EXO-RunIIFall17pLHE-00012',
'EXO-RunIIFall17pLHE-00013',
'EXO-RunIIFall17pLHE-00014',
'EXO-RunIIFall17pLHE-00015',
'EXO-RunIIFall17pLHE-00016',
'EXO-RunIIFall17pLHE-00017',
'EXO-RunIIFall17pLHE-00018',
'EXO-RunIIFall17pLHE-00019',
'EXO-RunIIFall17pLHE-00020',
'EXO-RunIIFall17pLHE-00021',
'EXO-RunIIFall17pLHE-00022',
'EXO-RunIIFall17pLHE-00023',
'EXO-RunIIFall17pLHE-00024',
'EXO-RunIIFall17pLHE-00025',
'EXO-RunIIFall17pLHE-00026',
'EXO-RunIIFall17pLHE-00027',
'EXO-RunIIFall17pLHE-00028',
'EXO-RunIIFall17pLHE-00029',
'EXO-RunIIFall17pLHE-00030',
'EXO-RunIIFall17pLHE-00031',
'EXO-RunIIFall17pLHE-00032',
'EXO-RunIIFall17pLHE-00033',
'EXO-RunIIFall17pLHE-00034',
'EXO-RunIIFall17pLHE-00035',
'EXO-RunIIFall17pLHE-00036',
'EXO-RunIIFall17pLHE-00037',
'EXO-RunIIFall17pLHE-00038',
'EXO-RunIIFall17pLHE-00039',
'EXO-RunIIFall17pLHE-00040',
'EXO-RunIIFall17pLHE-00041',
'EXO-RunIIFall17pLHE-00042',
'EXO-RunIIFall17pLHE-00043',
'EXO-RunIIFall17pLHE-00044',
'EXO-RunIIFall17pLHE-00045',
'EXO-RunIIFall17pLHE-00046',
'EXO-RunIIFall17pLHE-00047',
'EXO-RunIIFall17pLHE-00048',
'EXO-RunIIFall17pLHE-00049',
'EXO-RunIIFall17pLHE-00050',
'EXO-RunIIFall17pLHE-00051',
'EXO-RunIIFall17pLHE-00052',
'EXO-RunIIFall17pLHE-00053',
'EXO-RunIIFall17pLHE-00054',
'EXO-RunIIFall17pLHE-00055',
'EXO-RunIIFall17pLHE-00056',
'EXO-RunIIFall17pLHE-00057',
'EXO-RunIIFall17pLHE-00058',
'EXO-RunIIFall17pLHE-00059',
'EXO-RunIIFall17pLHE-00060',
'EXO-RunIIFall17pLHE-00061',
'EXO-RunIIFall17pLHE-00185',
'EXO-RunIIFall17pLHE-00062',
'EXO-RunIIFall17pLHE-00063',
'EXO-RunIIFall17pLHE-00064',
'EXO-RunIIFall17pLHE-00065',
'EXO-RunIIFall17pLHE-00066',
'EXO-RunIIFall17pLHE-00067',
'EXO-RunIIFall17pLHE-00068',
'EXO-RunIIFall17pLHE-00069',
'EXO-RunIIFall17pLHE-00070',
'EXO-RunIIFall17pLHE-00071',
'EXO-RunIIFall17pLHE-00072',
'EXO-RunIIFall17pLHE-00073',
'EXO-RunIIFall17pLHE-00074',
'EXO-RunIIFall17pLHE-00075',
'EXO-RunIIFall17pLHE-00076',
'EXO-RunIIFall17pLHE-00077',
'EXO-RunIIFall17pLHE-00186',
'EXO-RunIIFall17pLHE-00078',
'EXO-RunIIFall17pLHE-00079',
'EXO-RunIIFall17pLHE-00080',
'EXO-RunIIFall17pLHE-00081',
'EXO-RunIIFall17pLHE-00082',
'EXO-RunIIFall17pLHE-00083',
'EXO-RunIIFall17pLHE-00084',
'EXO-RunIIFall17pLHE-00085',
'EXO-RunIIFall17pLHE-00086',
'EXO-RunIIFall17pLHE-00087',
'EXO-RunIIFall17pLHE-00088',
'EXO-RunIIFall17pLHE-00089',
'EXO-RunIIFall17pLHE-00090',
'EXO-RunIIFall17pLHE-00091',
'EXO-RunIIFall17pLHE-00187',
'EXO-RunIIFall17pLHE-00092',
'EXO-RunIIFall17pLHE-00093',
'EXO-RunIIFall17pLHE-00094',
'EXO-RunIIFall17pLHE-00095',
'EXO-RunIIFall17pLHE-00096',
'EXO-RunIIFall17pLHE-00097',
'EXO-RunIIFall17pLHE-00098',
'EXO-RunIIFall17pLHE-00099',
'EXO-RunIIFall17pLHE-00100',
'EXO-RunIIFall17pLHE-00101',
'EXO-RunIIFall17pLHE-00102',
'EXO-RunIIFall17pLHE-00103',
'EXO-RunIIFall17pLHE-00104',
'EXO-RunIIFall17pLHE-00105',
'EXO-RunIIFall17pLHE-00106'
]

for request_prepid_to_clone in RequestsToClone:
    request = mcm.get('requests', request_prepid_to_clone)
    for key in modifications: request[key] = modifications[key]
    clone_answer = mcm.clone_request(request)
    if clone_answer.get('results'):
        print('Clone PrepID: %s' % (clone_answer['prepid']))
    else:
        print('Something went wrong while cloning a request. %s' % (dumps(clone_answer)))



