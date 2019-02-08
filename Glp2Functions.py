#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# Glp2Functions.py
#
# A set of helper function definitions.
# These functions are defined here to help keep the main code 'cleaner'.
#
# imports
from Glp2TestData import Glp2TestData

# Create a list of test data objects from a test data file.
# The file may contain data for more than one test.
# It is expected this data will be a list of lists:  Each test step will be a
# list of values, and each test will represented as a list of rows. Each row
# has a test GUID. This GUID is unique for each test, so all the rows (steps) 
# with a particular id will be contained in a single test data object.
# Return a list of test data objects (Glp2TestData objects), with each object
# having a unique test GUID.
#

def MakeTestList(fileName, dataSet, decimalSeparator):
    # The file data set must be a tuple, or something like a tuple.
    # A tuple is used to guard against bugs changing the data
    # Assume the first row is the header row.
    # The decimalSeparator is used to tell the test object if a decimal point 
    # or comma is used as a decimal separator.
    try:
        fileDataSet = tuple(dataSet)
    except ValueError as ve:
        print('Error: The data used to make a list of Glp2TestData objects is \
expected to be a tuple or something that can be converted to a tuple.')
        print(ve)
        quit()

    # If we get here, we have a tuple of the passed in file data set.
    # fileDataSet may be one or more sets of test data (multiple tests saved in one file)
    # each test may be (usually is) more than one step
    testIds=set()   # holding spot for set of unique ids
    test=[]         # holding spot for the rows corresponding to one test id
    tests=[]        # holding spot for test data objects created from the file data set.
    # Make a list of tests (tests[]),  but seperate each test by Test GUID
    # Get a list of unique test ids -- the set() container guarantees uniqueness
    # TODO: replace index values, (e.g. 0 in row[0]) with index values originating from config file
    for row in fileDataSet[1:]: # exclude the header (1st row)
        if len(row) >= 1: # exclude blank rows
            testIds.add(row[0])
    # Get the rows from the file data set that match a unique test id.
    # Have one list of rows for each unique id.
    for id in testIds:
        test.clear()
        for row in fileDataSet[1:]:
            # make a new list based on the filter.
            # Skip blank rows
            if len(row) >= 1 and id == row[0]:
                test.append(row)
        # At this point, all the rows for a given test id should be in test[]
        # Create a test object from it, and append it to a list of tests.
        # test[] contains the data, and the first row of the file data set
        # is the header info.
        tests.append(Glp2TestData(str(fileName), test, fileDataSet[0], decimalSeparator))
    # now tests[] has a Glp2TestData object for each test contained in the file
    return tests

def ParseGraphString(graphString):
    pass

