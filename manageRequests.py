#!/usr/bin/env python

################################
#
# manageRequests.py
#
#  Script to create, modify, and clone McM requests.
#
#  author: David G. Sheffield (Rutgers)
#  maintainer: Jose Ruiz (Vanderbilt)
#
################################

import sys
import os.path
import argparse
import csv
import pprint
import time
import urllib2
import mcmscripts_config
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import * # Load class to access McM
from requestClass import * # Load class to store request information

def getArguments():
    parser = argparse.ArgumentParser(
        description='Create, modify, and clone McM requests.')

    # Command line flags
    parser.add_argument('file_in')
    parser.add_argument('-c', '--campaign', action='store', dest='campaign',
                        metavar='name', help='Set member_of_campaign.')
    parser.add_argument('-p', '--pwg', action='store', dest='pwg',
                        default=mcmscripts_config.pwg,
                        help='Set PWG. Defaults to %(default)s. Change default in config.py')
    parser.add_argument('-m', '--modify', action='store_true', dest='doModify',
                        help='Modify existing requests. The CSV file must contain the PrepIds of the requests to be modified.')
    parser.add_argument('--clone', action='store', dest='cloneId', default='',
                        help='Clone an existing request by giving its PrepId')
    parser.add_argument('-d', '--dry', action='store_true', dest='doDryRun',
                        help='Dry run of result. Does not add requests to McM.')
    parser.add_argument('--dev', action='store_true', dest='useDev',
                        help='Use dev/test instance.')
    parser.add_argument('-l', '--lhe', action='store_true', dest='isLHErequest',
                        help='Check dataset when modifying requests. Fail and do not modify name if they conflict. Use for updating GS requests chained to wmLHE and pLHE requests.')
    parser.add_argument('-t', '--tags', action='append', dest='McMTags',
                        metavar='tags', help='Tags to append to request in McM.')

    args_ = parser.parse_args()
    return args_

def checkFile(file_):
    # Check that CSV file exists
    if not os.path.isfile(file_):
        print "Error: File {0} does not exist.".format(file_)
        sys.exit(1)

def checkPWG(pwg_):
    pwg_list = ['B2G', 'BPH', 'BTW', 'EGM', 'EWK', 'EXO', 'FSQ', 'FWD', 'HCA',
                'HIG', 'HIN', 'JME', 'L1T', 'MUO', 'QCD', 'SMP', 'SUS', 'TAU',
                'TOP', 'TRK', 'TSG']
    # Check that PWG is valid
    if pwg_ not in pwg_list:
        print "Error: {0} is not a recognized PWG.".format(pwg_)
        if pwg_ == 'XXX':
            print "Change the default value for flag -p to your PWG by modifying the variable defaultPWG on line 23."
        sys.stdout.write("Options are:")
        for iPWG in pwg_list:
            sys.stdout.write(" ")
            sys.stdout.write(iPWG)
        sys.stdout.write("\n")
        sys.exit(2)

def checkNotCreate(doModify_, cloneId_):
    # Check that script isn't being asked to both modify and clone a request
    doClone = False
    if cloneId_ != "":
        doClone = True
    if doModify_ and doClone:
        print "Error: cannot both --modify and --clone."
        sys.exit(6)
    return doModify_ or doClone # Return variable to use in fillFields()

def exitDuplicateField(file_in_, field_):
    print "Error: File {0} contains multiple instances of the field {1}".format(
        file_in_, field_)
    sys.exit(3)

