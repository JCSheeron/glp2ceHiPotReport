#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# Glp2Functions.py
#
# A set of helper function definitions.
# These functions are defined here to help keep the main code 'cleaner'.
#
# imports
from sys import exc_info # error reporting
from ordered_set import OrderedSet # test ids
from Glp2TestData import Glp2TestData
from math import ceil
# import numpy as np
import matplotlib.pyplot as plt # for plotting
import matplotlib.ticker as ticker
# pdf manipulation
from PyPDF2 import PdfFileMerger, PdfFileReader


# Create a list of test data objects from a test data file.
# The file may contain data for more than one test.
# It is expected this data will be a list of lists:  Each test step will be a
# list of values, and each test will represented as a list of rows. Each rowG
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

    pdf.cell(colWidth, textHeight, 'V Test (V)', border = 1)
    pdf.cell(colWidth, textHeight, 'I Range (mA)', border = 1)
    pdf.cell(colWidth, textHeight, 'I Limit (mA)', border = 1)
    pdf.cell(colWidth, textHeight, 'Test Time (s)', border = 1)
    pdf.cell(colWidth, textHeight, 'Ramp Time (s)', border = 1)
    pdf.cell(colWidth, textHeight, 'Delay Time (s)', border = 1)
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
    pdf.ln(textHeight * 3)

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
    colWidth = epw/12.0
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
    pdf.cell(colWidth * 9, textHeight, 'Timestamp', border = 1)
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
    pdf.cell(colWidth * 9, textHeight, str(dataStep.testTimestamp), border = 1)
    pdf.ln(textHeight)

    # print the 3rd row: comments header (bold)
    if pdf.fontNames[1] != pdf.defaultFontNames[1]:
        # non-default
        pdf.set_font("boldMono", '')
    else:
        # default
        pdf.set_font(pdf.defaultFontNames[1], '')

    # extra wide description taking up all the columns.
    pdf.cell(colWidth * 10, textHeight, 'Comments', border = 1)
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
    pdf.cell(colWidth * 10, textHeight, str(dataStep.comments), border = 1)
    endRowY = pdf.get_y()
    rowLines = ceil((endRowY - startRowY) / textHeight)
    if rowLines < 1:
        pdf.ln(textHeight) # only needed after a description shorter than 1 line.

    # print the 5th row: Header Row (bold)
    # Nom voltage, measured voltage, current limit, measured current
    if pdf.fontNames[1] != pdf.defaultFontNames[1]:
        # non-default
        pdf.set_font("boldMono", '')
    else:
        # default
        pdf.set_font(pdf.defaultFontNames[1], '')

    pdf.cell(colWidth * 2.5, textHeight, 'V Nom. (V)', border = 1)
    pdf.cell(colWidth * 2.5, textHeight, 'V Max Meas. (V)', border = 1)
    pdf.cell(colWidth * 2.5, textHeight, 'I Limit (mA)', border = 1)
    pdf.cell(colWidth * 2.5, textHeight, 'I Max Meas. (mA)', border = 1)
    pdf.ln(textHeight)

    # print the 6th row: values (regular weight)
    # Nom voltage, measured voltage, current limit, measured current
    if pdf.fontNames[0] != pdf.defaultFontNames[0]:
        # non-default
        pdf.set_font("regularMono", '')
    else:
        # default
        pdf.set_font(pdf.defaultFontNames[0], '')

    pdf.cell(colWidth * 2.5, textHeight, str(dataStep.nominalVoltage), border = 1)
    pdf.cell(colWidth * 2.5, textHeight, str(dataStep.measuredVoltage), border = 1)
    pdf.cell(colWidth * 2.5, textHeight, str(dataStep.currentLimit), border = 1)
    pdf.cell(colWidth * 2.5, textHeight, str(dataStep.measuredCurrent), border = 1)
    pdf.ln(textHeight * 3)

# Return a csv string containing the graph data with the following format:
# Axis0Label (units), Axis1Label (units) ... \n
# value, value, ... \n
#
# Provide the axis definitions, and the axis data.
# csvString will be overwritten.  It is assumed axisDefs and axisData are tuples
# to prevent inadvertant changes.
# The axisDefs is assumed to have this format (tuple of tuples):
# (
#   (axis 0 label, axis 0 units, axis 0 color, axis 0 min, axis 0 max, axis 0 formatting),
#   (axis 1 label, axis 1 units, axis 1 color, axis 1 min, axis 1 max, axis 1 formatting),
#   ...
#   )
def MakeGraphDataCsvFormat(axisDefs, axisData):
    # Make the csv header
    # Axis 0 label (axis 0 units), Axis 1 label (axis 1 units) ... \n

    # Make a temp holding spot, and loop thru the axis defs, and create the
    # csv header row
    hStr= ''
    axisLabel = '';
    for axis in axisDefs:
        # the label uses odd codes.  Make them user friendly where the
        # codes are known (emperically determined)
        if '%%968' == axis[0]:
            # code for current
            label= 'current'
        elif '%%740' == axis[0]:
            # code for voltate
            label= 'voltage'
        else:
            # no or unknown code. Use label directly.
            label= axis[0]

        hStr += label + ' (' + axis[1] + '),'
    # strip off last comma and add a new line
    hStr= hStr[:-1] + '\n'

    # Make a temp holding spot and loop thru the axis data appending
    # the data for each row
    rStr = ''
    for row in axisData:
        for value in row:
            rStr += value + ','
        # strip off last comma and add a new line
        rStr= rStr[:-1] + '\n'
    # add the row data to the header and return
    return hStr + rStr

