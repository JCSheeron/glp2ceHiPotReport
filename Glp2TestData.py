#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Glp2TestData.py
#
# imports
#

class Glp2TestData(object):
    def ClearData(self, header):
        self._testDfnName = ''
        self._testDfnId = ''
        self._testTimestamp = None
        self._deviceNumber = ''
        self._rawData = None
        self._graphData = None
        self._rows = 0
        if header is None: # no header specified
            self._dataHeaders = None
        else: # header specified
            try:
                # header is specified, but it must be convertable to a tuple.
                self._dataHeaders = tuple(header)
            except ValueError as ve:
                print('Value Error: The header specified when clearing the data is not \
a tuple, and cannot be converted to a tuple. This generally means it must be something iteratable.')
                print(ve)
                self._dataHeaders = None

    def __init__(self, data=None, header=None):
        if data is None: # no data provided
            # no data specified. Create an empty object. Use the header data if specified.
            ClearData(header=None)
        else: # data provided
            # make sure the data is convertable to a tuple. If not create
            # an empty object
            try:
                self._rawData=tuple(data)
                # if we get here, we should have a tuple with something in it
                # Assume it is a multi element tuple, with each element containing 
                # a row.
                # get the number of rows. This will inclued the first, presumably header row
                # self._rows = len(self._rawData)
                # get the header row as long as there is at least 1 row
                # if self._rows >= 1:
                #     self._dataHeaders = self._da
                # get the header values
            except ValueError as ve:
                print('Value Error: data parameter must be a tuple or something \
convertalbe to a tuple. This generally means it must be something iteratable. \
Creating empty object.')
                print(ve)
                ClearData()

        if header is None: # no header specified
            self._dataHeaders = None
        else: # header specified
            try:
                # header is specified, but it must be convertable to a tuple.
                self._dataHeaders = tuple(header)
            except ValueError as ve:
                print('Value Error: The header parameter must be a tuple, \
or something convertable to a tuple. This generally means it must be something \
iteratable. Setting the header to None.')
                print(ve)
                self._dataHeaders = None

    def __repr__(self):
        outputMsg=  '{:6} {}'.format('\nName: ', self._name + '\n')
        outputMsg+= '{:6} {}'.format('Id: ', self._id)
        outputMsg+=  '{}'.format('\nConfiguraiton:\n')
        # construct the config data into the message
        for section in self._config:
            outputMsg+= section + '\n'
            for option in self._config[section]:
                outputMsg+= '  ' + option + ':' + self._config[section][option] + '\n'
        return(outputMsg)

    # properties
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name = str(newName) # use the string version

    @property
    def id(self):
        return self._id

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, newFile, fileEncoding='UTF-8'):
        self._config = configParser.ConfigParser()
        self._config.read(newFile, fileEncoding)
        if self._config.has_option('General Data', 'GUID'):
            self._id = self._config['General Data']['GUID']
        else:
            self._id = 'No GUID found'

