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
# TODO: More info about the input file format.
# TODO: More info about the text data in the output PDF.
# TODO: More info about the plot in the output PDF.
#
# Specified is the input data file and the name of the PDF file created.
# TODO: What else is specified?
#
# imports
#
# system related
# import sys
# date and time stuff
from datetime import datetime, time
# from pandas.tseries.frequencies import to_offset
# from dateutil import parser as duparser

# config file parser
import configparser

# csv file stuff
import csv

# arg parser
import argparse

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
# TimeStamped Indexed Data Class
# from bpsTsIdxData import TsIdxData
# list duplication helper functions
# from bpsListDuplicates import listDuplicates 
# from bpsListDuplicates import listToListIntersection


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
parser.add_argument('dataFileName', help='Input data file (Schleich GLP2-ce file)')
parser.add_argument('outputFileName', help= 'Output PDF file name. The .pdf extension \
will be added to the file name if not specified.')
parser.add_argument('-dirPrefix', default='', metavar='', \
                    help='Directory prefix. If specified, this is prepended to \
the paths specified in the configuration file (default is config.ini). This is \
helpful if the data is inside directories that are named using serial numbers, \
dates, times, test numbers, station numbers, or some other dynamic data that is \
not known when the config file is created.')
parser.add_argument('-c', '--configFile', default='config.ini', metavar='', \
                   help='Config file. Default is config.ini.')
parser.add_argument('-v', '--verbose', action='store_true', default=False, \
                    help='Verbose output, usually used for troubleshooting.')
# parse the arguments
args = parser.parse_args()

# At this point, the arguments will be:
# Argument          Values      Description
# args.dataFileName     string
# args.outputFileName   string
# args.configFile       string, default 'config.ini'
# args.verbose          True/False, default False

# Put the begin mark here, after the arg parsing, so argument problems are
# reported first.
print('**** Begin Processing ****')
# get start processing time
procStart = datetime.now()
print('    Process start time: ' + procStart.strftime('%m/%d/%Y %H:%M:%S'))

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
    print('The config file(s) used are:')
    print(cfgFile)
    print('\nThe resulting configuration has these settings:')
    for section in config:
        print(section)
        for key in config[section]:
            print('  ', key, ':', config[section][key])




#get end  processing time
procEnd = datetime.now()
print('\n**** End Processing ****')
print('    Process end time: ' + procEnd.strftime('%m/%d/%Y %H:%M:%S'))
print('    Duration: ' + str(procEnd - procStart) + '\n')
