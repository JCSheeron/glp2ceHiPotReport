#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# glpCreateReport.py
#
# This program is intended to be used to create reports from data export from a
# Schleich GLP2-ce Hi Pot Modular Tester. ("tester").
# This program will import a data from a file exported by the tester. It will
# create a PDF file. The PDF file will contain numerical data in easy to read
# format, and it will also plot the data.
#
# **** Program operation
#   1)  The program will read in a config file. The file is either specified by
#       the -c/--configFile command line argument, or defaults to config.ini if not
#       specified.  The config file specifies:
#           a. The data file path
#           b. The test definition path
#
#   2)  The program will read in one or more test files from the test definition
#       path specified in the config file.  If a file is specified by the
#       -t/--testDfnFile command line option, then this file will be searched
#       for and loaded. If this file is not present, an error will result. If no
#       file is specified, then all the test definitions (*.TPR) will be loaded, and
#       the test data will determine which to use (below) by searching for the
#       proper test id.
#
#   3)  The program will read in and parse one or more data files from the data
#       path specified in the config file. If a file is specified by the
#       -d/--dataFile command line option, then this file will be loaded and
#       used.  If this file is not present, an error will result. If no file
#       specified, then all the data files (*.csv) will be loaded.
#
#   4)  Once one or more data files are loaded, the program will ensure that it
#       has available to it (from step 2), the corresponding test definition. The
#       test ID is used.
#
#   5)  TODO: What else
#
# TODO: More info about the input file format.
# TODO: More info about the text data in the output PDF.
# TODO: More info about the plot in the output PDF.
#
# Specified is the input data file and the name of the PDF file created.
# TODO: What else is specified?
#
# imports
# date and time stuff
from datetime import datetime, time

# os file related
# join combines path strings in a smart way (i.e. will insert '/' if missing,
# or remove a '/' if a join creates a repeat.
from os.path import join, splitext

# config file parser
import configparser

# arg parser
import argparse

# csv file stuff
import csv

# numerical manipulation libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt # for plotting
#import matplotlib.font_manager as fontmgr # for managing fonts

# pdf creation
from fpdf import FPDF
# pdf manipulation
from PyPDF2 import PdfFileMerger, PdfFileReader

# for default dictionary
from collections import defaultdict

# user libraries
# Note: May need PYTHONPATH (set in ~/.profile?) to be set depending
# on the location of the imported files
from bpsFile import listFiles
from bpsCPdf import cPdf
from bpsPrettyPrint import listPrettyPrint2ColStr

# specialized libraries unlikely to be used elsewhere. These should
# travel with this file.
from Glp2TestDfn import Glp2TestDfn
from Glp2TestData import Glp2TestData
# NOTE: The helper function MakeTestList in GlpFunctions requires ordered-set
# which normally needs to be installed.
from Glp2Functions import MakeTestList, MakePdfDfnStepRow, MakePdfDataStepRow
from Glp2Functions import PlotTvsVandI as plotVI
from Glp2GraphData import Glp2GraphData

# **** argument parsing
# define the arguments
# create an epilogue string to further describe the input file
# TODO: Complete the below description.
eplStr="""Python program to create a PDF report from a data export file from
a Schleich GLP2-ce Hi Pot Modular Tester."""

descrStr="""Python program to create a PDF report from a data export file from
a Schleich GLP2-ce Hi Pot Modular Tester. """

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, \
                                 description=descrStr, epilog=eplStr)
parser.add_argument('-of', '--outputFilePrefix', default=None,
                    help= 'Optional. Output prefix for PDF file names. The .pdf \
extension will be added to the file name if not specified. If no prefix is specified \
no output files will be created.')
parser.add_argument('-d', '--dataFile', default='', metavar='', \
                    help='Input data file (Schleich GLP2-ce file, *.csv). If \
specified, this data file will be used. If not specified, all *.csv files present \
in the data_dir path specified in the config directory will be used.')
parser.add_argument('-de', '--dataFileEncoding', default='UTF-16', metavar='', \
                    help='Data file encoding. Default is UTF-16.')
