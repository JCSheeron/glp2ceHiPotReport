#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Glp2TestData.py
#
# imports
#

class Glp2TestData(object):
    def __init__(self, data=None, header=None):
        if data is None: # no data provided
            # no data specified. Create an empty object. Use the header data if specified.
            ClearData(header=None)
        else: # data provided
            # make sure the data is convertable to a tuple. If not create
            # an empty object
            self._testDfnName = 'Peter'
            self._testDfnId = '666.6'
            self._testTimestamp = '12/15/2019'
            self._deviceNumber = '123456789'
            self._rawData = None
            self._graphData = None
            try:
                self._rawData=tuple(data)
                # if we get here, we should have a tuple with something in it
                # Assume it is a multi element tuple, with each element containing 
                # a row.
                # get the number of rows. This will inclued the first, presumably header row
                # self._rows = len(self._rawData)
                # get the header row as long as there is at least 1 row
                # if self._rows >= 1:
                #     self._dataHeader = self._da
                # get the header values
            except ValueError as ve:
                print('Value Error: data parameter must be a tuple or something \
convertalbe to a tuple. This generally means it must be something iteratable. \
Creating empty object.')
                print(ve)
                ClearData()

        if header is None: # no header specified
            self._dataHeader = None
        else: # header specified
            try:
                # header is specified, but it must be convertable to a tuple.
                self._dataHeader = tuple(header)
            except ValueError as ve:
                print('Value Error: The header parameter must be a tuple, \
or something convertable to a tuple. This generally means it must be something \
iteratable. Setting the header to None.')
                print(ve)
                self._dataHeader = None

    def __repr__(self):
        outputMsg=  '{:16} {}\n'.format('Test Dfn Name: ', self._testDfnName)
        outputMsg+= '{:16} {}\n'.format('Test Dfn Id: ', self._testDfnId)
        outputMsg+= '{:16} {}\n'.format('Test Timestamp: ', self._testTimestamp)
        outputMsg+= '{:16} {}\n'.format('Device Number: ', self._deviceNumber)
        outputMsg+= '{:16} \n'.format('Data Header: ')
        for idx, heading in enumerate(self._dataHeader):
            outputMsg+= '  {:2}: {}\n'.format(idx, heading)
        outputMsg+= '{:16} \n'.format('Test Data: ')
        outputMsg+= '{:16} \n'.format('Test Data: ')
        for rowNum, rowData in enumerate(self._rawData):
            for col, value in enumerate(rowData):
                outputMsg+= '  {:4}-{:<4} ({:27}): {}\n'.format(rowNum, col, self._dataHeader[col], value)

        return(outputMsg)

    def ClearData(self, header):
        self._testDfnName = ''
        self._testDfnId = ''
        self._testTimestamp = None
        self._deviceNumber = ''
        self._rawData = None
        self._graphData = None
        if header is None: # no header specified
            self._dataHeader = None
        else: # header specified
            try:
                # header is specified, but it must be convertable to a tuple.
                self._dataHeader = tuple(header)
            except ValueError as ve:
                print('Value Error: The header specified when clearing the data is not \
a tuple, and cannot be converted to a tuple. This generally means it must be something iteratable.')
                print(ve)
                self._dataHeader = None

    # properties
    # TODO: Derive the property value from the data, and get rid of the member variables
    @property
    def testDfnName(self):
        return self._testDfnName

    @property
    def testDfnId(self):
        return self._testDfnId

    @property
    def testTimestamp(self):
        return self._testTimestamp

    @property
    def deviceNumber(self):
        return self._deviceNumber

    @property
    def rows(self):
        return len(self._rawData)

    @property
    def header(self):
        return (self._dataHeader)
    @property
    def data(self):
        return self._rawData

    @property
    def graphData(self):
        return self._graphData


