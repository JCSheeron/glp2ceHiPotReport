#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# pyTemplate.py
#
# This is intended to be a template to be used as a starting place when creating a
# new python program. It is just a basic formatted framwork and some examples of
# how to import libraries and set up command line arguments.
#
# imports
#
# system related
# import sys
# date and time stuff
from datetime import datetime, time
# from pandas.tseries.frequencies import to_offset
# from dateutil import parser as duparser

# csv file stuff
# import csv

# arg parser
import argparse

# numerical manipulation libraries
# import numpy as np
# import pandas as pd

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
eplStr="""Python Program Template file
 This can be a very long string that describes the program, the command 
 line arguments, options, etc. """

descrStr="Short description string."
parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, \
                                 description=descrStr, epilog=eplStr)
parser.add_argument('posArg1', help='Positional Argument 1')
parser.add_argument('posArg2', help= 'Positional Argument 2')
parser.add_argument('-optArg1', '--optionalArgument1', default=None, metavar='', \
                   help='Optional Argument 1')
parser.add_argument('-optArg2', '--optionalArgument2', default='optArg2', metavar='', \
                   help='Optional Argument 2. How to escape a special \
character (\", \").How to escape the %% character.')
parser.add_argument('-optTFArg1', action='store_true', default=False, \
                    help='True/False argument set to default to False, and is \
set to True if the argument is specified. The argument takes no values.')
# add a mutually exclusive required group
typegroup = parser.add_mutually_exclusive_group(required=True)
typegroup.add_argument('-me1',  action='store_true', default=False, \
                    help='Mutually Exclusive choice 1')
typegroup.add_argument('-me2', action='store_true', default=False, \
                    help='Mutually Exclusive choice 2')
typegroup.add_argument('-me3', action='store_true', default=False, \
                    help='Mutually Exclusive choice 3')
# parse the arguments
args = parser.parse_args()
print('The following arguments were parsed:')
print(args)

# At this point, the arguments will be:
# Argument          Values      Description
# args.posArg1      string
# args.posArg2      string
# args.optionalArgument1     string
# args.optionalArgument2      string
# args.optTFArg1    True/False
# args.me1          True/False
# args.me2          True/False
# args.me3          True/False

# Put the begin mark here, after the arg parsing, so argument problems are
# reported first.
print('**** Begin Processing ****')
# get start processing time
procStart = datetime.now()
print('    Process start time: ' + procStart.strftime('%m/%d/%Y %H:%M:%S'))

# Process the arguments
if args.posArg1 is not None:
    print(args.posArg1)
else:
    # arg is none, so print a message.
    # Not actually possible, since this is a positional argument.
    # Inclued here so we can see how to process arguments.
    print('No value for posArg1.')

if args.posArg2 is not None:
    print(args.posArg2)
else:
    # arg is none, so print a message.
    # Not actually possible, since this is a positional argument.
    # Inclued here so we can see how to process arguments.
    print('No value for posArg2.')

if args.optionalArgument1 is not None:
    print(args.optionalArgument1)
else:
    # arg is none, so print a message.
    print('No value for optArg1.')

if args.optionalArgument2 is not None:
    print(args.optionalArgument2)
else:
    # arg is none, so print a message.
    print('No value for optArg1.')

if args.optTFArg1 is not None:
    print(args.optTFArg1)
else:
    # arg is none, so print a message.
    print('No value for optTFArg1.')

if args.me1 is not None:
    print(args.me1)
else:
    # arg is none, so print a message.
    print('No value for me1.')

if args.me2 is not None:
    print(args.me2)
else:
    # arg is none, so print a message.
    print('No value for me2.')

if args.me3 is not None:
    print(args.me3)
else:
    # arg is none, so print a message.
    print('No value for me3.')

#get end  processing time
procEnd = datetime.now()
print('\n**** End Processing ****')
print('    Process end time: ' + procEnd.strftime('%m/%d/%Y %H:%M:%S'))
print('    Duration: ' + str(procEnd - procStart) + '\n')