# Create a plot and make a pdf using the specified file name, if specified.
def PlotTvsVandI(tData, vData, iData, iThreshold, iMax, title='', showPlot=False, fileName=None):
    # get a figure and a single sub-plot to allow better control
    # than using no sub-plots
    fig, vAxis = plt.subplots()

    # set the titles
    fig.suptitle('Current and Voltage versus Time', \
                fontsize=14, fontweight='bold')
    plt.title(title, fontsize=12, fontweight='bold')
    tColor = 'black'
    vColor = 'blue'
    iColor = 'green'
    mxColor = 'orange' # max measured color
    thColor = 'red' # threshold color
    vAxis.set_xlabel('time (s)', color=tColor)
    vAxis.set_ylabel('voltage (V)', color=vColor)
    vAxis.plot(tData, vData, color=vColor)
    # make additional room for the labels
    #plt.subplots_adjust(left=0.18, bottom=0.18)

    # make a second y axis for current that shares the same x axis as voltage
    iAxis = vAxis.twinx()
    iAxis.set_ylabel('current (mA)', color=iColor)
    iAxis.plot(tData, iData, color=iColor)
    # plot horizontal line at current threshold
    iThs = [iThreshold] * len(tData)
    iAxis.plot(tData, iThs, color=thColor)
    # plot horizontal line at the max measured current
    iMx = [iMax] * len(tData)
    iAxis.plot(tData, iMx, color=mxColor)
    # show the grid
    vAxis.grid(b=True, which='both', linewidth=0.5, linestyle='-.')

    # iEstablish a relation between the two zxes scales using a funciton and
    # set the ticks on the second (iAxis) to be in the same location as on the
    # first (vAxis).
    # For each vAxis tick, figure out the percentage up the vAxis and put the
    # iAxis tick in the same spot
    limsV = vAxis.get_ylim() # [0] axis min value, [1] axis max value
    limsI = iAxis.get_ylim()
    # IMin + ((x - VMin) / (VMax - VMin)) * (IMax - IMin)
    f = lambda x: limsI[0] + ((x - limsV[0])/(limsV[1] - limsV[0])) * (limsI[1] - limsI[0])
    iTicks = f(vAxis.get_yticks())
    iAxis.yaxis.set_major_locator(ticker.FixedLocator(iTicks))


    # put page numbers (3 of 3) in the lower left
    #txStyle = dict(fontsize=8, color='black', horizontalalignment='left')
    #plt.text(0.05, 0, 'Page 3 of 3', transform=plt.gcf().transFigure, **txStyle)

    # Save the plot if fileName is specified.
    if fileName is not None:
        try:
            # not sure what the possible exceptions are. Take a guess, and raise
            # in the 'generic' case
            plt.savefig(fileName, orientation='portrait', papertype='letter',
                       format='pdf', transparent=False, frameon=False,
                       bbox_inches='tight', pad_inches=0.25)
        except IOError as ioe:
            print('I/O error when saving the plot:')
            print(ioe)
        except:
            print('Unexpcted error saving the plot: ', sys.exc_info()[0])
            raise

    # Show the plot if specified. The user will need to close the plot.
    # Otherwise close the plot so it no longer consumes memory
    if showPlot:
        plt.show()
    else:
        plt.close()

# Merge (append) pdf source 2 to the end of pdf source 1, and save the result in the
# destination file. Delete the source files if option is specified.
def MergePdf(fileNameSrc1, fileNameSrc2, fileNameDest, deleteSrcFiles=False ):

    # Now merge the plot pdf onto the end of the cal data pdf
    merger= PdfFileMerger()
    try:
       src1= open(fileNameSrc1, 'rb')
       src2= open(fileNameSrc2, 'rb')
       merger.append(PdfFileReader(src1))
       merger.append(PdfFileReader(src2))
       src1.close()
       src2.close()
       merger.write(fileNameDest)
       merger.close()

    except IOError as ioe:
        print('I/O error when merging the data and plot files:')
        print(ioe)
    except:
        print('Unexpcted error merging the data and plot files: ', exc_info()[0])
        raise

    # Delete the source files if specified
    if deleteSrcFiles:
        try:
            # delete the individual files
            if os.path.exists(fileNameSrc1):
                os.remove(fileNameSrc1)
            if os.path.exists(fileNameSrc2):
                os.remove(fileNameSrc2)

        except:
            print('Unexpcted error when deleting files in MergePdf(): ', exc_info()[0])
            raise