parser.add_argument('-dirPrefix', default='', metavar='', \
                    help='Directory prefix. If specified, this is prepended to \
the paths specified in the configuration ini file (default is config.ini). This is \
helpful if the data is inside directories that are named using serial numbers, \
dates, times, test numbers, station numbers, or some other dynamic data that is \
not known when the configuration file is created.')
parser.add_argument('-c', '--configFile', default='config.ini', metavar='', \
                   help='Config file. Default is config.ini. A list of files \
may be specified ([\'file1.ini\',\'file2.ini\',...]) if the configuration is \
spread across multiple files. The resulting configuration will be a union of the \
information, so if keys are repeated, the key will have the value it had in the \
last file read.')
parser.add_argument('-ce', '--configEncoding', default='UTF-8', metavar='', \
                   help='Config file encoding. Default is UTF-8.')
parser.add_argument('-t', '--testDfnFile', default='', metavar='', \
                   help='Test definition file (*.TPR). If specified, this and only \
this test definition is used. If not specified, all *.TPR files in the test_dfn_dir \
will be considered.  A proper data file will include a test definition id. In \
either case (specified or not), the test id must match test id in the data file. \
In the non-specified case, any files present will be searched until the test id \
in the data is found in one of the test definition files.')
parser.add_argument('-te', '--testDfnEncoding', default='UTF-16', metavar='', \
                   help='Test definition file encoding. Default is UTF-16.')
parser.add_argument('-v', '--verbose', action='store_true', default=False, \
                    help='Verbose output, usually used for troubleshooting.')
# parse the arguments
args = parser.parse_args()

# At this point, the arguments will be:
# Argument          Values       Description
# args.outputFilePrefix string   Optional. Output file name prefix. No output
#                                files are cretated if not specified.
# args.dataFile         string   Input file name. Optional. Data directory in
#                                config file will be searched if a file is not
#                                specified.
# args.dataFileEncoding string   Optional. Default is UTF-16
# args.dirPrefix        string   Optional. Prepended to directory path specified
#                                in config file.
# args.configFile       string   Optional. Default 'config.ini'
# args.configEncoding   string   Optional. Default 'UTF-8'
# args.testDfnFile      string   Optional. Test Definition File. If a file is
#                                not specified, all *.TPR files in the path
#                                specified in the config file will be considered.
# args.testDfnEncoding  string   Optional. Default 'UTF-16'. The tester uses
#                                UTF-16 encoding when creating these definition
#                                files.
# args.verbose          True/False, default False. Increase output messages.

# Put the begin mark here, after the arg parsing, so argument problems are
# reported first.
print('**** Begin Processing ****')
# get start processing time
procStart = datetime.now()
print('    Process start time: ' + procStart.strftime('%m/%d/%Y %H:%M:%S'))

# **** Get config info from config file
# bring in config data from config.ini by default or from file specified
# with -c argument
config = configparser.ConfigParser()
cfgFile = config.read(args.configFile)
# bail out if no config file was read
if not cfgFile:
    print('ERROR: The configuration file: ' + args.configFile + ' was not found. Exiting.')
    quit()
# if we get here, we have config data
if args.verbose:
    print('\nThe following config file(s) are used:')
    print(cfgFile)
    print('The resulting configuration has these settings:')
    for section in config:
        print(section)
        for option in config[section]:
            print('  ', option, ':', config[section][option])
# set the data paths to use internally
if args.dirPrefix is not None:
    testDataPath = join(args.dirPrefix, config['Paths']['common_dir'], config['Paths']['data_dir'])
    testDfnPath = join(args.dirPrefix, config['Paths']['common_dir'], config['Paths']['test_dfn_dir'])
else:
    testDataPath = join(config['Paths']['common_dir'], config['Paths']['data_dir'])
    testDfnPath = join(config['Paths']['common_dir'], config['Paths']['test_dfn_dir'])

# construct a message to detail files used.  Use for pdf and verbose output.
# TODO: Insert PDF Bold 'section' heading
fileMsg  = '\nThe following paths are searched for test definition and test data files:'
fileMsg += '\n{:22}{}'.format('Test Data Path: ',testDataPath)
fileMsg += '\n{:22}{}'.format('Test Definition Path: ', testDfnPath)

# get the decimal separator from the file, or use the default of a ',' (the euro way)
if config.has_option('TestData', 'decimalSeparator'):
    decimalSeparator = config['TestData']['decimalSeparator']
else:
    decimalSeparator = ','

# **** Figure out what test definition file to use, and load it (or them!!)
# Get a list of test definition files in the test definition path
testDfnNames = listFiles(testDfnPath)
testDfns = [] # definition holding spot

# TODO: Insert PDF Bold 'section' heading
fileMsg += '\n\nThe following Test Definition files were found:'
fileMsg += listPrettyPrint2ColStr(testDfnNames, 40)