def getFields(csvfile_):
    field_indices = {}
    field_candidates = ['name', 'dataset', 'mcdbid', 'cross section', 'events', 'fragment', 'time per event', 'size per event', 'tag', 'generator', 'campaign', 'sequences customize', 'gridpack', 'gridpack cards url', 'mcm tag', 'filter efficiency', "filter efficiency err", "match efficiency", "match efficiency err", "pwg", 'campaign', 'prepid', 'sequences customize', 'process string', 'notes', 'sequences beamspot', 'sequences magfield', 'jobid']

    synonym_list = {
        "dataset":["dataset name", "dataset"],
        "mcdbid":["eos", "mcdbid"],
        "cross section":['cross section [pb]', 'cross section (pb)', 'cross section', 'cs', 'cs [pb]', 'cs (pb)', 'xsec', 'xsec [pb]', 'xsec (pb)'],
        "events":['total events', 'events', 'number of events'],
        "fragment":['fragment name', 'generator fragment name', 'fragment'],
        "time per event":['time per event [s]', 'time per event', 'time per event (s)', 'time', 'time [s]', 'time (s)'],
        "size per event":['size per event [kb]', 'size per event', 'size per event (kb)', 'size', 'size [kb]', 'size (kb)'],
        "tag":['tag', 'fragment tag', 'sha', 'sha-1'],
        "generator":['generator', 'generators'],
        "campaign":['campaign', 'member of campaign'],
        "sequences customize":['sequences customise', 'sequences customize'],
        "gridpack":['gridpack location', 'gridpack'],
        "gridpack cards url":['gridpack cards url', 'cards url', 'gridpack cards location', 'cards location'],
        "mcm tag":['mcm tag', 'mcm tags'],
        "match efficiency":["match efficiency", "matching efficiency", "match eff", "matching eff"],
        "match efficiency err":["match efficiency err", "matching efficiency err", "match eff eff", "matching eff eff"],
    }

    # Process header row
    header = csv.reader(csvfile_).next()
    for ind, field in enumerate(header):
        field = field.lower()

        # Check for synonyms
        for field_rename, field_synonyms in synonym_list.iteritems():
            if field in field_synonyms:
                field = field_rename

        # Field is in the whitelist?
        if not field in field_candidates:
            raise ValueError("Unknown header field: {} in header {}".format(field, header))

        # Duplicate?
        if field in field_indices:
            raise ValueError("Duplicate header field: {} in header {}".format(field, header))

        field_indices[field] = ind

    return field_indices

def formatFragment(file_, campaign_):
    if len(file_.split("/")) > 2:
        return file_
    # 8TeV campaign
    elif campaign_ in ['Summer12']:
        return "Configuration/GenProduction/python/EightTeV/"+file_
    # 13 TeV campaigns
    elif campaign_ in ['Fall13', 'RunIIFall14GS', 'RunIIWinter15GS',
                       'RunIIWinter15wmLHE', 'RunIIWinter15pLHE',
                       'RunIISummer15GS', 'RunIISummer15wmLHEGS', 
                       'RunIIFall17GS', 'RunIIFall17pLHE', 'RunIIFall17wmLHEGS', 
                       'RunIIFall18GS', 'RunIIFall18pLHE', 'RunIIFall18wmLHEGS']:
        #return "Configuration/GenProduction/python/ThirteenTeV/Hadronizer/"+file_
        return "Configuration/GenProduction/python/ThirteenTeV/"+file_
    else:
        print "Error: Cannot determine energy of campaign {0}.".format(campaign_)
        sys.exit(5)

def fetchFragment(file_):
    try:
        if "http" in file_:
            url = file_
            print 'Fetching '+ url
            FragmentFetched = urllib2.urlopen(url).read()
            #print type(FragmentFetched)
            #print FragmentFetched.split("\n")[:10]
        elif "/afs/" in file_:
            FObject = open(file_,"r")
            FragmentFetched = FObject.read()
            FObject.close()
        else:
            print "The fragment must be located in github, giving full raw address, or in lxplus!!!"
            print file_
    except Exception, e:
        print e
        return None
    return FragmentFetched
    #return """ {0} """.format(FragmentFetched)

def createLHEProducer(gridpack, cards, fragment, tag):
    code = """import FWCore.ParameterSet.Config as cms

externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    args = cms.vstring('{0}'),
    nEvents = cms.untracked.uint32(5000),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh')
)""".format(gridpack)

    if cards != "":
        code += """

# Link to cards:
# {0}
""".format(cards)

    if fragment != "":
        #gen_fragment_url = "https://raw.githubusercontent.com/cms-sw/genproductions/{0}/{1}".format(
        #    tag, fragment.split("Configuration/GenProduction/")[1])
        gen_fragment_url = fragment
        #gen_fragment = urllib2.urlopen(gen_fragment_url).read()
        gen_fragment = fetchFragment(fragment)

        if "ExternalLHEProducer" in gen_fragment:
            raise ValueError("The analyzer fragment already has an ExternalLHEProducer. Please remove it before proceeding. Otherwise, the fragment will have two ExternalLHEProducers.")

        code += """
{0}

# Link to generator fragment:
# {1}
""".format(gen_fragment, gen_fragment_url)
    #if "\t" in code: 
    #print code#.split("\n")[:10]
    #print repr(code)
    return code

