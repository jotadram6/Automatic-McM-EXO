#!/usr/bin/env python

from Essentials import *

CorrectionsNeeded={
"EXO-RunIIFall17GS-05112": 0.63281250,
"EXO-RunIIFall17GS-05109": 0.44704861,
"EXO-RunIISummer15GS-14517": 0.44357639,
"EXO-RunIIFall17GS-05106": 0.50781250,
"EXO-RunIIFall17GS-05111": 0.77430556,
"EXO-RunIISummer15GS-14501": 0.82899306,
"EXO-RunIIFall18GS-03283": 0.45052083,
"EXO-RunIIFall17GS-05105": 0.50607639,
"EXO-RunIISummer15GS-14515": 0.44878472,
"EXO-RunIIFall18GS-03279": 0.56076389,
"EXO-RunIISummer15GS-14499": 0.82204861,
"EXO-RunIIFall18GS-03268": 0.68402778,
"EXO-RunIIFall18GS-03281": 0.51996528,
"EXO-RunIISummer15GS-14513": 0.46267361,
"EXO-RunIIFall18GS-03280": 0.52864583,
"EXO-RunIIFall17GS-05113": 0.60850694,
"EXO-RunIIFall18GS-03282": 0.54253472,
"EXO-RunIIFall17GS-05110": 0.42708333,
"EXO-RunIISummer15GS-14500": 0.72222222,
"EXO-RunIISummer15GS-14502": 0.77864583,
"EXO-RunIIFall18GS-03273": 0.43315972,
"EXO-RunIISummer15GS-14506": 0.54687500,
"EXO-RunIISummer15GS-14511": 0.47743056,
"EXO-RunIIFall18GS-03262": 0.69010417,
"EXO-RunIIFall18GS-03275": 0.41059028,
"EXO-RunIISummer15GS-14510": 0.50260417,
"EXO-RunIIFall17GS-05122": 0.81510417,
"EXO-RunIIFall17GS-05102": 0.72482639,
"EXO-RunIIFall18GS-03267": 0.60937500,
"EXO-RunIISummer15GS-14516": 0.44097222,
"EXO-RunIIFall17GS-05115": 0.56163194,
"EXO-RunIIFall18GS-03285": 0.58159722,
"EXO-RunIIFall18GS-03284": 0.40711806,
"EXO-RunIIFall18GS-03272": 0.48090278,
"EXO-RunIIFall17GS-05119": 0.45920139,
"EXO-RunIISummer15GS-14507": 0.57899306,
"EXO-RunIISummer15GS-14509": 0.50434028,
"EXO-RunIISummer15GS-14512": 0.49739583,
"EXO-RunIIFall17GS-05121": 0.43663194,
"EXO-RunIIFall18GS-03277": 0.71267361,
"EXO-RunIIFall17GS-05118": 0.51388889,
"EXO-RunIIFall18GS-03265": 0.67187500,
"EXO-RunIISummer15GS-14514": 0.46527778,
"EXO-RunIIFall17GS-05117": 0.53732639,
"EXO-RunIIFall17GS-05114": 0.54774306,
"EXO-RunIIFall18GS-03276": 0.76909722,
"EXO-RunIIFall17GS-05123": 0.82638889,
"EXO-RunIIFall18GS-03264": 0.75694444,
"EXO-RunIIFall18GS-03269": 0.49392361,
"EXO-RunIIFall18GS-03263": 0.80208333,
"EXO-RunIISummer15GS-14495": 0.68750000,
"EXO-RunIIFall17GS-05103": 0.67708333,
"EXO-RunIISummer15GS-14504": 0.60329861,
"EXO-RunIIFall18GS-03274": 0.44184028,
"EXO-RunIISummer15GS-14505": 0.59809028,
"EXO-RunIIFall18GS-03266": 0.82638889,
"EXO-RunIIFall17GS-05116": 0.53732639,
"EXO-RunIISummer15GS-14498": 0.77690972,
"EXO-RunIISummer15GS-14503": 0.66059028,
"EXO-RunIIFall18GS-03270": 0.46527778,
"EXO-RunIIFall18GS-03278": 0.59722222
}

