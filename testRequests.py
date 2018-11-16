#!/usr/bin/env python

################################
#
# testRequests.py
#
#  Script to test the time and size per event of
#  requests in McM. Prepares results in a CSV file
#  that can be used by manageRequests.py
#
#  author: David G. Sheffield (Rutgers)
#  maintainer: Jose Ruiz (Vanderbilt)
#
################################

import sys
import os
import subprocess
import argparse
import csv
import re
import glob
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import * # Load class to access McM
from requestClass import * # Load class to store request information

def getArguments():
    parser = argparse.ArgumentParser(description='Test McM requests.')

    # Command line flags
    parser.add_argument('-i', '--ids', dest='ids', help=
                        'List of PrepIDs to be tested. Separate range by >.')
    parser.add_argument('-f', '--file', dest='csv', help='Input CSV file.')
    parser.add_argument('-o', '--output', dest='output', default='test.csv',
                        help='Output CSV file')
    parser.add_argument('-b', '--bsub', dest='bsub', action='store_true', help='Use bsub instead of condor')
    parser.add_argument('-n', dest='nEvents', help='Number of events to test.')

    args_ = parser.parse_args()
    return args_

def fillIDRange(pwg, campaign, first, last):
    first = int(first)
    last = int(last)
    requests = []
    if first > last:
        print "Error: PrepID range out of order. {0}-{1}-{2:05d} > {0}-{1}-{3:05d}".format(
            pwg, campaign, first, last)
        sys.exit(4)

    for number in range(first, last+1):
        tmpReq = Request()
        tmpReq.setPrepId("{0}-{1}-{2:05d}".format(pwg, campaign, number))
        requests.append(tmpReq)
    return requests

def parseIDList(compactList):
    splitList = compactList.split(',')
    requests = []
    for subList in splitList:
        splitSubList = subList.split('-')
        if len(splitSubList) == 3:
            tmpReq = Request()
            tmpReq.setPrepId(subList)
            requests.append(tmpReq)
        elif len(splitSubList) == 4:
            requests = requests + fillIDRange(splitSubList[0], splitSubList[1],
                                              splitSubList[2], splitSubList[3])
        elif len(splitSubList) == 6:
            if splitSubList[0] != splitSubList[3]:
                print "Error: PrepID range must be for the same PWG."
                sys.exit(4)
            if splitSubList[1] != splitSubList[4]:
                print "Error: PrepID range must be for the same campaign."
                sys.exit(4)
            requests = requests + fillIDRange(splitSubList[0], splitSubList[1],
                                              splitSubList[2], splitSubList[5])
        else:
            print "Error: Poorly formed PrepID list."
            print "Exiting with status 3."
            sys.exit(3)
    return requests

def getTestScript(PrepID, nEvents, use_bsub=False):
    request_type = "requests"
    if "chain_" in PrepID:
        request_type = "chained_requests"

    get_test = ""
    if use_bsub:
        scriptFile = "{}.sh".format(PrepID)
    else:
        scriptFile = "test_{}/{}.sh".format(PrepID, PrepID)
    if nEvents is None:
        get_test =  "curl -s --insecure \
https://cms-pdmv.cern.ch/mcm/public/restapi/{0}/get_test/{1} -o {2}".format(
            request_type, PrepID, scriptFile)
    else:
        # add "/N" to end of URL to get N events
        os.system("mkdir -pv test_{}".format(PrepID))
        get_test =  "curl -s --insecure \
https://cms-pdmv.cern.ch/mcm/public/restapi/{0}/get_test/{1}/{2} -o {3}".format(
            request_type, PrepID, nEvents, scriptFile)
    print get_test
    subprocess.call(get_test, shell=True)

    if request_type == "chained_requests" and nEvents is not None:
        tmpScriptFile = "tmp{}".format(scriptFile)
        inputfile = open(scriptFile, 'r')
        outputfile = open(tmpScriptFile, 'w')
        for line in inputfile:
            outline = re.sub('(.*--eventcontent LHE.*-n) \d*( .*)',
                             r'\1 {0}\2'.format(nEvents), line)
            outline = re.sub('(.*--eventcontent DQM.*-n) \d*( .*)',
                             r'\1 {0}\2'.format(nEvents), outline)
            outline = re.sub('(.*--eventcontent RAWSIM.*-n) \d*( .*)',
                             r'\1 {0}\2'.format(nEvents), outline)
            outputfile.write(outline)
        inputfile.close()
        outputfile.close()
        os.rename(tmpScriptFile, scriptFile)

    subprocess.call("chmod 755 {}".format(scriptFile), shell=True)
    return