def fillFields(csvfile, fields, campaign, PWG, notCreate_, McMTags):
    requests = [] # List containing request objects
    num_requests = 0

    # Required fields
    #required_fields = ["fragment", "dataset", "events"]
    #for required_field in required_fields:
    #    if not required_field in fields:
    #        raise ValueError("Missing required field {}. Please make sure it's in the header.".format(required_field))

    for row in csv.reader(csvfile):
        if "fragment" in fields:
            if "http" in row[fields["fragment"]]:
                time.sleep(1)
                print num_requests % 15
                if num_requests % 15 == 14:
                    print "[fillFields] INFO : Sleeping to avoid HTTP Error 429: Too Many Requests"
                    time.sleep(20)
        if row[0].startswith("#"):
            continue
        num_requests += 1
        tmpReq = Request()

        # Set default values here, before parsing CSV file
        tmpReq.setKeepOutput(False)

        if "dataset" in fields:
            tmpReq.setDataSetName(row[fields["dataset"]])

        if "mcdbid" in fields:
            tmpReq.setMCDBID(row[fields["mcdbid"]])
        elif not notCreate_:
            # For some reason, MCM complains about wmLHEGS with negative MCDBID. 
            # David thinks there's a bug somewhere, but this should fix the problem.
            if campaign in ["RunIISummer15wmLHEGS", "RunIIFall17wmLHEGS", "RunIIFall18wmLHEGS"]:
                tmpReq.setMCDBID(0)
            else:
                tmpReq.setMCDBID(-1)
        if "cross section" in fields:
            tmpReq.setCS(row[fields["cross section"]])
        elif not notCreate_:
            tmpReq.setCS(1.0)

        if "events" in fields:
            tmpReq.setEvts(row[fields["events"]])
        if "campaign" in fields:
            campaign = row[fields["campaign"]]
            tmpReq.setCamp(campaign)
        elif campaign is not None:
            tmpReq.setCamp(campaign)

        if "fragment" in fields:
            #tmpReq.setFrag(formatFragment(row[fields[4]],campaign))
            fragment = fetchFragment(row[fields["fragment"]])
            if fragment:
                tmpReq.setMcMFrag(fragment)
            else:
                print "[fillFields] WARNING : Failed to get fragment " + row[fields["fragment"]] + "!"
                sys.exit(1)
            #tmpReq.setMcMFrag(createLHEProducer(row[fields[18]], "", row[fields[4]], "1"))
            #tmpReq.setFrag(formatFragment(row[fields[4]],campaign))

        if "time per event" in fields:
            tmpReq.setTime(row[fields["time per event"]])

        if "size per event" in fields:
            tmpReq.setSize(row[fields["size per event"]])

        if "tag" in fields:
            tmpReq.setTag(row[fields["tag"]])

        if "generator" in fields:
            tmpReq.setGen(row[fields["generator"]].split(" ")) # Multiple generators separated by spaces

        if "filter efficiency" in fields:
            tmpReq.setFiltEff(row[fields["filter efficiency"]])
        elif not notCreate_:
            tmpReq.setFiltEff(1.0)

        if "filter efficiency err" in fields:
            tmpReq.setFiltEffErr(row[fields["filter efficiency err"]])
        elif not notCreate_:
            tmpReq.setFiltEffErr(0.0)

        if "match efficiency" in fields:
            tmpReq.setMatchEff(row[fields["match efficiency"]])
        elif not notCreate_:
            tmpReq.setMatchEff(1.0)

        if "match efficiency err" in fields:
            tmpReq.setMatchEffErr(row[fields["match efficiency err"]])
        elif not notCreate_:
            tmpReq.setMatchEffErr(0.0)

        if "pwg" in fields:
            tmpReq.setPWG(row[fields["pwg"]])
        elif not notCreate_:
            tmpReq.setPWG(PWG)

        if "prepid" in fields:
            tmpReq.setPrepId(row[fields["prepid"]])

        if "sequences customize" in fields:
            tmpReq.setSequencesCustomise(row[fields["sequences customize"]])

        if "process string" in fields:
            tmpReq.setProcessString(row[fields["process string"]])
        if "gridpack" in fields:
            this_gridpack = row[fields["gridpack"]]
            if "gridpack cards url" in fields:
                this_gridpack_cards_url = row[fields["gridpack cards url"]]
            else:
                this_gridpack_cards_url = ""
            if "fragment" in fields:
                this_fragment = row[fields["fragment"]]
            else:
                this_fragment = ""
            if "tag" in fields:
                this_tag = row[fields["tag"]]
            else:
                this_tag = ""
            tmpReq.setMcMFrag(createLHEProducer(this_gridpack, this_gridpack_cards_url, this_fragment, this_tag))
        if "notes" in fields:
            tmpReq.setNotes(row[fields[20]])

        if "mcm tag" in fields:
            tmpReq.setMcMTag(row[fields[21]].split(" "))
        elif McMTags is not None:
            tmpReq.setMcMTag(McMTags)

        if "sequences beamspot" in fields:
            tmpReq.setSequencesBeamspot(row[fields[22]])
        if "sequences magfield" in fields:
            tmpReq.setSequencesMagField(row[fields[23]])
        requests.append(tmpReq)
    return requests, num_requests

