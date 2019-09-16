import os
import sys
import csv
sys.path.append("/afs/cern.ch/user/d/dryu/workspace/private/MCI/Automatic-McM-EXO")
sys.path.append("/afs/cern.ch/user/d/dryu/workspace/private/MCI/Automatic-McM-EXO/randomized_parameters")
from manageRequests import getFields
from request import RandomizedParameterRequest


if __name__ == "__main__":
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument("-s", "--spreadsheet", type=str, required=True, help="Path to spreadsheet")
  parser.add_argument("-n", "--name", type=str, required=True, help="Name of dataset")
  parser.add_argument("-c", "--campaign", type=str, required=True, help="Name of campaign")
  args = parser.parse_args()

  rp_request = RandomizedParameterRequest(dataset_name=args.name, campaign=args.campaign)
  with open(args.spreadsheet, 'rb') as spreadsheet:
    fields = getFields(spreadsheet) # Dict {column name : column index}

    params = {}
    csv_reader = csv.reader(spreadsheet)
    for i, row in enumerate(csv_reader):
      if i == 0:
        continue
      for field, index in fields.iteritems():
        params[field] = row[index]

      req_kwargs = {
        "grid_point_name":params["dataset"], 
        "fragment_path":params["fragment"], 
        "nevents":int(params["events"]), 
        "generator_name":params["generator"], 
      }
      if rp_request.type() == "gridpack":
        req_kwargs["gridpack_path"] = params["gridpack"]
      rp_request.add_request(**req_kwargs)
    rp_request.finalize(args.name)

