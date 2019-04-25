import sys
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import McM
from json import dumps

mcm = McM(dev=False)

# Script clones a request to other campaign.
# Define list of modifications
# If member_of_campaign is different, it will clone to other campaign
modifications = {'member_of_campaign': 'RunIIFall18GS'}

# WJJ
#input_prepids = ["EXO-RunIIFall17GS-01174","EXO-RunIIFall17GS-01175","EXO-RunIIFall17GS-01176","EXO-RunIIFall17GS-01177","EXO-RunIIFall17GS-01178","EXO-RunIIFall17GS-01179","EXO-RunIIFall17GS-01180","EXO-RunIIFall17GS-01181","EXO-RunIIFall17GS-01182","EXO-RunIIFall17GS-01183","EXO-RunIIFall17GS-01184","EXO-RunIIFall17GS-01185","EXO-RunIIFall17GS-01186","EXO-RunIIFall17GS-01187","EXO-RunIIFall17GS-01188","EXO-RunIIFall17GS-01189","EXO-RunIIFall17GS-01190","EXO-RunIIFall17GS-01191","EXO-RunIIFall17GS-01192","EXO-RunIIFall17GS-01193","EXO-RunIIFall17GS-01194","EXO-RunIIFall17GS-01195","EXO-RunIIFall17GS-01196","EXO-RunIIFall17GS-01197","EXO-RunIIFall17GS-01198","EXO-RunIIFall17GS-01199","EXO-RunIIFall17GS-01200","EXO-RunIIFall17GS-01201","EXO-RunIIFall17GS-01202","EXO-RunIIFall17GS-01203","EXO-RunIIFall17GS-01204","EXO-RunIIFall17GS-01205","EXO-RunIIFall17GS-01206","EXO-RunIIFall17GS-01207","EXO-RunIIFall17GS-01208","EXO-RunIIFall17GS-01209","EXO-RunIIFall17GS-01210","EXO-RunIIFall17GS-01211","EXO-RunIIFall17GS-01212","EXO-RunIIFall17GS-01213","EXO-RunIIFall17GS-01214","EXO-RunIIFall17GS-01215","EXO-RunIIFall17GS-01216","EXO-RunIIFall17GS-01217","EXO-RunIIFall17GS-01218","EXO-RunIIFall17GS-01219","EXO-RunIIFall17GS-01220","EXO-RunIIFall17GS-01221"]
# WLNU
input_prepids = ["EXO-RunIIFall17GS-01227", "EXO-RunIIFall17GS-01265", "EXO-RunIIFall17GS-01222", "EXO-RunIIFall17GS-01223", "EXO-RunIIFall17GS-01224", "EXO-RunIIFall17GS-01225", "EXO-RunIIFall17GS-01226", "EXO-RunIIFall17GS-01228", "EXO-RunIIFall17GS-01229", "EXO-RunIIFall17GS-01230", "EXO-RunIIFall17GS-01231", "EXO-RunIIFall17GS-01232", "EXO-RunIIFall17GS-01233", "EXO-RunIIFall17GS-01234", "EXO-RunIIFall17GS-01235", "EXO-RunIIFall17GS-01236", "EXO-RunIIFall17GS-01237", "EXO-RunIIFall17GS-01238", "EXO-RunIIFall17GS-01239", "EXO-RunIIFall17GS-01240", "EXO-RunIIFall17GS-01241", "EXO-RunIIFall17GS-01242", "EXO-RunIIFall17GS-01243", "EXO-RunIIFall17GS-01244", "EXO-RunIIFall17GS-01245", "EXO-RunIIFall17GS-01246", "EXO-RunIIFall17GS-01247", "EXO-RunIIFall17GS-01248", "EXO-RunIIFall17GS-01249", "EXO-RunIIFall17GS-01250", "EXO-RunIIFall17GS-01251", "EXO-RunIIFall17GS-01252", "EXO-RunIIFall17GS-01253", "EXO-RunIIFall17GS-01254", "EXO-RunIIFall17GS-01255", "EXO-RunIIFall17GS-01256", "EXO-RunIIFall17GS-01257", "EXO-RunIIFall17GS-01258", "EXO-RunIIFall17GS-01259", "EXO-RunIIFall17GS-01260", "EXO-RunIIFall17GS-01261", "EXO-RunIIFall17GS-01262", "EXO-RunIIFall17GS-01263", "EXO-RunIIFall17GS-01264", "EXO-RunIIFall17GS-01266", "EXO-RunIIFall17GS-01267", "EXO-RunIIFall17GS-01268", "EXO-RunIIFall17GS-01269"]
 
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
	    print clone_answer
	else:
	    print('Something went wrong while cloning a request. %s' % (dumps(clone_answer)))