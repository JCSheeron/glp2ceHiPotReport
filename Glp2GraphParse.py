#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# Glp2GraphParse.py
#
# imports
#
    # 1) Search for beginning of graph string token
    # If beginning token is found, continue, else exit
    #
    # 2) Get substring contained between '<' and '>'. These
    # are the axis definitions.  Each axis has 6 delimited
    # with a '\', and the axes are separated from each other
    # with a '|'.
    # <axis 1 fields|axis 2 fields|...axis n fields>
    # Make a list of axis strings
    #
    # 3) The rest of the string after the closing '>' of the
    # axes definitions are the axis values. One value per axis,
    # each value separated with a '|', and each set of axis values
    # separated from the next set with a '\'
    # Strip off the remaining string as the data string.

class Glp2GraphParse(object):
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
        dfnStrings = self._rawDataStr[posSoax + 1:posEoax - 1].split(self.AXIS_TOKEN)
        # go through each definition and separate out the fields
        dfns = []
        for dfn in dfnStrings:
            dfns.append(dfn.split(self.AXIS_FIELD_TOKEN))
        #return a list of axis field lists
        return dfns

        # Break the data in to a list of sample sets. Each sample set is a list
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
        # go through each sample and separate out the values
        samples = []
        for sample in sampleStrings:
            samples.append(sample.split(self.DATA_AXIS_TOKEN))
        #return a list of sample lists
        return samples

    def __init__(self, rawDataStr):
        # make sure you can convert the raw data to a string. If so, get it.
        try:
            self._rawDataStr = str(rawDataStr)
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

#    # properties
#    @property
#    def prop_name(self):
#        return None
#
#    @prop_name.setter
#    def name(self, newName):
#        pass