def submitToBatch(PrepId):
    batch_command = "bsub -q 8nh {0}.sh".format(PrepId)
    print batch_command
    output = subprocess.Popen(batch_command, stdout=subprocess.PIPE,
                              shell=True).communicate()[0]
    match = re.match('Job <(\d*)> is', output)
    jobID = match.group(1)
    return jobID

def submitToCondor(PrepId):
    batch_command = "csub {}.sh -t workday -d test_{}".format(PrepId, PrepId)
    print batch_command
    output = subprocess.Popen(batch_command, stdout=subprocess.PIPE,
                              shell=True).communicate()[0]
    print output
    match = re.search('submitted to cluster (\d*)', output)
    jobID = match.group(1)
    return jobID

def createTest(compactPrepIDList, outputFile, nEvents, use_bsub=False):
    requests = parseIDList(compactPrepIDList)

    csvfile = csv.writer(open(outputFile, 'w'))
    csvfile.writerow(['PrepId', 'JobId', 'Time per event [s]',
                      'Size per event [kB]'])

    print "Testing {0} requests".format(len(requests))
    for req in requests:
        getTestScript(req.getPrepId(), nEvents)
        if use_bsub:
            jobID = submitToBatch(req.getPrepId())
        else:
            jobID = submitToCondor(req.getPrepId())
        req.setJobID(jobID)
        searched = re.search('chain_', req.getPrepId())
        if searched is None:
            csvfile.writerow([req.getPrepId(), req.getJobID(), "", ""])
        else:
            mcm = McM(dev=False) # Get McM connection
            mcm_req = mcm.get('chained_requests', req.getPrepId())
            wmLHEPrepId = mcm_req['chain'][0]
            GSPrepId = mcm_req['chain'][1]
            csvfile.writerow([wmLHEPrepId, req.getJobID(), "", ""])
            csvfile.writerow([GSPrepId, req.getJobID(), "", ""])
    return

def exitDuplicateField(file_in_,field_):
    print "Error: File {0} contains multiple instances of the field {1}".format(
        file_in_, field_)
    sys.exit(5)