# If a test definition file was specified, see if it was found. If not, error out.
# If no test definition file was specified, load them all, and look for the correct id later
if args.testDfnFile != '' and args.testDfnFile is not None and not args.testDfnFile in testDfnNames:
    # Test dfn file specified, but not found. Print message and leave.
    print('\nERROR: The test definition file \'' + args.testDfnFile + '\' was specified, \
but was not found. Exiting.')
    quit()
elif args.testDfnFile != '' and args.testDfnFile is not None and args.testDfnFile in testDfnNames:
    # Test dfn file specified, and found. Print message and load into a 1 element list. Save the
    # message for use in the PDF output (later).
    # This message will be printed as part of the verbose output also, so only print it here if
    # verbose is not selected.
    partMsg = '\n\nSpecified test definition file \'' + args.testDfnFile + '\' was found and is being used.'
    fileMsg += partMsg
    if not args.verbose:
        print(partMsg)
    try:
        testDfns.append(Glp2TestDfn(args.testDfnFile, join(testDfnPath, args.testDfnFile),
                                    args.testDfnEncoding))
        # convert to a tuple to prevent change
        testDfns = tuple(testDfns)
    except UnicodeError as  ue:
        print('Unicode Error: Unable to load test definition file: ' + args.testDfnFile +
            '. Check encoding. ' + args.testDfnEncoding + ' was expected.')
        print(ue)
        quit()
elif args.testDfnFile == '' or args.testDfnFile is None:
    # Test dfn file not specified. Print message and load all the definitions into a list. Save the
    # message for use in the PDF output (later).
    # This message will be printed as part of the verbose output also, so only print it here if
    # verbose is not selected.
    partMsg = '\n\nThere was no test definition file specified.  The test definition id in the \
data will be used to try and determine the correct test definition file to use.'
    fileMsg += partMsg
    if not args.verbose:
        print(partMsg)

    # For each definition file name, create and append a Glp2TestDfn object.
    # Exclude files starting with '.', or files that don't end with '*.tpr' (case insensitive)
    # The no starting dot filters out hidden or locked files, and the .tpr
    # requirement at the end means that only *.tpr files are considered.
    for dfnName in testDfnNames:
        if not dfnName.startswith('.') and dfnName.lower().endswith('.tpr'):
            try:
                testDfns.append(Glp2TestDfn(dfnName, join(testDfnPath, dfnName), args.testDfnEncoding))
            except UnicodeError as  ue:
                print('Unicode Error: Unable to load test definition file: ' + dfnName +
                '. Check encoding. ' + args.testDfnEncoding + ' was expected.')
                print(ue)
    # if we get here, we should have a list of test definitions.
    # convert to a tuple to prevent change
    testDfns = tuple(testDfns)

# At this point, testDfns is a tuple containing the test definitions to consider

# **** Figure out what test data file to use, and load it (or them!!)
# Get a list of test data files in the data path
testDataNames = listFiles(testDataPath)

# TODO: Insert PDF Bold 'section' heading
fileMsg += '\n\nTest following Test Data files were found:'
fileMsg += listPrettyPrint2ColStr(testDataNames, 40)

# If a test data file was specified, see if it was found. If not, error out.
# If no test data file was specified, load them all, so they can all be processed.
if args.dataFile != '' and args.dataFile is not None and not args.dataFile in testDataNames:
    # Test data file specified, but not found. Print message and leave.
    print('\nERROR: The test data file \'' + args.dataFile + '\' was specified, \
but was not found. Exiting.')
    quit()
elif args.dataFile != '' and args.dataFile is not None and args.dataFile in testDataNames:
    # Test data file specified, and found. Print message and load into a 1 element list. Save
    # the message for use in the pdf (later).
    # This message will be printed as part of the verbose output also, so only print it here if
    # verbose is not selected.
    partMsg = '\n\nSpecified test data file \'' + args.dataFile + '\' was found and is being used.'
    fileMsg += partMsg
    if not args.verbose:
        print(partMsg)
    # **** read the csv file into a data frame.  The first row is treated as the header
    try:
        with open(join(testDataPath, args.dataFile), mode='r', encoding=args.dataFileEncoding) as dataCsvFile:
            tests = MakeTestList(args.dataFile,
                                 csv.reader(dataCsvFile, delimiter = ';'),
                                 decimalSeparator)

    except UnicodeDecodeError as ude:
        print('Unicode Error: Unable to load test data file: ' + args.dataFile +
            '. Check encoding. ' + args.dataFileEncoding + ' was expected.')
        print(ude)
        quit()