def createRequests(requests, num_requests, doDryRun, useDev):
    # Create new requests based on campaign and PWG
    print "Is dev being used? ----------------------_> ", useDev
    mcm = McM(dev=useDev) # Get McM connection

    if not doDryRun:
        print "Adding {0} requests to McM.".format(num_requests)
    else:
        print "Dry run. {0} requests will not be added to McM.".format(
            num_requests)
    for reqFields in requests:
        if not reqFields.useCamp():
            print "A campaign is needed for new requests."
            continue

        # Create new request's dictionary
        new_req = {'pwg': reqFields.getPWG(),
                   'member_of_campaign': reqFields.getCamp(),
                   'mcdb_id': reqFields.getMCDBID()}
        # Fill dictionary with fields
        if reqFields.useDataSetName():
            new_req['dataset_name'] = reqFields.getDataSetName()
        if reqFields.useEvts():
            new_req['total_events'] = reqFields.getEvts()
        if reqFields.useMcMFrag():
            new_req['fragment'] = reqFields.getMcMFrag()
            #if type(new_req['fragment'])==type(reqFields.getMcMFrag()): print "Same type of McMFrag object is propagated"
            #if new_req['fragment']==reqFields.getMcMFrag(): print "Same McMFrag object is propagated"
        else:
            if reqFields.useFrag():
                new_req['name_of_fragment'] = reqFields.getFrag()
            if reqFields.useTag():
                new_req['fragment_tag'] = reqFields.getTag()
        if reqFields.useTime():
            new_req['time_event'] = reqFields.getTime()
        if reqFields.useSize():
            new_req['size_event'] = reqFields.getSize()
        if reqFields.useGen():
            new_req['generators'] = reqFields.getGen()
        if reqFields.useProcessString():
            new_req['process_string'] = reqFields.getProcessString()
        if reqFields.useNotes():
            new_req['notes'] = reqFields.getNotes()
        if reqFields.useMcMTag():
            new_req['tags'] = reqFields.getMcMTag()
        #print new_req
        
        if not doDryRun:
            #print "DEBUG 1 -----------------------> ", "Dictionary prepared:", new_req
            #pprint.pprint(new_req)
            answer = mcm.put('requests', new_req) # Create request
            #print "DEBUG 2 -----------------------> ", answer
            #print "DEBUG 3 -----------------------> ", answer['results']
            #print "DEBUG 4 -----------------------> ", answer['prepid']
            if not "results" in answer:
                print "Something is wrong! Here is the response from MCM:"
                print answer
                sys.exit(1)
            if answer['results']:
                # Cannot fill generator parameters while creating a new request
                # Modify newly created request with generator parameters
                # Get newly created request
                print "Succesfully created request:", answer['prepid']
                mcm = McM(dev=useDev)
                mod_req = mcm.get('requests', answer['prepid'])
                # Fill generator parameters
                mod_req['generator_parameters'][0]['cross_section'] \
                    = reqFields.getCS()
                mod_req['generator_parameters'][0]['filter_efficiency'] \
                    = reqFields.getFiltEff()
                mod_req['generator_parameters'][0]['filter_efficiency_error'] \
                    = reqFields.getFiltEffErr()
                mod_req['generator_parameters'][0]['match_efficiency'] \
                    = reqFields.getMatchEff()
                mod_req['generator_parameters'][0]['match_efficiency_error'] \
                    = reqFields.getMatchEffErr()
                if reqFields.useSequencesCustomise():
                    mod_req['sequences'][0]['customise'] = reqFields.getSequencesCustomise()
                if reqFields.useSequencesBeamspot():
                    mod_req['sequences'][0]['beamspot'] = reqFields.getSequencesBeamspot()
                if reqFields.useSequencesMagField():
                    mod_req['sequences'][0]['magField'] = reqFields.getSequencesMagField()
                # Update request with generator parameters and sequences
                update_answer = mcm.update('requests', mod_req)
                if update_answer['results']:
                    print "\033[0;32m{0} created\033[0;m".format(answer['prepid'])
                else:
                    print "\033[0;33m{0} created but generator parameters not set\033[0;m".format(
                        answer['prepid'])
            else:
                if reqFields.useDataSetname():
                    print "\033[0;31m{0} failed to be created\033[0;m".format(
                        reqFields.getDataSetName())
                else:
                    print "\033[0;31mA request has failed to be created\033[0;m"
        else:
            if reqFields.useDataSetName():
                print "\033[0;31m{0} not created\033[0;m".format(
                    reqFields.getDataSetName())
            else:
                print "\033[0;31mrequest not created\033[0;m"
            #pprint.pprint(new_req)