def getFields(csvfile):
    # List of indices for each field in CSV file
    list = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
             -1, -1, -1, -1, -1, -1, -1, -1]
    header = csv.reader(csvfile).next()
    for ind, field in enumerate(header):
        field = field.lower()
        if field in ['dataset name', 'dataset']:
            #ensure no duplicate fields
            if list[0] > -1:
                exitDuplicateField(file_in_, "Dataset name")
            list[0] = ind
        elif field in ['eos', 'mcdbid']:
            if list[1] > -1:
                exitDuplicateField(file_in_, "EOS")
            list[1] = ind
        elif field in ['cross section [pb]', 'cross section',
                       'cross section (pb)', 'cs', 'cs [pb]', 'cs (pb)', 'xsec',
                       'xsec [pb]', 'xsec (pb)']:
            if list[2] > -1:
                exitDuplicateField(file_in_, "Cross section [pb]")
            list[2] = ind
        elif field in ['total events', 'events', 'number of events']:
            if list[3] > -1:
                exitDuplicateField(file_in_, "Total events")
            list[3] = ind
        elif field in ['fragment name', 'generator fragment name', 'fragment']:
            if list[4] > -1:
                exitDuplicateField(file_in_, "Fragment name")
            list[4] = ind
        elif field in ['time per event [s]', 'time per event',
                       'time per event (s)', 'time', 'time [s]', 'time (s)']:
            if list[5] > -1:
                exitDuplicateField(file_in_, "Time per event [s]")
            list[5] = ind
        elif field in ['size per event [kb]', 'size per event',
                       'size per event (kb)', 'size', 'size [kb]', 'size (kb)']:
            if list[6] > -1:
                exitDuplicateField(file_in_, "Size per event [kB]")
            list[6] = ind
        elif field in ['tag', 'fragment tag', 'sha', 'sha-1']:
            if list[7] > -1:
                exitDuplicateField(file_in_, "Fragment tag")
            list[7] = ind
        elif field in ['generator', 'generators']:
            if list[8] > -1:
                exitDuplicateField(file_in_, "Generator")
            list[8] = ind
        elif field in ['filter efficiency']:
            if list[9] > -1:
                exitDuplicateField(file_in_, "Filter efficiency")
            list[9] = ind
        elif field in ['filter efficiency error']:
            if list[10] > -1:
                exitDuplicateField(file_in_, "Filter efficiency error")
            list[10] = ind
        elif field in ['match efficiency']:
            if list[11] > -1:
                exitDuplicateField(file_in_, "Match efficiency")
            list[11] = ind
        elif field in ['match efficiency error']:
            if list[12] > -1:
                exitDuplicateField(file_in_, "Match efficiency error")
            list[12] = ind
        elif field in ['pwg']:
            if list[13] > -1:
                exitDuplicateField(file_in_, "PWG")
            list[13] = ind
        elif field in ['campaign', 'member of campaign']:
            if list[14] > -1:
                exitDuplicateField(file_in_, "Member of campaign")
            list[14] = ind
        elif field in ['prepid']:
            if list[15] > -1:
                exitDuplicateField(file_in_, "PrepID")
            list[15] = ind
        elif field in ['sequences customise', 'sequences customize']:
            if list[16] > -1:
                exitDuplicateField(file_in_, "Sequences customise")
            list[16] = ind
        elif field in ['process string']:
            if list[17] > -1:
                exitDuplicateField(file_in_, "Process string")
            list[17] = ind
        elif field in ['gridpack location', 'gridpack']:
            if list[18] > -1:
                exitDuplicateField(file_in_, "Gridpack location")
            list[18] = ind
        elif field in ['gridpack cards url', 'cards url',
                       'gridpack cards location', 'cards location']:
            if list[19] > -1:
                exitDuplicateField(file_in_, "Gridpack cards URL")
            list[19] = ind
        elif field in ['jobid']:
            if list[20] > -1:
                exitDuplicateField(file_in_, "JobId")
            list[20] = ind
        elif field in ['notes']:
            if list[21] > -1:
                exitDuplicateField(file_in_, "Notes")
            list[21] = ind
        elif field in ['mcm tag', 'mcm tags']:
            if list[22] > -1:
                exitDuplicateField(file_in_, "McM tags")
            list[22] = ind
        elif field in ['sequences beamspot']:
            if list[23] > -1:
                exitDuplicateField(file_in_, "Sequences beamspot")
            list[23] = ind
        elif field in ['sequences magField']:
            if list[24] > -1:
                exitDuplicateField(file_in_, "Sequences magField")
            list[24] = ind
        elif field in ['local gridpack location', 'Local lhe', 'lhe']:
            continue
        else:
            print "Error: The field {0} is not valid.".format(field)
            sys.exit(6)

    return list