def AwsomeFunction(MyAwsomeList):
    for i in MyAwsomeList:
        pLHER=mcm.get(u'chained_requests', i)[u'chain'][0]
        #print pLHER
        #if int(pLHER.split("-")[-1])!=295: continue
        GSR=mcm.get(u'chained_requests', i)[u'chain'][1]
        #print pLHER, GSR
        pLHERequest=mcm.get('requests', pLHER)
        GSRequest=mcm.get('requests', GSR)
        #if ListOf2017R.index(i)==0:
        #    print pLHERequest[u"status"]
        #    print pLHERequest[u"approval"]
        #    print GSRequest[u"memory"]
        #    print GSRequest[u"sequences"][0][u"nThreads"]
        #    print pLHERequest[u"memory"]
        #    print pLHERequest[u"sequences"]
        #for i in pLHERequest.keys():
        #    print "------------------------------------------> KEY:", i
        #    print pLHERequest[i]
        #print GSRequest[u"validation"]
        #if GSRequest[u'size_event'][0] == 0: 
        #    GSRequest[u'size_event'] = [100.]
        #if GSRequest[u'time_event'][0] == 0:
        #    GSRequest[u'time_event'] = [10.0]
        GSRequest[u'size_event'] = [100.]
        GSRequest[u'time_event'] = [10.0]
        #pLHERequest[u'time_event'] = [pLHERequest[u'time_event'][0]*10]
        #if pLHERequest[u'time_event'][0]>=0.001: pLHERequest[u'time_event'] = [0.0006]
        #if GSRequest[u'time_event'][0]<=11.: GSRequest[u'time_event'] = [80.]
        #FIRST TIME CONFIGS
        #GSRequest[u'time_event'] = [80.]
        #GSRequest[u'size_event'] = [900.]
        #pLHERequest[u'time_event'] = [0.0006]
        #pLHERequest[u'size_event'] = [6340.]
        GSRequest[u"memory"] = 2300
        GSRequest[u"sequences"][0][u"nThreads"] = 1
        pLHERequest[u"memory"] = 2300
        pLHERequest[u"sequences"][0][u"nThreads"] = 1
        pLHERequest[u"validation"][u'time_multiplier'] = 2
        GSRequest[u"validation"][u'time_multiplier'] = 2
        #pLHERequest[u'fragment'] = pLHERequest[u'fragment'].replace("\'pythia8CP5Settings\',\n","\'pythia8CUEP8M1Settings\'\n")
        GSRequest[u'fragment'] = pLHERequest[u'fragment']
        pLHERequest[u'generator_parameters'][0][u'cross_section'] = 1.0
        pLHERequest[u'generator_parameters'][0][u'filter_efficiency'] = 1.0
        pLHERequest[u'generator_parameters'][0][u'filter_efficiency_error'] = 0.0
        pLHERequest[u'generator_parameters'][0][u'match_efficiency'] = 1.0
        pLHERequest[u'generator_parameters'][0][u'match_efficiency_error'] = 0.0
        pLHERequest[u'generator_parameters'][0][u'negative_weights_fraction'] = -1.0
        GSRequest[u'generator_parameters'] = pLHERequest[u'generator_parameters']
        if GSR in CorrectionsNeeded.keys():
            GSRequest[u'generator_parameters'][0][u'filter_efficiency'] = CorrectionsNeeded[GSR]
            GSRequest[u'total_events'] = pLHERequest[u'total_events']*CorrectionsNeeded[GSR]
        pLHERequest[u"keep_output"]=[True]
        GSRequest[u"keep_output"]=[True]
        #pLHERequest[u'dataset_name'] = pLHERequest[u'dataset_name'].replace('CP5','CUEP8M1')
        #GSRequest[u'dataset_name'] = GSRequest[u'dataset_name'].replace('CP5','CUEP8M1')
        
        ##################
        if pLHERequest[u"approval"] == "none" and GSRequest[u"approval"] == "none":
            update_answer = mcm.update('requests', GSRequest)
            print("Updating GS:",GSR,update_answer)
            update_answer = mcm.update('requests', pLHERequest)
            print("Updating pLHE:",pLHER,update_answer)
            print("Validation:", mcm.get(u'chained_requests', i, method='test'))
        if pLHERequest[u"approval"] == "none" and GSRequest[u"approval"] == "validation":
            print("Problems, LHE not validated while GS is being validated!")
        if pLHERequest[u"approval"] == "validation" and GSRequest[u"approval"] == "none":
            print("Problems, LHE validated while GS is not!")
            print(mcm.approve('requests', GSR, None))
        if pLHERequest[u"status"] == "validation" and GSRequest[u"status"] == "validation":
            print("Both LHE and GS have been validated, now moving them to define.")
            print(mcm.approve('requests', pLHER, None))
            print(mcm.approve('requests', GSR, None))

#Swagata-Kerstin QBH

ListOf2016R=ListOfRequests('EXO-chain_RunIIWinter15pLHE_flowLHE2Summer15GS_flowRunIISummer16DR80PremixPUMoriond17_flowRunIISummer16MiniAODv3_flowRunIISummer16NanoAODv7-00001','EXO-chain_RunIIWinter15pLHE_flowLHE2Summer15GS_flowRunIISummer16DR80PremixPUMoriond17_flowRunIISummer16MiniAODv3_flowRunIISummer16NanoAODv7-00024')