elif args.dataFile == '' or args.dataFile is None:
    # Test data file not specified. Load all those found.  Save message for pdf use (later).
    # This message will be printed as part of the verbose output also, so only print it here if
    # verbose is not selected.
    # TODO: Insert PDF Bold 'section' heading
    partMsg = '\n\nThere was no test data file specified.  All data files found will be \
processed. File names starting with a \'.\', or files that don\'t end with \'*.csv\' will \
be ignored. This is to filter out hidden or locked files, or other file types.'
    fileMsg += partMsg
    if not args.verbose:
        print(partMsg)
    tests = [] # this will be a list of found test data objects.
    for fileName in testDataNames:
        # For each data file name, make a list of Glp2TestData objects
        # Exclude files starting with '.', or files that don't end with '*.csv'
        # The no starting dot filters out hidden or locked files, and the .csv
        # requirement at the end means that only *.csv files are considered.
        if not fileName.startswith('.') and fileName.lower().endswith('.csv'):
           # file should be considered test data
            try:
                with open(join(testDataPath, fileName), mode='r', encoding=args.dataFileEncoding) as dataCsvFile:
                    fileTestList = MakeTestList(fileName,
                                                csv.reader(dataCsvFile, delimiter = ';'),
                                                decimalSeparator)

            except UnicodeDecodeError as ude:
                print('Unicode Error: Unable to load test data file: ' + args.dataFile +
                    '. Check encoding. ' + args.dataFileEncoding + ' was expected.')
                print(ude)
                quit()
            # If we get here, we have a partial list of test objects from the file
            # processed.  Use tests[] to accumulate all of them from all files.
            tests.extend(fileTestList) # list.append appends an object, list.extend appends elements.

# If we get here, tests[] contains all the test data from one or more test data (*.csv) files.
# Convert it to a tuple to prevent bugs from changing it.
tests = tuple(tests)

# Now the file related finding, loading, listing, and other early tasks
# are done. Print the verbose message about them if requested.
if args.verbose:
    print(fileMsg)

# **** Link the test data with the test definition
# At this point we have the test definitions loaded in the testDfns(...) tuple,
# and the test data loaded in the tests(...) tuple.
# Use the GUIDs to link the two. Loop through the test data tuple, get the
# test dfn guid, and then match this guid with a test definition file.
# Pair the two up, and process them.
#
# Make a tuple of (test index, test definition index) matching pairs (prt_tDfn)
prt_tDfn=[]
# Also keep track of test data without a test definition, and for test
# definitions for which there is no data. (tDfnMatch and dfnTMatch)
# Init a list where the index position represents a test or definition index position.
# After the loop, any False values are indexes without matches
tDfnMatch=[False] * len(tests) # list of test data <-> test definition matches by position
dfnTMatch=[False] * len(testDfns) # list of test definition <-> test data matches by position
# Lastly, for informational (display) purposes, make a list of test definitions used
# in each data file -- this will be a dictionary of sets with the data file
# name being the dictionary key (fnVsDfn). A set is used so duplicates are automatically eliminated.
# A duplicate, for example, would exist whenever a data file contains several test runs using the
# same test definition.
fnVsDfn=defaultdict(set)
for tidx, test in enumerate(tests):
    # associate tests with definitions and keep track of orphaned test data and definitions.
    for didx, dfn in enumerate(testDfns):
        if test.getTestProgramGuid() == dfn.dfnGuid:
            # match found. Create pair and set the flags.
            prt_tDfn.append((tidx, didx))
            tDfnMatch[tidx] = True
            dfnTMatch[didx] = True
    # populate the file name dictionary
    fnVsDfn[test.fileName].add(test.getTestProgramName())
# now convet the list to a tuple
prt_tDfn = tuple(prt_tDfn)

# **** Create a string used for the pdf output about test data files and
# test definitions.
dataDfnAssocMsg = '\nEach data file may contain test data for multiple tests. Each \
test is associated with a particular test definition. For the data files processed \
(see above), there is test data for ' + str(len(tests)) + ' test'
# account for plural tests
if len(tests) > 1:
    dataDfnAssocMsg += 's.'
else:
    dataDfnAssocMsg += '.'