def fillFields(csvfile, fields):
    requests = [] # List containing request objects
    num_requests = 0
    for row in csv.reader(csvfile):
        if row[0].startswith("#"):
            continue
        num_requests += 1
        tmpReq = Request()
        if fields[0] > -1:
            tmpReq.setDataSetName(row[fields[0]])
        if fields[1] > -1:
            tmpReq.setMCDBID(row[fields[1]])
        if fields[2] > -1:
            tmpReq.setCS(row[fields[2]])
        if fields[3] > -1:
            tmpReq.setEvts(row[fields[3]])
        if fields[14] > -1:
            campaign = row[fields[14]]
            tmpReq.setCamp(campaign)
        if fields[4] > -1:
            tmpReq.setFrag(formatFragment(row[fields[4]],campaign))
        if fields[5] > -1 and row[fields[5]] != "":
            tmpReq.setTime(row[fields[5]])
        if fields[6] > -1 and row[fields[6]] != "":
            tmpReq.setSize(row[fields[6]])
        if fields[7] > -1:
            tmpReq.setTag(row[fields[7]])
        if fields[8] > -1:
            tmpReq.setGen(row[fields[8]].split(" ")) # Multiple generators separated by spaces
        if fields[9] > -1:
            tmpReq.setFiltEff(row[fields[9]])
        if fields[10] > -1:
            tmpReq.setFiltEffErr(row[fields[10]])
        if fields[11] > -1:
            tmpReq.setMatchEff(row[fields[11]])
        if fields[12] > -1:
            tmpReq.setMatchEffErr(row[fields[12]])
        if fields[13] > -1:
            tmpReq.setPWG(row[fields[13]])
        if fields[15] > -1:
            tmpReq.setPrepId(row[fields[15]])
        if fields[16] > -1:
            tmpReq.setSequencesCustomise(row[fields[16]])
        if fields[17] > -1:
            tmpReq.setProcessString(row[fields[17]])
        if fields[18] > -1:
            if fields[19] > -1:
                tmpReq.setMcMFrag(createLHEProducer(row[fields[18]],
                                                    row[fields[19]]))
            else:
                tmpReq.setMcMFrag(createLHEProducer(row[fields[18]], ""))
        if fields[20] > -1:
            tmpReq.setJobID(row[fields[20]])
        if fields[21] > -1:
            tmpReq.setNotes(row[fields[21]])
        if fields[22] > -1:
            tmpReq.setMcMTag(row[fields[22]].split(" "))
        if fields[23] > -1:
            tmpReq.setSequencesBeamspot(row[fields[23]])
        if fields[24] > -1:
            tmpReq.setSequencesMagField(row[fields[24]])
        requests.append(tmpReq)
    return requests, num_requests

def rewriteCSVFile(csvfile, requests):
    csvWriter = csv.writer(csvfile)
    csvWriter.writerow(['PrepId', 'JobId', 'Time per event [s]',
                        'Size per event [kB]', 'match efficiency'])

    for req in requests:
        timePerEvent = ""
        if req.useTime(): timePerEvent = req.getTime()
        sizePerEvent = ""
        if req.useSize(): sizePerEvent = req.getSize()
        matchEff = ""
        if req.useMatchEff(): matchEff = req.getMatchEff()

        csvWriter.writerow([req.getPrepId(), req.getJobID(), timePerEvent,
                            sizePerEvent, matchEff])
    return

def getTimeSizeFromFile(stdoutFile, iswmLHE, use_bsub=False):
    totalSize = 0
    timePerEvent = 0
    nEvents = 0
    XsBeforeMatch = 0
    XsAfterMatch = 0
    matchEff = 0
    fileContents = open(stdoutFile, 'r')
    for line in fileContents:
        match = re.match('<TotalEvents>(\d*)</TotalEvents>', line)
        #match = re.match('(\d*) events were ran', line)
        if match is not None:
            nEvents = float(match.group(1))
            continue
        match = re.match('    <Metric Name="Timing-tstoragefile-write-totalMegabytes" Value="(\d*\.\d*)"/>',
                         line)
        if match is not None:
            totalSize = float(match.group(1))
            continue
        if 'Before matching' in line: 
            XsBeforeMatch=float(line.split('=')[-1].split('+-')[0])
            print "Cross section Before Matching:", XsBeforeMatch
        if 'After matching' in line: 
            XsAfterMatch=float(line.split('=')[-1].split('+-')[0])
            print "Cross section After Matching: ", XsAfterMatch
        if XsAfterMatch!=0 and XsBeforeMatch!=0: matchEff=XsAfterMatch/XsBeforeMatch
        timePerEvent1=0; timePerEvent2=0; timePerEvent3=0; timePerEvent4=0;
        match = re.match('    <Metric Name="AvgEventCPU" Value="(\d*\.\d*)"/>',
                         line)
        if match is not None:
            timePerEvent1 = float(match.group(1))
            continue
        match = re.match('    <Metric Name="TotalJobCPU" Value="(\d*\.\d*)"/>',
                         line)
        if match is not None:
            timePerEvent2 = float(match.group(1))
            continue
        match = re.match('    <Metric Name="AvgEventTime" Value="(\d*\.\d*)"/>',
                         line)
        if match is not None:
            timePerEvent3 = float(match.group(1))
            continue
        match = re.match('    <Metric Name="TotalJobTime" Value="(\d*\.\d*)"/>',
                         line)
        if match is not None:
            timePerEvent4 = float(match.group(1))
            timePerEvent=max(timePerEvent1,timePerEvent2,timePerEvent3,timePerEvent4)/nEvents
            if not iswmLHE:
                matchEff=1.0
                continue
            else:
                break

    if nEvents != 0:
        sizePerEvent = totalSize*1024.0/nEvents
    else:
        sizePerEvent = -1
    print "Found (time, size, matchEff)=({}, {}, {}) in file {}:".format(timePerEvent, sizePerEvent, matchEff, stdoutFile)
    return timePerEvent, sizePerEvent, matchEff

