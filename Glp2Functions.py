#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# Glp2Functions.py
#
# A set of helper function definitions.
# These functions are defined here to help keep the main code 'cleaner'.
#
# imports
from ordered_set import OrderedSet # test ids
from Glp2TestData import Glp2TestData
from math import ceil

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
    testIds=OrderedSet()   # holding spot for set of unique ids. Use an ordered set to derrive testInstanceId
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
        tests.append(Glp2TestData(fileName=str(fileName),
                    data=test,
                    header=fileDataSet[0],
                    testInstanceId=testIds.index(id),
                    decimalSeparator=decimalSeparator))
    # tests[] has a Glp2TestData object for each test contained in the file
    return tests


# This function is expecting an FPDF object and a Glp2TestDfnStep.  It assumes
# the pdf format, font, font size, etc has been set up.
# The output will be 4 rows of cells: 1: a heading row, 2: value row,
# 3: heading row, 4: value row.
def MakePdfDfnStepRow(pdf, dfnStep):
    # calc the effective page width, epw, and the 'unit' cell width.  Per the
    # desired layout, there are 6 cell widths across a page.
    epw = pdf.w - (pdf.l_margin + pdf.r_margin)
    colWidth = epw/6.0
    # text height
    textHeight = pdf.font_size
    # font order is mono regular, mono bold, proportional regular, proportional bold

    # print the first row, a header row (bold)
    # Step, Mode, Method header
    if pdf.fontNames[1] != pdf.defaultFontNames[1]:
        # non-default
        pdf.set_font("boldMono", '')
    else:
        # default
        pdf.set_font(pdf.defaultFontNames[1], '')

    pdf.cell(colWidth, textHeight, 'Step', border = 1)
    pdf.cell(colWidth, textHeight, 'Mode', border = 1)
    pdf.cell(colWidth * 4, textHeight, 'Method', border = 1)
    pdf.ln(textHeight)

    # print the 2nd row, a value row (regular weight)
    # Step, Mode, Method values
    if pdf.fontNames[0] != pdf.defaultFontNames[0]:
        # non-default
        pdf.set_font("regularMono", '')
    else:
        # default
        pdf.set_font(pdf.defaultFontNames[0], '')

    pdf.cell(colWidth, textHeight, str(dfnStep.stepNum), border = 1)
    pdf.cell(colWidth, textHeight, str(dfnStep.stepMode), border = 1)
    pdf.cell(colWidth * 4, textHeight, str(dfnStep.stepMethod), border = 1)
    pdf.ln(textHeight)

    # print the 3rd row: description header (bold)
    if pdf.fontNames[1] != pdf.defaultFontNames[1]:
        # non-default
        pdf.set_font("boldMono", '')
    else:
        # default
        pdf.set_font(pdf.defaultFontNames[1], '')

    # extra wide description taking up all the columns.
    pdf.cell(colWidth * 6.0, textHeight, 'Description', border = 1)
    pdf.ln(textHeight)

    # print the 4th row: description, proportional, regular weight
    if pdf.fontNames[2] != pdf.defaultFontNames[2]:
        # non-default
        pdf.set_font("regularProp", '')
    else:
        # default
        pdf.set_font(pdf.defaultFontNames[2], '')

    # a line break is not needed if the multi_cell description is mulitple lines
    # detect the multiple line case
    startRowY = pdf.get_y()
    pdf.cell(colWidth * 6.0, textHeight, str(dfnStep.stepDescription), border = 1)
    endRowY = pdf.get_y()
    rowLines = ceil((endRowY - startRowY) / textHeight)
    print('rowLines: ' + str(rowLines))
    if rowLines < 1:
        pdf.ln(textHeight) # only needed after a description shorter than 1 line.

    # print the 5th row: Header Row (bold)
    # Test Voltage, Current Range, current limit, test time, ramp time, delay time
    if pdf.fontNames[1] != pdf.defaultFontNames[1]:
        # non-default
        pdf.set_font("boldMono", '')
    else:
        # default
        pdf.set_font(pdf.defaultFontNames[1], '')

    pdf.cell(colWidth, textHeight, 'Test Volt.', border = 1)
    pdf.cell(colWidth, textHeight, 'I Range', border = 1)
    pdf.cell(colWidth, textHeight, 'I Limit', border = 1)
    pdf.cell(colWidth, textHeight, 'Test Time', border = 1)
    pdf.cell(colWidth, textHeight, 'Ramp Time', border = 1)
    pdf.cell(colWidth, textHeight, 'Delay Time', border = 1)
    pdf.ln(textHeight)

    # print the 6th row: values (regular weight)
    # Test Voltage, Current Range, current limit, test time, ramp time, delay time
    if pdf.fontNames[0] != pdf.defaultFontNames[0]:
        # non-default
        pdf.set_font("regularMono", '')
    else:
        # default
        pdf.set_font(pdf.defaultFontNames[0], '')

    pdf.cell(colWidth, textHeight, str(dfnStep.testVoltage), border = 1)
    pdf.cell(colWidth, textHeight, str(dfnStep.currentRange), border = 1)
    pdf.cell(colWidth, textHeight, str(dfnStep.currentLimit), border = 1)
    pdf.cell(colWidth, textHeight, str(dfnStep.testTime), border = 1)
    pdf.cell(colWidth, textHeight, str(dfnStep.rampTime), border = 1)
    pdf.cell(colWidth, textHeight, str(dfnStep.delayTime), border = 1)
    pdf.ln(textHeight)