dataDfnAssocMsg += '\n\nIn the test data, the following associations were found \
between data file names and test definitions:'
# print the file vs dfn associations
for fn, dfns in fnVsDfn.items():
    dataDfnAssocMsg += '\n\n' + fn
    if dfns:
        # if there are definitions associated with the file
        for dfn in dfns:
            dataDfnAssocMsg += '\n    ' + dfn
    else:
        # no definitions associated with the file
        # I don't think it is possible to get here, but just for safety
        dataDfnAssocMsg += '    (no definitions associated with this file)'

# Make a list of test data indexes with no definition
tNoDef = [tidx for tidx, val in enumerate(tDfnMatch) if not val]
# Message if there is any test data without a found definition
if tNoDef:
    # TODO: Insert PDF Bold 'section' heading
    tNoDefMsg = '\n\nThere is test data that is associated with one or more test \
definitions that are not found. This is usually because the definition was \
deleted after it was used to run a test.\n\nNote that internal identification \
numbers are used, rather than names, to uniquely identify test definitions. \
This means that this condition can occur, for example, when a (new) test \
definition is given the same name as a previously deleted test definition \
that was used to run a test. In this case, the data will still contain the \
identification number of the old test definition, and even though the new test \
definition has the same name, the new test definition will not be associated \
with the previously run test.\n\nThere is no test definition found for the following '
    # accommodate singular or plural in the message
    if len(tNoDef) == 1:
        tNoDefMsg += 'test:'
    else:
        tNoDefMsg += str(len(tNoDef)) + ' tests:'

    for testIdx in tNoDef:
        tNoDefMsg += '\n\nFile Name: ' + tests[testIdx].fileName
        tNoDefMsg += '\n    Program Name: ' + tests[testIdx].getTestProgramName()
        tNoDefMsg += '\n    Test number: ' + str(tests[testIdx].testInstanceId)

# Make a list of test definition indexes with no test data.
defNoT = [didx for didx, val in enumerate(dfnTMatch) if not val]
# Message if there are any unused test definitions.
if defNoT:
    # TODO: Insert PDF Bold 'section' heading
    defNoTMsg = '\n\nThere are test definitions found that were not used for any \
of the test data. This is not an indication of a problem. It simply means that \
a test is defined that was not used when running any of the test for which there \
is test data.  It is being reported for information only.\n\nThe following test \
definitions are not used in any of the test data:'
    for defIdx in defNoT:
        defNoTMsg += '\n\nFile Name: ' + testDfns[defIdx].fileName
        defNoTMsg += '\n    Definition Name: ' + testDfns[defIdx].name
        defNoTMsg += '\n    Programmer: ' + testDfns[defIdx].nameOfProgrammer

# **** Put the information about test definitions and test data associations in
# a pdf.
# First print it to the terminal if verbose argument is used.
if args.verbose:
    print(dataDfnAssocMsg)
    print(tNoDefMsg)
    print(defNoTMsg)

# Make the data associaiton pdf if an output prefix is specified.
if args.outputFilePrefix is not None:
    fnameData= '__zzqq__tempPdf_dataAssoc__zzqq__.pdf' # not likely to exist and be something else
    # Units are in points (pt)
    dataAssocPdf = cPdf(orientation = 'P', unit = 'pt', format='Letter',
                        headerText='Test Definition and Test Data Associations')
    # define the nb alias for total page numbers used in footer
    #dataAssocPdf.alias_nb_pages() # Enable {nb} magic: total number of pages used in the footer
    dataAssocPdf.set_margins(54, 72, 54) # left, top, right margins (in points)

    # Set the font for the main content
    # use the bold proportional font
    if dataAssocPdf.fontNames[0] != dataAssocPdf.defaultFontNames[0]:
        # non-default
        dataAssocPdf.set_font("regularMono", '', 10)
    else:
        # default
        dataAssocPdf.set_font(dataAssocPdf.defaultFontNames[0], '', 10)

    # add the content put into outputMsg above
    dataAssocPdf.add_page() # use ctor params
    dataAssocPdf.multi_cell(w=0, h=13,
                            txt=fileMsg + dataDfnAssocMsg + tNoDefMsg + defNoTMsg,
                            border=0, align='L', fill=False)
    dataAssocPdf.output(name = fnameData, dest='F')

