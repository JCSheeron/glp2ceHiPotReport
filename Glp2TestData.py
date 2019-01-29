#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Glp2TestData.py
#
# imports
#

class Glp2TestData(object):
    def __init__(self, data=None, header=None, nameIdx=25, guidIdx=49,
                timestampIdx=30, deviceNumberIdx=31, graphDataIdx=76):
        if data is None: # no data provided
            # no data specified. Create an empty object. Use the header data if specified.
            ClearData(header=header)
        else: # data provided
            # make sure the data is convertable to a tuple. If not create
            # an empty object
            try:
                self._rawData=tuple(data)
                self._len = len(self._rawData)
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

        self._nameIdx = nameIdx
        self._guidIdx = guidIdx
        self._timestampIdx = timestampIdx
        self._deviceNumberIdx = deviceNumberIdx
        self._graphDataIdx = graphDataIdx

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
        outputMsg=  '{:16} {}\n'.format('Test Dfn Name: ', self.testDfnName)
        outputMsg+= '{:16} {}\n'.format('Test Dfn Id: ', self.testDfnId)
        outputMsg+= '{:16} {}\n'.format('Test Timestamp: ', self.testTimestamp)
        outputMsg+= '{:16} {}\n'.format('Device Number: ', self.deviceNumber)
        outputMsg+= '{:16} \n'.format('Data Header: ')
        for idx, heading in enumerate(self._dataHeader):
            outputMsg+= '  {:2}: {}\n'.format(idx, heading)
        outputMsg+= '{:16} \n'.format('Test Data: ')
#        for idx, heading in enumerate(self._dataHeader):
#            outputMsg+= '  {:4}-{:<4}: {}\n'.format(idx, heading, self._rawData[idx])

        return(outputMsg)

    def ClearData(self, header=None):
        self._rawData = None
        self._len = 0

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
    @property
    def testDfnName(self):
        # get the value from the raw data if the data is present
        if self._rawData is not None and self._nameIdx + 1 <= self._len:
            return self._rawData[self._nameIdx]
        else:
            return None

    @property
    def testDfnId(self):
        # get the value from the raw data if the data is present
        if self._rawData is not None and self._guidIdx + 1 <= self._len:
            return self._rawData[self._guidIdx]
        else:
            return None

    @property
    def testTimestamp(self):
        # get the value from the raw data if the data is present
        if self._rawData is not None and self._timestampIdx + 1 <= self._len:
            return self._rawData[self._timestampIdx]
        else:
            return None

    @property
    def deviceNumber(self):
        # get the value from the raw data if the data is present
        if self._rawData is not None and self._deviceNumberIdx + 1 <= self._len:
            return self._rawData[self._deviceNumberIdx]
        else:
            return None

    @property
    def rows(self):
        return self._len

    @property
    def header(self):
        return (self._dataHeader)

    @property
    def data(self):
        return self._rawData

    @property
    def graphData(self):
        # get the value from the raw data if the data is present
        if self._rawData is not None and self._graphDataIdx + 1 <= self._len:
            return self._rawData[self._graphDataIdx]
        else:
            return None


