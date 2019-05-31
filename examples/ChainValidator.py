#!/usr/bin/env python

import sys
import time
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import *

from Essential import * 

CR18QBH=ListOfRequests('EXO-chain_RunIIFall18pLHE_flowRunIIFall18GS_flowRunIIAutumn18DRPremix_flowRunIIAutumn18MiniAOD_flowRunIIAutumn18NanoAODv4-00105','EXO-chain_RunIIFall18pLHE_flowRunIIFall18GS_flowRunIIAutumn18DRPremix_flowRunIIAutumn18MiniAOD_flowRunIIAutumn18NanoAODv4-00169')
for i in CR18QBH:
    print(mcm.get(u'chained_requests', i, method='test'))

CR16QBH=ListOfRequests('EXO-chain_RunIIWinter15pLHE_flowLHE2Summer15GS_flowRunIISummer16DR80PremixPUMoriond17_flowRunIISummer16MiniAODv3_flowRunIISummer16NanoAODv4-00193','EXO-chain_RunIIWinter15pLHE_flowLHE2Summer15GS_flowRunIISummer16DR80PremixPUMoriond17_flowRunIISummer16MiniAODv3_flowRunIISummer16NanoAODv4-00258')
for i in CR16QBH:
    print(mcm.get(u'chained_requests', i, method='test'))

CR18RPV=ListOfRequests('EXO-chain_RunIIFall18pLHE_flowRunIIFall18GS_flowRunIIAutumn18DRPremix_flowRunIIAutumn18MiniAOD_flowRunIIAutumn18NanoAODv4-00170','EXO-chain_RunIIFall18pLHE_flowRunIIFall18GS_flowRunIIAutumn18DRPremix_flowRunIIAutumn18MiniAOD_flowRunIIAutumn18NanoAODv4-00283')
for i in CR18RPV:
    print(mcm.get(u'chained_requests', i, method='test'))
