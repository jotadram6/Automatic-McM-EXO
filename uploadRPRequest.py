#!/usr/bin/env python
import pickle
import sys
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import * # Load class to access McM

if __name__ == "__main__":
  # Make sure CMSSW isn't setup
  if os.getenv("CMSSW_BASE") is not None:
    print "CMSSW is setup! Run in a clean shell."
    sys.exit(1)

  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument("pkl", type=str, help="Pickle file from make_rp_request")
  parser.add_argument("--eventsPerLS", "-e", type=str, required=True, help="Events per LS")
  parser.add_argument("--dev", "-d", action="store_true", help="Use MCM dev instance")
  parser.add_argument("--tag", "-t", type=str, help="Add tag to MCM requests")
  args = parser.parse_args()
  print args
  mcm = McM(dev=args.dev)

  with open(args.pkl, 'r') as f:
    # Load randomized parameter request from pickle (created with make_rp_request.py)
    request = pickle.load(f)


    # Customize MCM request
    if args.tag:
      if "tags" in request:
        request["tags"].extend(args.tag.split(","))
      else:
        request["tags"] = args.tag.split(",")

    # Upload to MCM
    answer = mcm.put('requests', request)
    if not "results" in answer:
      print "Something went wrong with MCM! Here is the response:"
      print answer
    else:
      print "Success!"
      print answer["prepid"]

      # Modify the sequence now
      mcm_request = mcm.get('requests', answer["prepid"])
      mcm_request[u"events_per_lumi"] = args.eventsPerLS
      # eventsPerLS in customise_commands is only used for validation. Set to a small number for local validation, but change to the actual number for MCM validation.
      mcm_request[u"sequences"][0][u"customise_commands"] = u"\"process.source.numberEventsInLuminosityBlock = cms.untracked.uint32(25)\""
      mcm.update('requests', mcm_request)

