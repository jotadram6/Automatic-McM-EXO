#!/usr/bin/env python

from Essentials import *

#pLHE=ListOfRequests("","")
#GS=ListOfRequests("","")

#QBH 2016
pLHE=ListOfRequests("EXO-RunIIWinter15pLHE-03948","EXO-RunIIWinter15pLHE-04013")
GS=ListOfRequests("EXO-RunIISummer15GS-14073","EXO-RunIISummer15GS-14138")

#QBH 2017
#pLHE=ListOfRequests("EXO-RunIIFall17pLHE-00302","EXO-RunIIFall17pLHE-00367")
#GS=ListOfRequests("EXO-RunIIFall17GS-03946","EXO-RunIIFall17GS-04011")

#QBH 2018
#pLHE=ListOfRequests("EXO-RunIIFall18pLHE-00218","EXO-RunIIFall18pLHE-00283")
#GS=ListOfRequests("EXO-RunIIFall18GS-02046","EXO-RunIIFall18GS-02111")

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