def modifyRequests(requests, num_requests, doDryRun, useDev, isLHErequest):
    # Modify existing request based on PrepId
    mcm = McM(dev=useDev) # Get McM connection

    if not doDryRun:
        print "Modifying {0} requests to McM.".format(num_requests)
    else:
        print "Dry run. {0} requests will not be modified in McM.".format(
            num_requests)
    for reqFields in requests:
        # Get request from McM
        if isLHErequest:
            if not reqFields.useDataSetName():
                print "\033[0;31mDataset name missing\033[0;m"
                continue
            elif not reqFields.useCamp():
                print "\033[0;31m{0} modification failed. Must provide campaign.\033[0;m".format(
                    reqFields.getDataSetName())
                continue
            query_string = "dataset_name={0}&member_of_campaign={1}".format(
                reqFields.getDataSetName(), reqFields.getCamp())
            failed_to_get = True
            for tries in range(3):
                time.sleep(0.1)
                mcm = McM(dev=useDev)
                mod_req_list = mcm.get('requests', query=query_string)
                if mod_req_list is not None:
                    failed_to_get = False
                    break
            if failed_to_get:
                print "\033[0;31m{0} modification failed. Could not get request from McM.\033[0;m".format(
                    reqFields.getDataSetName())
                continue
            if len(mod_req_list) > 1:
                print "\033[0;31m{0} modification failed. Too many requests match query.\033[0;m".format(
                    reqFields.getDataSetName())
                continue
            elif len(mod_req_list) == 0:
                print "\033[0;31m{0} modification failed. No requests match query.\033[0;m".format(
                    reqFields.getDataSetName())
                continue
            mod_req = mod_req_list[0]
        else:
            if not reqFields.usePrepId():
                print "\033[0;31mPrepId is missing.\033[0;m"
                continue
            time.sleep(0.1)
            mcm = McM(dev=useDev)
            mod_req = mcm.get('requests', reqFields.getPrepId())

        if reqFields.useDataSetName() and not isLHErequest:
            mod_req['dataset_name'] = reqFields.getDataSetName()
        if reqFields.useMCDBID():
            mod_req['mcdb_id'] = reqFields.getMCDBID()
        if reqFields.useEvts():
            mod_req['total_events'] = reqFields.getEvts()
        if reqFields.useMcMFrag():
            mod_req['fragment'] = reqFields.getMcMFrag()
            #mod_req['fragment'] = reqFields.getMcMFrag().replace('"""',"'")
        else:
            #print "Modifying non LHE requests"
            if reqFields.useFrag():
                mod_req['name_of_fragment'] = reqFields.getFrag()#.replace('"""',"'")
            if reqFields.useTag():
                mod_req['fragment_tag'] = reqFields.getTag()
        if reqFields.useTime():
            mod_req['time_event'] = [reqFields.getTime()]
            #print "Debugging update request: Time=", reqFields.getTime(), type(reqFields.getTime()), mod_req['time_event'], type(mod_req['time_event'])
        if reqFields.useSize():
            mod_req['size_event'] = [reqFields.getSize()]
            #print "Debugging update request: Size=", reqFields.getSize()
        if reqFields.useGen():
            mod_req['generators'] = reqFields.getGen()
        if (reqFields.useCS() or reqFields.useFiltEff()
            or reqFields.useFiltEffErr() or reqFields.useMatchEff()
            or reqFields.useMatchEffErr()):# and mod_req['generator_parameters'] == []:
            print "Resetting generator_parameters"
            mod_req['generator_parameters'] = [{'match_efficiency_error': 0.0,
                                                'match_efficiency': 1.0,
                                                'filter_efficiency': 1.0,
                                                'version': 0,
                                                'cross_section': 1.0,
                                                'filter_efficiency_error': 0.0}]
        if reqFields.useCS():
            mod_req['generator_parameters'][0]['cross_section'] \
                = reqFields.getCS()
        if reqFields.useFiltEff():
            mod_req['generator_parameters'][0]['filter_efficiency'] \
                = reqFields.getFiltEff()
        if reqFields.useFiltEffErr():
            mod_req['generator_parameters'][0]['filter_efficiency_error'] \
                = reqFields.getFiltEffErr()
        if reqFields.useMatchEff():
            mod_req['generator_parameters'][0]['match_efficiency'] \
                = reqFields.getMatchEff()
        if reqFields.useMatchEffErr():
            mod_req['generator_parameters'][0]['match_efficiency_error'] \
                = reqFields.getMatchEffErr()
        if reqFields.useSequencesCustomise():
            mod_req['sequences'][0]['customise'] \
                = reqFields.getSequencesCustomise()
        if reqFields.useSequencesBeamspot():
            mod_req['sequences'][0]['beamspot'] = reqFields.getSequencesBeamspot()
        if reqFields.useSequencesMagField():
            mod_req['sequences'][0]['magField'] = reqFields.getSequencesMagField()
        if reqFields.useProcessString():
            mod_req['process_string'] = reqFields.getProcessString()
        if reqFields.useNotes():
            mod_req['notes'] = reqFields.getNotes()
        if reqFields.useMcMTag():
            mod_req['tags'] += reqFields.getMcMTag()

        # Don't update if the local test job failed
        if mod_req['time_event'] == 0 or mod_req['size_event'] == 0:
            print "ERROR : For prepid {}, time_event={}, size_event={}. Skipping this request.".format(reqFields.getPrepId(), mod_req['time_event'], mod_req['size_event'])
            return
            
        #Avoiding to have unset generator parameters
        if mod_req['generator_parameters'][0]['cross_section'] < 0: mod_req['generator_parameters'][0]['cross_section'] = 1.0
        if mod_req['generator_parameters'][0]['filter_efficiency'] < 0: mod_req['generator_parameters'][0]['filter_efficiency'] = 1.0
        if mod_req['generator_parameters'][0]['filter_efficiency_error'] < 0: mod_req['generator_parameters'][0]['filter_efficiency_error'] = 0.0
        if mod_req['generator_parameters'][0]['match_efficiency'] < 0: mod_req['generator_parameters'][0]['match_efficiency'] = 1.0
        if mod_req['generator_parameters'][0]['match_efficiency_error'] < 0: mod_req['generator_parameters'][0]['match_efficiency_error'] = 0.0

        if not doDryRun:
            #mod_req['fragment']=mod_req['fragment'].replace('"""',"'")
            answer = mcm.update('requests', mod_req) # Update request
            #print "mod_req object: ", mod_req
            #print "Debugging update request: McM_Answer=", answer
            if answer['results']:
                if not isLHErequest:
                    print "\033[0;32m{0} modified\033[0;m".format(
                        reqFields.getPrepId())
                else:
                    print "\033[0;32m{0} in {1} modified\033[0;m".format(
                        reqFields.getDataSetName(), reqFields.getCamp())
            else:
                if not isLHErequest:
                    print "\033[0;31m{0} failed to be modified\033[0;m".format(
                        reqFields.getPrepId())
                else:
                    print "\033[0;31m{0} failed to be modified\033[0;m".format(
                        reqFields.getDataSetName())
        else:
            if not isLHErequest:
                print "\033[0;31m{0} not modified\033[0;m".format(
                    reqFields.getPrepId())
                pprint.pprint(mod_req)
            else:
                print "\033[0;31m{0} not modified\033[0;m".format(
                    reqFields.getDataSetName())
                pprint.pprint(mod_req)