ListOf2017R=ListOfRequests('EXO-chain_RunIIFall17pLHE_flowRunIIFall17pLHE2GS_flowRunIIFall17DRPremixPU2017_flowRunIIFall17MiniAODv2_flowRunIIFall17NanoAODv7-00001','EXO-chain_RunIIFall17pLHE_flowRunIIFall17pLHE2GS_flowRunIIFall17DRPremixPU2017_flowRunIIFall17MiniAODv2_flowRunIIFall17NanoAODv7-00024')

ListOf2018R=ListOfRequests('EXO-chain_RunIIFall18pLHE_flowRunIIFall18GS_flowRunIIAutumn18DRPremix_flowRunIIAutumn18MiniAOD_flowRunIIAutumn18NanoAODv7-00001','EXO-chain_RunIIFall18pLHE_flowRunIIFall18GS_flowRunIIAutumn18DRPremix_flowRunIIAutumn18MiniAOD_flowRunIIAutumn18NanoAODv7-00024')

#Justin CTPPS

#ListOf2016R=ListOfRequests('EXO-chain_RunIIWinter15pLHE_flowLHE2Summer15GS_flowRunIISummer16DR80PremixPUMoriond17_flowRunIISummer16MiniAODv3_flowRunIISummer16NanoAODv6-00283','EXO-chain_RunIIWinter15pLHE_flowLHE2Summer15GS_flowRunIISummer16DR80PremixPUMoriond17_flowRunIISummer16MiniAODv3_flowRunIISummer16NanoAODv6-00286')

#ListOf2017R=ListOfRequests('EXO-chain_RunIIFall17pLHE_flowRunIIFall17pLHE2GS_flowRunIIFall17DRPremixPU2017_flowRunIIFall17MiniAODv2_flowRunIIFall17NanoAODv6-00362','EXO-chain_RunIIFall17pLHE_flowRunIIFall17pLHE2GS_flowRunIIFall17DRPremixPU2017_flowRunIIFall17MiniAODv2_flowRunIIFall17NanoAODv6-00365')

#ListOf2018R=ListOfRequests('EXO-chain_RunIIFall18pLHE_flowRunIIFall18GS_flowRunIIAutumn18DRPremix_flowRunIIAutumn18MiniAOD_flowRunIIAutumn18NanoAODv6-00309','EXO-chain_RunIIFall18pLHE_flowRunIIFall18GS_flowRunIIAutumn18DRPremix_flowRunIIAutumn18MiniAOD_flowRunIIAutumn18NanoAODv6-00312')

#Sushil

#ListOf2016R=ListOfRequests('EXO-chain_RunIIWinter15pLHE_flowLHE2Summer15GS_flowRunIISummer16DR80PremixPUMoriond17_flowRunIISummer16MiniAODv3_flowRunIISummer16NanoAODv6-00258','EXO-chain_RunIIWinter15pLHE_flowLHE2Summer15GS_flowRunIISummer16DR80PremixPUMoriond17_flowRunIISummer16MiniAODv3_flowRunIISummer16NanoAODv6-00282')

#ListOf2017R=ListOfRequests('EXO-chain_RunIIFall17pLHE_flowRunIIFall17pLHE2GS_flowRunIIFall17DRPremixPU2017_flowRunIIFall17MiniAODv2_flowRunIIFall17NanoAODv5-00351','EXO-chain_RunIIFall17pLHE_flowRunIIFall17pLHE2GS_flowRunIIFall17DRPremixPU2017_flowRunIIFall17MiniAODv2_flowRunIIFall17NanoAODv5-00375')

#ListOf2018R=ListOfRequests('EXO-chain_RunIIFall18pLHE_flowRunIIFall18GS_flowRunIIAutumn18DRPremix_flowRunIIAutumn18MiniAOD_flowRunIIAutumn18NanoAODv5-00104','EXO-chain_RunIIFall18pLHE_flowRunIIFall18GS_flowRunIIAutumn18DRPremix_flowRunIIAutumn18MiniAOD_flowRunIIAutumn18NanoAODv5-00128')

AwsomeFunction(ListOf2016R)
AwsomeFunction(ListOf2017R)
AwsomeFunction(ListOf2018R)