# **** If an output file prefix is specified, for each (test, test definition) 
# pair, make a pdf of:
#   The test definition
#   The test results (tabular)
#   The test results (graph)
if args.outputFilePrefix is not None:
    for tIdx, dfnIdx in prt_tDfn:
        # Instantiate the extended pdf cVlass and get on with making the pdf
        # Units are in points (pt)
        headerText = '{}          {} {}'.format('Test Data','File Name:', tests[tIdx].fileName)
        pdf = cPdf(orientation = 'P', unit = 'pt', format='Letter', headerText=headerText)
        # define the nb alias for total page numbers used in footer
        pdf.alias_nb_pages() # Enable {nb} magic: total number of pages used in the footer
        pdf.set_margins(54, 68, 54) # left, top, right margins (in points)
        # add a page to be able to add content
        pdf.add_page() # use ctor params
        textHeight = pdf.font_size
        # calc the effective page width, epw, and the 'unit' cell width.
        # colwidth is somewhat arbitrary, but picked to be a convenient size
        epw = pdf.w - (pdf.l_margin + pdf.r_margin)
        colWidth = epw/6.0
        # create pdf file name from test data file name and use indexes to make it unique
        # TODO: think of a better file name?
        fname= 'TestData_' + splitext(tests[tIdx].fileName)[0] + '_' + str(tIdx) + '_' + str(dfnIdx) + '.pdf'
        # Insert a bold section heading for the definition
        if pdf.fontNames[3] != pdf.defaultFontNames[3]:
            # non-default
            pdf.set_font("boldProp", 'B')
        else:
            # default
            pdf.set_font(pdf.defaultFontNames[3], 'B')
        pdf.cell(epw, textHeight * 1.2, 'Test Definition', border = 0)
        # Reset back to regular weight, mono spaced
        if pdf.fontNames[0] != pdf.defaultFontNames[0]:
            # non-default
            pdf.set_font("regularMono", '')
        else:
            # default
            pdf.set_font(pdf.defaultFontNames[0], '')
        pdf.ln(textHeight)
        #
        # test definition data, but include test data file name in the beginning
        # to help make it clear where/why this definition is being used
        testDfnMsg  = '\n{} {}'.format('Program Name:', testDfns[dfnIdx].name)
        testDfnMsg += '\n{} {}'.format('Programmer:', testDfns[dfnIdx].nameOfProgrammer)
        testDfnMsg += '\n{} {}'.format('File Name:', testDfns[dfnIdx].fileName)
        testDfnMsg += '\n{} {}\n\n'.format('Comments:', testDfns[dfnIdx].generalComments)
        # Add the test dfn data to the pdf
        pdf.multi_cell(w=0, h=13, txt=testDfnMsg, border=0, align='L', fill=False )
        # add the definition steps to the pdf
        for step in testDfns[dfnIdx]._steps:
            MakePdfDfnStepRow(pdf, step)
        # Test Data
        # Insert a bold section heading for the test data
        if pdf.fontNames[3] != pdf.defaultFontNames[3]:
            # non-default
            pdf.set_font("boldProp", 'B')
        else:
            # default
            pdf.set_font(pdf.defaultFontNames[3], 'B')
        pdf.cell(epw, textHeight * 1.2, 'Test Data', border = 0)
        # Reset back to regular weight, mono spaced
        if pdf.fontNames[0] != pdf.defaultFontNames[0]:
            # non-default
            pdf.set_font("regularMono", '')
        else:
            # default
            pdf.set_font(pdf.defaultFontNames[0], '')
        pdf.ln(textHeight)
        testDataMsg  = '\n{} {}'.format('Program Name:', tests[tIdx].testProgramName)
        testDataMsg += '\n{} {}'.format('Device S/N:', tests[tIdx].deviceNumber)
        testDataMsg += '\n{} {}\n'.format('Operator:', tests[tIdx].operator)
        # add the test data to thd pdf
        pdf.multi_cell(w=0, h=13, txt=testDataMsg, border=0, align='L', fill=False )
        # add the data steps to the pdf
        for step in tests[tIdx]._steps:
            MakePdfDataStepRow(pdf, step)
        # writ the pdf to a file
        pdf.output(name = fname, dest='F')

## **** Parse & Process the graph data
grphObject = Glp2GraphData(tests[0]._steps[0].graphData)
print(tests[0].fileName)
plotVI(tData = grphObject.getAxisData(0),
       vData = grphObject.getAxisData(2),
       iData = grphObject.getAxisData(1),
       iThreshold = 0.1)

##
# TODO: Create a graph (MatPlotLib)
#
# TODO: Create a PDF with the text and graph output

# get end processing time
procEnd = datetime.now()
print('\n**** End Processing ****')
print('    Process end time: ' + procEnd.strftime('%m/%d/%Y %H:%M:%S'))
print('    Duration: ' + str(procEnd - procStart) + '\n')