def getTimeSize(requests, use_bsub=False, force_update=False):
    number_complete = 0
    for req in requests:
        if not req.useTime() or not req.useSize() or force_update:
            if use_bsub:
                stdoutFile = "LSFJOB_{0}/STDOUT".format(req.getJobID())
            else:
                stdoutCandidates = glob.glob("test_{}/*{}*.stdout".format(req.getPrepId(), req.getJobID()))
                if len(stdoutCandidates) == 0:
                    print "[getTimeSize] WARNING : Didn't find output file for request {}".format(req.getJobID())
                elif len(stdoutCandidates) >= 1:
                    # Multiple attempts: use latest
                    stdoutCandidates.sort(key=lambda x: os.path.getmtime(x), reverse=True)
                stdoutFile = stdoutCandidates[0]
            if os.path.exists(stdoutFile):
                number_complete += 1
                iswmLHE = False
                searched = re.search('wmLHE', req.getPrepId())
                if searched is not None:
                    iswmLHE = True
                timePerEvent, sizePerEvent, matchEff = getTimeSizeFromFile(stdoutFile, iswmLHE, use_bsub=use_bsub)

                if timePerEvent == 0:
                    print "[getTimeSize] WARNING : timePerEvent=0 for request {}. Try resubmitting.".format(req.getPrepId())
                    print "testRequests.py -n 20 -i {}".format(req.getPrepId())

                req.setTime(timePerEvent)
                req.setSize(sizePerEvent)
                req.setMatchEff(matchEff)
        else:
            number_complete += 1

    if number_complete == len(requests):
        print "Extracted info for all {0} requests.".format(len(requests))
    else:
        print "Extracted info for {0} of {1} requests. {2} requests remain.".format(
            number_complete, len(requests), len(requests) - number_complete)
    return

def extractTest(inputCsvFilePath, force_update=False, use_bsub=False):
    inputCsvFile = open(inputCsvFilePath, 'r') # Open CSV file
    fields = getFields(csvfile)  # Get list of field indices
    # Fill list of request objects from CSV file and get number of requests
    requests, num_requests = fillFields(inputCsvFile, fields)
    inputCsvFile.close()

    getTimeSize(requests, force_update=force_update, use_bsub=use_bsub)

    outputCsvFile = open("results_{}".format(inputCsvFilePath), 'w')
    rewriteCSVFile(outputCsvFile, requests)

    return

def main():
    args = getArguments() # Setup flags and get arguments
    if args.ids and args.csv:
        print "Error: Cannot use both -i and -f."
        sys.exit(1)
    elif args.ids:
        createTest(args.ids, args.output, args.nEvents, use_bsub=args.bsub)
    elif args.csv:
        extractTest(args.csv, use_bsub=args.bsub)
    else:
        print "Error: Must use either -i or -f."
        sys.exit(2)

if __name__ == '__main__':
    main()