"""for i in ListOf2017R:
    pLHER=mcm.get(u'chained_requests', i)[u'chain'][0]
    GSR=mcm.get(u'chained_requests', i)[u'chain'][1]
    pLHERequest=mcm.get('requests', pLHER)
    GSRequest=mcm.get('requests', GSR)
    #if ListOf2017R.index(i)==0:
    #    print pLHERequest[u"status"]
    #    print pLHERequest[u"approval"]
    #    print GSRequest[u"memory"]
    #    print GSRequest[u"sequences"][0][u"nThreads"]
    #    print pLHERequest[u"memory"]
    #    print pLHERequest[u"sequences"]
    GSRequest[u'fragment'] = pLHERequest[u'fragment']
    GSRequest[u'generator_parameters'] = pLHERequest[u'generator_parameters']
    #GSRequest[u'generator_parameters'][0][u'cross_section'] = 1.0
    #GSRequest[u'generator_parameters'][0][u'filter_efficiency'] = 1.0
    #GSRequest[u'generator_parameters'][0][u'filter_efficiency_error'] = 0.0
    #GSRequest[u'generator_parameters'][0][u'match_efficiency'] = 1.0
    #GSRequest[u'generator_parameters'][0][u'match_efficiency_error'] = 0.0
    #GSRequest[u'generator_parameters'][0][u'negative_weights_fraction'] = -1.0
    if GSRequest[u'size_event'][0] == 0: 
        GSRequest[u'size_event'] = [100.]
    if GSRequest[u'time_event'][0] == 0:
        GSRequest[u'time_event'] = [10.0]
    GSRequest[u"memory"] = 2300
    GSRequest[u"sequences"][0][u"nThreads"] = 1
    pLHERequest[u"memory"] = 2300
    pLHERequest[u"sequences"][0][u"nThreads"] = 1
    if pLHERequest[u"approval"] == "none" and GSRequest[u"approval"] == "none":
        update_answer = mcm.update('requests', GSRequest)
        print(GSR,update_answer)
        update_answer = mcm.update('requests', pLHERequest)
        print(pLHER,update_answer)
        print("Validation:", mcm.get(u'chained_requests', i, method='test'))
    if pLHERequest[u"approval"] == "none" and GSRequest[u"approval"] == "validation":
        print("Problems!")

for i in ListOf2018R:
    pLHER=mcm.get(u'chained_requests', i)[u'chain'][0]
    GSR=mcm.get(u'chained_requests', i)[u'chain'][1]
    pLHERequest=mcm.get('requests', pLHER)
    GSRequest=mcm.get('requests', GSR)
    GSRequest[u'fragment'] = pLHERequest[u'fragment']
    GSRequest[u'generator_parameters'] = pLHERequest[u'generator_parameters']
    if GSRequest[u'size_event'][0] == 0: 
        GSRequest[u'size_event'] = [100.]
    if GSRequest[u'time_event'][0] == 0:
        GSRequest[u'time_event'] = [10.0]
    GSRequest[u"memory"] = 2300
    GSRequest[u"sequences"][0][u"nThreads"] = 1
    pLHERequest[u"memory"] = 2300
    pLHERequest[u"sequences"][0][u"nThreads"] = 1
    if pLHERequest[u"approval"] == "none" and GSRequest[u"approval"] == "none":
        update_answer = mcm.update('requests', GSRequest)
        print(GSR,update_answer)
        update_answer = mcm.update('requests', pLHERequest)
        print(pLHER,update_answer)
        print("Validation:", mcm.get(u'chained_requests', i, method='test'))
    if pLHERequest[u"approval"] == "none" and GSRequest[u"approval"] == "validation":
        print("Problems!")


for request_prepid_to_clone in pLHE:
    requestpLHE = mcm.get('requests', request_prepid_to_clone)
    requestGS = mcm.get('requests', GS[pLHE.index(request_prepid_to_clone)])
    requestGS[u'fragment'] = requestpLHE[u'fragment']
    #requestGS[u'generator_parameters'] = request[u'generator_parameters']
    requestGS[u'generator_parameters'] = [
        {u'cross_section': 1.0,
         u'filter_efficiency': 1.0,
         u'filter_efficiency_error': 0.0,
         u'match_efficiency': 1.0,
         u'match_efficiency_error': 0.0,
         u'negative_weights_fraction': -1.0,
         u'submission_details': {u'author_email': u'jose.ruiz@cern.ch',
                                 u'author_name': u'Jose Ruiz',
                                 u'author_username': u'jruizalv',
                                 u'submission_date': u'2019-05-21-17-43'},
         u'version': 0}]
    requestGS[u'size_event'] = [100.]
    requestGS[u'time_event'] = [10.0]
    update_answer = mcm.update('requests', requestGS)
    print(GS[pLHE.index(request_prepid_to_clone)],update_answer)
"""