def cloneRequests(requests, num_requests, doDryRun, useDev, cloneId_):
    # Create new requests be cloning an old one based on PrepId
    mcm = McM(dev=useDev) # Get McM connection

    if not doDryRun:
        print "Adding {0} requests to McM using clone.".format(num_requests)
    else:
        print "Dry run. {0} requests will not be added to McM using clone.".format(
            num_requests)
    for reqFields in requests:
        mcm = McM(dev=useDev)
        clone_req = mcm.get('requests', cloneId_) # Get request to clone
        if reqFields.useDataSetName():
            clone_req['dataset_name'] = reqFields.getDataSetName()
        if reqFields.useMCDBID():
            clone_req['mcdb_id'] = reqFields.getMCDBID()
        if reqFields.useEvts():
            clone_req['total_events'] = reqFields.getEvts()
        if reqFields.useMcMFrag():
            clone_req['fragment'] = reqFields.getMcMFrag()
        else:
            if reqFields.useFrag():
                clone_req['name_of_fragment'] = reqFields.getFrag()
            if reqFields.useTag():
                clone_req['fragment_tag'] = reqFields.getTag()
        if reqFields.useTime():
            clone_req['time_event'] = reqFields.getTime()
        if reqFields.useSize():
            clone_req['size_event'] = reqFields.getSize()
        if reqFields.useGen():
            clone_req['generators'] = reqFields.getGen()
        if reqFields.useCS():
            clone_req['generator_parameters'][0]['cross_section'] \
                = reqFields.getCS()
        if reqFields.useFiltEff():
            clone_req['generator_parameters'][0]['filter_efficiency'] \
                = reqFields.getFiltEff()
        if reqFields.useFiltEffErr():
            clone_req['generator_parameters'][0]['filter_efficiency_error'] \
                = reqFields.getFiltEffErr()
        if reqFields.useMatchEff():
            clone_req['generator_parameters'][0]['match_efficiency'] \
                = reqFields.getMatchEff()
        if reqFields.useMatchEffErr():
            clone_req['generator_parameters'][0]['match_efficiency_error'] \
                = reqFields.getMatchEffErr()
        if reqFields.useSequencesCustomise():
            clone_req['sequences'][0]['customise'] \
                = reqFields.getSequencesCustomise()
        if reqFields.useSequencesBeamspot():
            clone_req['sequences'][0]['beamspot'] = reqFields.getSequencesBeamspot()
        if reqFields.useSequencesMagField():
            clone_req['sequences'][0]['magField'] = reqFields.getSequencesMagField()
        if reqFields.useProcessString():
            clone_req['process_string'] = reqFields.getProcessString()
        if reqFields.useNotes():
            clone_req['notes'] = reqFields.getNotes()
        if reqFields.useMcMTag():
            clone_req['tags'] += reqFields.getMcMTag()

        if not doDryRun:
            answer = mcm.clone(cloneId_, clone_req) # Clone request
            if answer['results']:
                print "\033[0;32m{0} created using clone\033[0;m".format(
                    answer['prepid'])
            else:
                if reqFields.useDataSetName():
                    print "\033[0;31m{0} failed to be created using clone\033[0;m".format(
                        reqFields.getDataSetName())
                else:
                    print "\033[0;31mrequest failed to be created using clone\033[0;m"
        else:
            if reqFields.useDataSetName():
                print "\033[0;31m{0} not created using clone\033[0;m".format(
                    reqFields.getDataSetName())
            else:
                print "\033[0;31mrequest not created using clone\033[0;m"
            pprint.pprint(clone_req)

def main():
    args = getArguments() # Setup flags and get arguments
    checkPWG(args.pwg) # Make sure PWG is an actual PWG
    # Check that script is not asked to both modify and clone
    # Store variable that is true if script is asked to modify or clone
    notCreate = checkNotCreate(args.doModify, args.cloneId)
    checkFile(args.file_in) # Ensure CSV file exists

    if args.useDev:
        print "Using dev/test instance."

    csvfile = open(args.file_in, 'r') # Open CSV file
    fields = getFields(csvfile) # Get list of field indices
    # Fill list of request objects with fields from CSV and get number of requests
    requests, num_requests = fillFields(csvfile, fields, args.campaign,
                                        args.pwg, notCreate, args.McMTags)

    if args.doModify:
        # Modify existing requests
        modifyRequests(requests, num_requests, args.doDryRun, args.useDev,
                       args.isLHErequest)
    elif args.cloneId != "":
        # Create new requests using clone
        cloneRequests(requests, num_requests, args.doDryRun, args.useDev,
                      args.cloneId)
    else:
        # Create new requests
        createRequests(requests, num_requests, args.doDryRun, args.useDev)

if __name__ == '__main__':
    main()
