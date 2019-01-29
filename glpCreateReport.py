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
#
# date and time stuff
from datetime import datetime, time

# os file related
# join combines path stirngs in a smart way (i.e. will insert '/' if missing,
# or remove a '/' if a join creates a repeat.
from os.path import join

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
import matplotlib.font_manager as fontmgr # for managing fonts

# pdf creation
from fpdf import FPDF
# pdf manipulation
from PyPDF2 import PdfFileMerger, PdfFileReader

# user libraries
# Note: May need PYTHONPATH (set in ~/.profile?) to be set depending
# on the location of the imported files
from bpsFile import listFiles

# sepcialized libraties unlikely to be used elsewhere. These should
# travle with this file.
from Glp2TestDfn import Glp2TestDfn
from Glp2TestData import Glp2TestData

# **** argument parsing
# define the arguments
# create an epilog string to further describe the input file
# TODO: Complete the below description.
eplStr="""Python program to create a PDF report from a data export file from
a Schleich GLP2-ce Hi Pot Modular Tester."""

descrStr="""Python program to create a PDF report from a data export file from
a Schleich GLP2-ce Hi Pot Modular Tester. """

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, \
                                 description=descrStr, epilog=eplStr)
parser.add_argument('outputFile', help= 'Output PDF file name. The .pdf extension \
will be added to the file name if not specified.')
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
spread across multiple files. The resuling configuration will be a union of the \
information, so if keys are repeated, the key will have the value it had in the \
last file read.')
parser.add_argument('-ce', '--configEncoding', default='UTF-8', metavar='', \
                   help='Config file encoding. Default is UTF-8.')
parser.add_argument('-t', '--testDfnFile', default='', metavar='', \
                   help='Test definition file (*.TPR). If specified, this and only \
this test definition is used. If not specified, all *.TPR files in the test_dfn_dir \
will be considered.  A proper data file will include a test definiton id. In \
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
# args.outputFile       string   Output file name. Required.
# args.dataFile         string   Input file name. Optional. Data directory in
#                                config file will be searched if a file is not
#                                specified.
# args.dataFileEncoding string   Optional. Default is UTF-16
# args.dirPrefix        string   Optional. Prepended to directory path specified
#                                in config file.
# args.configFile       string   Optional. Default 'config.ini'
# args.configEncoding   string   Optional. Default 'UTF-8'
# args.testDfnFile      string   Optional. Test Definition File. If a file is
#                                not specified, all *.TPR files int the path
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

if args.verbose:
    print('\nTest Data Path: ' + testDataPath)
    print('Test Definition Path: ' + testDfnPath)

# **** Figure out what test definition file to use, and load it (or them!!)
# Get a list of test definition files in the test definition path
testDfnNames = listFiles(testDfnPath)
testDfns = [] # definition holding spot

if args.verbose:
    print('\nTest Definitions found:')
    print(testDfnNames)

# If a test definition file was specified, see if it was found. If not, error out.
# If no test definition file was specified, load them all, and look for the correct id later
if args.testDfnFile != '' and args.testDfnFile is not None and not args.testDfnFile in testDfnNames:
    # Test dfn file specified, but not found. Print message and leave.
    print('\nERROR: The test definition file \'' + args.testDfnFile + '\' was specified, \
but was not found. Exiting.')
    quit()
elif args.testDfnFile != '' and args.testDfnFile is not None and args.testDfnFile in testDfnNames:
    # Test dfn file specified, and found. Print message and load into a 1 element list
    print('\nSepecified test definition file \'' + args.testDfnFile + '\' was found and is being used.')
    try:
        testDfns.append(Glp2TestDfn(args.testDfnFile, join(testDfnPath, args.testDfnFile),
                                    args.testDfnEncoding))
    except UnicodeError as  ue:
        print('Unicode Error: Unable to load test definition file: ' + args.testDfnFile +
            '. Check encoding. ' + args.testDfnEncoding + ' was expected.')
        print(ue)
        quit()
elif args.testDfnFile == '' or args.testDfnFile is None:
    # Test dfn file not specified. Load all the definitions.
    print('\nThere was no test definition file specified.  The test definition id in the \
data will be used to try and determne the correct test definition file to use.')
    for dfnName in testDfnNames:
        try:
            testDfns.append(Glp2TestDfn(dfnName, join(testDfnPath, dfnName), args.testDfnEncoding))
        except UnicodeError as  ue:
            print('Unicode Error: Unable to load test definition file: ' + dfnName +
            '. Check encoding. ' + args.testDfnEncoding + ' was expected.')
            print(ue)

# **** Figure out what test data file to use, and load it (or them!!)
# Get a list of test data files in the data path
testDataNames = listFiles(testDataPath)
testDatas = [] # data holding spot

if args.verbose:
    print('\nTest data files found:')
    print(testDataNames)

# If a test data file was specified, see if it was found. If not, error out.
# If no test data file was specified, load them all, so they can all be processed.
if args.dataFile != '' and args.dataFile is not None and not args.dataFile in testDataNames:
    # Test data file specified, but not found. Print message and leave.
    print('\nERROR: The test data file \'' + args.dataFile + '\' was specified, \
but was not found. Exiting.')
    quit()
elif args.dataFile != '' and args.dataFile is not None and args.dataFile in testDataNames:
    # Test data file specified, and found. Print message and load into a 1 element list
    print('\nSepecified test data file \'' + args.dataFile + '\' was found and is being used.')
    # **** read the csv file into a data frame.  The first row is treated as the header
    try:
        with open(join(testDataPath, args.dataFile), mode='r', encoding=args.dataFileEncoding) as dataCsvFile:
            testDataSet = tuple(csv.reader(dataCsvFile, delimiter = ';'))
            # testDataSet may be one or more sets of test data (multiple tests saved in one file)
            # each test may be (usually is) more than one step
            testIds=set()   # holding spot for set of unique ids
            tests=[]        # holding spot for a list of test objects
            testObjs=[]
            # make a list of tests, but use seperate each test by Test GUID
            # Get a list of unique test ids
            for row in testDataSet[1:]: # exclude the header (1st row)
                if len(row) >= 1: # exclude blank rows
                    testIds.add(row[0])
            # make a filter function
            def idMatch(id, x):
                return x[0]==id
            # make a list for each unique id
            for id in testIds:
                # make a new list based on the filter
                tests.append(filter(lambda x: idMatch(id, x), testDataSet))
            # now make a test object for each filter result
            for test in tests:
                testObjs.append(Glp2TestData(test, testDataSet[0]))

            for test in testObjs:
                print(test)

    except UnicodeDecodeError as ude:
        print('Unicode Error: Unable to load test data file: ' + args.dataFile +
            '. Check encoding. ' + args.dataFileEncoding + ' was expected.')
        print(ude)
        quit()
#    except LookupError as lue:
#        print('Unknown encoding specified. Most common are \'UTF-16\' or \'UTF-8\'')
#        print(lue)
#        quit()

elif args.dataFile == '' or args.dataFile is None:
    # Test data file not specified. Load all those found.
    print('\nThere was no test data file specified.  All data files found will be processed.')
    for dataName in testDataNames:
        # TODO: Read CSV File, and get it into an object.
        pass



# get end  processing time
procEnd = datetime.now()
print('\n**** End Processing ****')
print('    Process end time: ' + procEnd.strftime('%m/%d/%Y %H:%M:%S'))
print('    Duration: ' + str(procEnd - procStart) + '\n')
