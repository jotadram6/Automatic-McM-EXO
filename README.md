# Automatic-McM-EXO

Getting cookies to be able to talk with MCM: source Cookies.sh  

Script to copy gridpacks to eos: copyGridpacks.sh  

Script to make tickets: makeTicket.py  

Script to create/manage requestes: manageRequests.py  

Script to automatically do local validation of requests: testRequests.py

Instructions for wmLHE requests on lxplus6:

Format to be used in the .csv file with example for each field:

Dataset name,Total events,Generator fragment name,Generator,Gridpack location,Gridpack cards URL,match efficiency,Xsec [pb],Tag,MCDBID

Debugging_wmLHE_scripts, 300000, https://raw.githubusercontent.com/jotadram6/genproductions/DarkHiggs/python/ThirteenTeV/DarkHiggs/ZprimeToDmDmDarkhiggs_DarkhiggsToBB_TuneCUETP8M1_13TeV_MLM_4f_max1j_DM_LHE_pythia8_cff.py, madgraph pythia8, /cvmfs/cms.cern.ch/phys_generator/gridpacks/slc6_amd64_gcc481/13TeV/madgraph/V5_2.4.2/DrakHiggs_MZP_MCHI/v2_patched/MZP-500_MCHI-100_slc6_amd64_gcc481_CMSSW_7_1_30_tarball.tar.xz, https://github.com/cms-sw/genproductions/tree/27fcaa7ab3f1a50fa98784318da96cc9c1564619/bin/MadGraph5_aMCatNLO/cards/production/2017/13TeV/Darkhiggs_4f_LO/, 61.9, 3.36, 05f6761656afb772d1fd7e9dde5d3e8a758724e2, 0

1. `<source Cookies.sh>`
1. python manageRequests.py -c RunIIFall17wmLHEGS -t EXO-Name-Number file.csv
1. Note down the first and last prepid of the created requests
1. python testRequests.py -n 50 -i FirstRequestPrepId-LastRequestPrepId
   1. Wait until all the jobs have finished
1. python testRequests.py -f test.csv
1. python manageRequests.py -m test.csv
1. Go to McM: https://cms-pdmv.cern.ch/mcm/requests?range=FirstRequestPrepId,LastRequestPrepId
1. Click on the icon ">" that is "next step"
   1. Wait until all requests are in "validation validation" status
   1. If some of the validation fails, click again on next step
1. Click on the icon ">" that is "next step"
   1. Check that all requests are in "defined defined" status
1. Go back to lxplus to create the ticket with: python makeTicket.py -i FirstRequestPrepId-LastRequestPrepId
1. Report the ticket on the next MCCM