#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Glp2TestDataStep.py
#
# imports
#

class Glp2TestDataStep(object):
    def __init__(self, data=None, header=None, guidIdx=1, stepNumberIdx=2,
            timeStampIdx=30, deviceNumberIdx=31, graphDatIdx=76):
        # The data expected is a tuple, list, or something convertable to a
        # tuple that has an entire row of data from a test data file.  The
        # indexes are the normal column counts, starting at zero.
        if data is not None: # data provided
            # make sure the data is convertable to a tuple. If not, report an 
            # error -- a tuple is immutable, so an empty one isn't very useful.
            try:
                self._rawData=tuple(data)
                # if we get here, we should have a tuple with something in it
                # Assume it is a multi element tuple, with each element containing
                # the details of a test step.
            except ValueError as ve:
                print('Value Error: The data parameter must be a tuple or something \
convertalbe to a tuple. This generally means it must be something iteratable. \
No step information captured.')
                print(ve)
                self._rawData = None
        else: # no data provided
            self._rawData = None


        self._guidIdx = guidIdx
        self._stepNumberIdx = stepNumberIdx
        self._timestampIdx = timeStampIdx
        self._deviceNumberIdx = deviceNumberIdx
        self._graphDataIdx = graphDataIdx

        if header is not None: # header specified
            try:
                # header is specified, but it must be convertable to a tuple.
                self._dataHeader = tuple(header)
            except ValueError as ve:
                print('Value Error: The header parameter must be a tuple, or something \
convertable to a tuple. This generally means it must be something iteratable. \
Header not changed.')
                print(ve)
                self._dataHeader = None
        else: # no header specified
            self._dataHeader = None

    def __repr__(self):
        outputMsg=  '{:16} {}\n'.format('Test Step GUID: ', self.stepGuid)
        outputMsg+= '{:16} {}\n'.format('Test Step Number:', self.stepNumber)
        outputMsg+= '{:16} {}\n'.format('Test Step Timestamp: ', self.testTimestamp)
        outputMsg+= '{:16} {}\n'.format('Test Step Device Number: ', self.deviceNumber)
        # header
        if self_dataHeader is not None:
            outputMsg+= '{:16} \n'.format('Data Header: ')
            for idx, heading in enumerate(self._dataHeader):
                outputMsg+= '  {:2}: {}\n'.format(idx, heading)

        # data - may include header info also
        if self._dataHeader is not None and self._rawData is not None:
            # data and header info avail -- include header info
            outputMsg+= '{:16} \n'.format('Test Data: ')
            for idx, heading in enumerate(self._dataHeader):
                for value in self._rawData:
                    outputMsg+= '  {:4}-{:4<}: {}\n'.format(idx, heading, value)
        elif self._dataHeader is None and self._rawData is not None:
            # data but no header info
            for idx, value in enumerate(self._rawData):
                outputMsg+= '  {:4}: {}\n'.format(idx, value)
        else:
            # no data stored!!
            outputMsg+= '  No Data\n'

        return(outputMsg)

    # properties
    @property
    def stepGuid(self):
        # get the value from the raw data if the data is present
        if self._rawData is not None and self._guidIdx + 1 <= len(self._rawData):
            return self._rawData[self._guidIdx]
        else:
            return None

    @property
    def stepNumber(self):
        # get the value from the raw data if the data is present
        if self._rawData is not None and self._stepNumberIdx + 1 <= len(self._rawData):
            return self._rawData[self._stepNumberIdx]
        else:
            return None

    @property
    def testTimestamp(self):
        # get the value from the raw data if the data is present
        if self._rawData is not None and self._timestampIdx + 1 <= len(self._rawData):
            return self._rawData[self._timestampIdx]
        else:
            return None

    @property
    def deviceNumber(self):
        # get the value from the raw data if the data is present
        if self._rawData is not None and self._deviceNumberIdx + 1 <= len(self._rawData):
            return self._rawData[self._deviceNumberIdx]
        else:
            return None

    @property
    def len(self):
        return len(self._rawData)

    @property
    def header(self):
        return (self._dataHeader)

    @header.setter
    def header(self, headerData):
        if headerData is not None:
            try:
                # header is specified, but it must be convertable to a tuple.
                self._dataHeader = tuple(headerData)
            except ValueError as ve:
                print('Value Error: The header parameter must be a tuple, or something \
convertable to a tuple. This generally means it must be something iteratable. \
Header not changed.')
                print(ve)
        else: # nothing specified for header
            self._dataHeader = None



    @property
    def data(self):
        return self._rawData

    @data.setter
    def data(self, data):
        if data is not None: # data provided
            # make sure the data is convertable to a tuple. If not, report an 
            # error -- a tuple is immutable, so an empty one isn't very useful.
            try:
                self._rawData=tuple(data)
                # if we get here, we should have a tuple with something in it
                # Assume it is a multi element tuple, with each element containing
                # the details of a test step.
            except ValueError as ve:
                print('Value Error: The data parameter must be a tuple or something \
convertalbe to a tuple. This generally means it must be something iteratable. \
Data not changed.')
                print(ve)
        else: # no data provided
            self._rawData = None


    @property
    def graphData(self):
        # get the value from the raw data if the data is present
        if self._rawData is not None and self._graphDataIdx + 1 <= len(self._rawData):
            return self._rawData[self._graphDataIdx]
        else:
            return None


