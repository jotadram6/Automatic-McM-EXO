import sys
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import McM
from json import dumps

mcm = McM(dev=False)

# Script clones a request to other campaign.
# Fefine list of modifications
# If member_of_campaign is different, it will clone to other campaign
modifications = {'member_of_campaign': 'RunIIFall18wmLHEGS'}

# WJJ
#input_prepids = ["EXO-RunIIFall17wmLHEGS-00350", "EXO-RunIIFall17wmLHEGS-00351", "EXO-RunIIFall17wmLHEGS-00352", "EXO-RunIIFall17wmLHEGS-00353", "EXO-RunIIFall17wmLHEGS-00354", "EXO-RunIIFall17wmLHEGS-00355", "EXO-RunIIFall17wmLHEGS-00356", "EXO-RunIIFall17wmLHEGS-00357", "EXO-RunIIFall17wmLHEGS-00358", "EXO-RunIIFall17wmLHEGS-00359", "EXO-RunIIFall17wmLHEGS-00360", "EXO-RunIIFall17wmLHEGS-00361", "EXO-RunIIFall17wmLHEGS-00362", "EXO-RunIIFall17wmLHEGS-00363", "EXO-RunIIFall17wmLHEGS-00364", "EXO-RunIIFall17wmLHEGS-00365", "EXO-RunIIFall17wmLHEGS-00366", "EXO-RunIIFall17wmLHEGS-00367", "EXO-RunIIFall17wmLHEGS-00368", "EXO-RunIIFall17wmLHEGS-00369", "EXO-RunIIFall17wmLHEGS-00370", "EXO-RunIIFall17wmLHEGS-00371", "EXO-RunIIFall17wmLHEGS-00372", "EXO-RunIIFall17wmLHEGS-00373", "EXO-RunIIFall17wmLHEGS-00374", "EXO-RunIIFall17wmLHEGS-00375", "EXO-RunIIFall17wmLHEGS-00376", "EXO-RunIIFall17wmLHEGS-00377", "EXO-RunIIFall17wmLHEGS-00378", "EXO-RunIIFall17wmLHEGS-00379", "EXO-RunIIFall17wmLHEGS-00380", "EXO-RunIIFall17wmLHEGS-00381", "EXO-RunIIFall17wmLHEGS-00382", "EXO-RunIIFall17wmLHEGS-00383", "EXO-RunIIFall17wmLHEGS-00384", "EXO-RunIIFall17wmLHEGS-00385", "EXO-RunIIFall17wmLHEGS-00386", "EXO-RunIIFall17wmLHEGS-00387", "EXO-RunIIFall17wmLHEGS-00388", "EXO-RunIIFall17wmLHEGS-00389", "EXO-RunIIFall17wmLHEGS-00390", "EXO-RunIIFall17wmLHEGS-00391", "EXO-RunIIFall17wmLHEGS-00392", "EXO-RunIIFall17wmLHEGS-00393", "EXO-RunIIFall17wmLHEGS-00394", "EXO-RunIIFall17wmLHEGS-00395", "EXO-RunIIFall17wmLHEGS-00396", "EXO-RunIIFall17wmLHEGS-00397"]
# WLNu
input_prepids = ["EXO-RunIIFall17wmLHEGS-00398", "EXO-RunIIFall17wmLHEGS-00399", "EXO-RunIIFall17wmLHEGS-00400", "EXO-RunIIFall17wmLHEGS-00401", "EXO-RunIIFall17wmLHEGS-00402", "EXO-RunIIFall17wmLHEGS-00403", "EXO-RunIIFall17wmLHEGS-00404", "EXO-RunIIFall17wmLHEGS-00405", "EXO-RunIIFall17wmLHEGS-00406", "EXO-RunIIFall17wmLHEGS-00407", "EXO-RunIIFall17wmLHEGS-00408", "EXO-RunIIFall17wmLHEGS-00409", "EXO-RunIIFall17wmLHEGS-00410", "EXO-RunIIFall17wmLHEGS-00411", "EXO-RunIIFall17wmLHEGS-00412", "EXO-RunIIFall17wmLHEGS-00413", "EXO-RunIIFall17wmLHEGS-00414", "EXO-RunIIFall17wmLHEGS-00415", "EXO-RunIIFall17wmLHEGS-00416", "EXO-RunIIFall17wmLHEGS-00417", "EXO-RunIIFall17wmLHEGS-00418", "EXO-RunIIFall17wmLHEGS-00419", "EXO-RunIIFall17wmLHEGS-00420", "EXO-RunIIFall17wmLHEGS-00421", "EXO-RunIIFall17wmLHEGS-00422", "EXO-RunIIFall17wmLHEGS-00423", "EXO-RunIIFall17wmLHEGS-00424", "EXO-RunIIFall17wmLHEGS-00425", "EXO-RunIIFall17wmLHEGS-00426", "EXO-RunIIFall17wmLHEGS-00427", "EXO-RunIIFall17wmLHEGS-00428", "EXO-RunIIFall17wmLHEGS-00429", "EXO-RunIIFall17wmLHEGS-00430", "EXO-RunIIFall17wmLHEGS-00431", "EXO-RunIIFall17wmLHEGS-00432", "EXO-RunIIFall17wmLHEGS-00433", "EXO-RunIIFall17wmLHEGS-00434", "EXO-RunIIFall17wmLHEGS-00435", "EXO-RunIIFall17wmLHEGS-00436", "EXO-RunIIFall17wmLHEGS-00437", "EXO-RunIIFall17wmLHEGS-00438", "EXO-RunIIFall17wmLHEGS-00439", "EXO-RunIIFall17wmLHEGS-00440", "EXO-RunIIFall17wmLHEGS-00441", "EXO-RunIIFall17wmLHEGS-00442", "EXO-RunIIFall17wmLHEGS-00443", "EXO-RunIIFall17wmLHEGS-00444", "EXO-RunIIFall17wmLHEGS-00445"]

for input_prepid in input_prepids:
	request = mcm.get('requests', input_prepid)

	# Make predefined modifications
	for key in modifications:
	    request[key] = modifications[key]

	frag17 = request["fragment"]
	if "PSweights" in frag17:
		continue
	frag18 = frag17.replace("from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *\n", 
							"from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *\nfrom Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *\n")\
				.replace("pythia8CP5SettingsBlock,\n", 
						 "pythia8CP5SettingsBlock,\n        pythia8PSweightsSettingsBlock,\n")\
				.replace("\'pythia8CP5Settings\',\n", 
						 "\'pythia8CP5Settings\',\n                                    \'pythia8PSweightsSettings\',\n")
	request["fragment"] = frag18

	clone_answer = mcm.clone_request(request)
	if clone_answer.get('results'):
	    print('Clone PrepID: %s' % (clone_answer['prepid']))
	else:
	    print('Something went wrong while cloning a request. %s' % (dumps(clone_answer)))