#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# Glp2GraphData.py
#
# Given a raw data string, or something convertable to a string, parse the
# string into a tuple of axis definitions and a tuple of axis values, where each
# axis definition is a tuple of definition fileds, and each value item is a
# tuple of values.  The order of the tuple of values matches the order of the axis
# defintions, so it is implied which value goes with which axis.  Tuples are used
# so inadvertant change is an error.
#
# imports
#
class Glp2GraphData(object):
    # class constants
    SOG_TOKEN = '|#GR#|'    # Denote Start of the graph
    SOAX_TOKEN = '<'        # Denote the start of axis definition(s)
    EOAX_TOKEN = '>'        # Denote the end of axis definition(s)
    AXIS_TOKEN ='|'         # Delimits one axis definition from another
    AXIS_FIELD_TOKEN = '\\' # Delimits axis definition fields
    DATA_AXIS_TOKEN = '|'   # Delimits axis values within a data sample set
    DATA_SAMPLE_TOKEN = '\\'# Delimits one sample set from the next is the data set
    EOD_TOKEN = '}'         # End of data token


    # find the position of the beginning of the graph data (i.e. return the
    # position of the start of graph (SOG) string token. return value is zero based for the
    # beginning of the string, and -1 if not found.
    def _posSOG(self):
        return self._rawDataStr.find(self.SOG_TOKEN)

    # Break out the axis definitions and return a list of lists. Each
    # item in the list will be a list of field values for an axis definition.
    # The fields (6 fields if all is well) of the axis definition are delimited
    # by the AXIS_FIELD_TOKEN.  The start and end of the axis definition
    # section is delimited within the graph data by being between the SOAX and
    # EOAX Tokens.  Within the axis definition, one axis definition is delimited
    # from another with the AXIS_TOKEN.
    def _getAxisDfns(self):
        # make sure there is a start of graph data
        posSog = self._rawDataStr.find(self.SOG_TOKEN)
        # get start and end of axis definition positions.
        posSoax = self._rawDataStr.find(self.SOAX_TOKEN)
        posEoax = self._rawDataStr.find(self.EOAX_TOKEN)
        # If the beginning of graph data was found, and the beginning and end
        # of axis definitions were found, and beginning is before end, and
        # overall length is greater than the end position, then the positions
        # are believable.  Return None if this isn't the case.
        if (posSog == -1 or posSog >= posSoax or posSoax == -1 or posEoax == -1 or
                posSoax >= posEoax or posEoax >= len(self._rawDataStr)):
            return None

        # good positions if we get here
        # Split the axis definition string by the AXIS_TOKEN split out each
        # definition
        dfnStrings = self._rawDataStr[posSoax + 1:posEoax].split(self.AXIS_TOKEN)
        # go through each definition and separate out the fields
        dfns = []
        for dfn in dfnStrings:
            dfns.append(tuple(dfn.split(self.AXIS_FIELD_TOKEN)))
        #return a list of axis field lists
        return tuple(dfns)

        # Break the data in to a list oddf sample sets. Each sample set is a list
        # of values, one value per axis.  The sample set values are in the same
        # order as the axis definitions.
    def _getAxisData(self):
        # make sure there is a start of graph data
        posSog = self._rawDataStr.find(self.SOG_TOKEN)
        # get the end of axis definition position. Data is next...
        posEoax = self._rawDataStr.find(self.EOAX_TOKEN)
        # get the end of the data position
        posEod = self._rawDataStr.find(self.EOD_TOKEN)
        # If the beginning of graph data was found, and the end
        # of axis definitions was found, and the end of the date was found,
        # and the beginning of the graph data is before the end of the axis
        # definitions, and end of the axis definitions is before the end of
        # the data, and the overall length is greater than the end of the
        # data position, then the positions are believable.
        # Return None if this isn't the case.
        if (posSog == -1 or posEoax == -1 or posEod == -1 or posSog >= posEoax or
                posEoax >= posEod or posEod >= len(self._rawDataStr)):
            return None

        # good positions if we get here
        # Split the data string by the DATA_SAMPLE_TOKEN to make a list of sample
        # strings
        sampleStrings = self._rawDataStr[posEoax + 1:posEod].split(self.DATA_SAMPLE_TOKEN)
        # The data is created with a data sample token after the last data sample,
        # so the split code above appends and empty sample set.  Remove this empty
        # sample by removing the last element from the sampleStrings list
        sampleStrings = sampleStrings[:-1]
        # go through each sample and separate out the values
        samples = []
        for sample in sampleStrings:
            samples.append(tuple(sample.split(self.DATA_AXIS_TOKEN)))
        #return a list of sample lists
        return tuple(samples)

    def __init__(self, rawDataStr):
        # make sure you can convert the raw data to a string. If so, get it.
        try:
            self._rawDataStr = str(rawDataStr)
            self._axisDfns = self._getAxisDfns()
            self._axisData = self._getAxisData()
        except ValueError as ve:
            print('The raw data must be a string or convertible to a string.')
            print(ve)
            quit()

    def __repr__(self):
        # __repr__ should create a 'representation that
        # should look like a valid Python Expression that could be used
        # to recreate an object with the same value.'
        # The goal of __repr__ is to be unambiguous.
        # Implement __repr__ for any class you implement.
        return self._rawDataStr

    def __str__(self):
        # The goal of __str__ is to create a string representation
        # of the object that is readable to a user (not a programmer).
        # Implement __str__ if you think it would be useful to have a string
        # version which errs on the side of readability in favor of more
        # ambiguity
        outputMsg=  '{:20}\n{}\n'.format('Axis Definitions: ', self._getAxisDfns())
        outputMsg+= '{:20}\n{}\n'.format('Data Definitions: ', self._getAxisData())
        return outputMsg

    # properties
    # return a tuple of tuples containing the definition of each axis
    @property
    def axisDefinitions(self):
        return self._axisDfns

    # return a tuple of tuples containing the data for all axes
    @property
    def axesData(self):
        return self._axisData

    # return a tuple containing the data for the specified axis (zero based).
    def getAxisData(self, axis=0):
        try:
            return tuple([float(samples[axis]) for samples in self._axisData])
        except IndexError:
            return None