# This function is expecting an FPDF object and a Glp2TestDfnStep.  It assumes
# the pdf format, font, font size, etc has been set up.
# The output will be 4 rows of cells: 1: a heading row, 2: value row,
# 3: heading row, 4: value row.
def MakePdfDataStepRow(pdf, dataStep):
    # calc the effective page width, epw, and the 'unit' cell width.  Somewhat
    # arbitrarily, but also to be consistent with the similar function for
    # definition steps, there will be a unit cell width based on 6 cells per 
    # page width.
    epw = pdf.w - (pdf.l_margin + pdf.r_margin)
    colWidth = epw/6.0
    # text height
    textHeight = pdf.font_size
    # font order is mono regular, mono bold, proportional regular, proportional bold

    # print the first row, a header row (bold)
    # Step, Timestamp
    if pdf.fontNames[1] != pdf.defaultFontNames[1]:
        # non-default
        pdf.set_font("boldMono", '')
    else:
        # default
        pdf.set_font(pdf.defaultFontNames[1], '')

    pdf.cell(colWidth, textHeight, 'Step', border = 1)
    pdf.cell(colWidth * 3, textHeight, 'Timestamp', border = 1)
    pdf.ln(textHeight)

    # print the 2nd row, a value row (regular weight)
    # Step, Timestamp
    if pdf.fontNames[0] != pdf.defaultFontNames[0]:
        # non-default
        pdf.set_font("regularMono", '')
    else:
        # default
        pdf.set_font(pdf.defaultFontNames[0], '')

    pdf.cell(colWidth, textHeight, str(dataStep.stepNumber), border = 1)
    pdf.cell(colWidth * 3, textHeight, str(dataStep.testTimestamp), border = 1)
    pdf.ln(textHeight)

    # print the 3rd row: Header Row (bold)
    # Nom voltage, measured voltage, current limit, measured current
    if pdf.fontNames[1] != pdf.defaultFontNames[1]:
        # non-default
        pdf.set_font("boldMono", '')
    else:
        # default
        pdf.set_font(pdf.defaultFontNames[1], '')

    pdf.cell(colWidth, textHeight, 'Volt. Nom.', border = 1)
    pdf.cell(colWidth, textHeight, 'Volt. Meas.', border = 1)
    pdf.cell(colWidth, textHeight, 'I Limit', border = 1)
    pdf.cell(colWidth, textHeight, 'I Meas.', border = 1)
    pdf.ln(textHeight)

    # print the 4th row: values (regular weight)
    # Nom voltage, measured voltage, current limit, measured current
    if pdf.fontNames[0] != pdf.defaultFontNames[0]:
        # non-default
        pdf.set_font("regularMono", '')
    else:
        # default
        pdf.set_font(pdf.defaultFontNames[0], '')

    pdf.cell(colWidth, textHeight, str(dataStep.nominalVoltage), border = 1)
    pdf.cell(colWidth, textHeight, str(dataStep.measuredVoltage), border = 1)
    pdf.cell(colWidth, textHeight, str(dataStep.currentLimit), border = 1)
    pdf.cell(colWidth, textHeight, str(dataStep.measuredCurrent), border = 1)
    pdf.ln(textHeight)


# Given the width, height, and a string, determine how high the multi-cell
# will be (auto line wrap).  Use the passed in unit and parameter so the 
# calculated value takes into account the target font and unit.
#def GetMultiCellHeight(pdf, unit, w, h, txt, border = 0, align = 'J', fill = False):
#    '''Return the height of a multi-cell given a height, width, and string.'''
#    # Note that the border and align and fill are there to make the call
#    # consistent with the multi_cell ctor.
#    # This routine is a bit brute force:  Make a pdf and a multicell that
#    # will never be seen, and calc and return the delta Y value.
#    #
#    # Get params from passed in pdf
#    font_family = pdf.font_family
#    font_style = pdf.font_style
#    font_size_pt = pdf.font_size_pt
#    # make a local pdf
#    tpdf = FPDF(format='letter', unit = unit)
#    tpdf.add_page()
#    tpdf.set_font(font_family, font_style, font_size_pt)
#    startY = tpdf.get_y()
#    tpdf.multi_cell(w, h, txt, border, align, fill)
#    endY = tpdf.get_y()
#    return (endY - startY)
#
