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
    # Make a list of axis stirngs
    #
    # 3) The rest of the string after the closing '>' of the
    # axes definitions are the axis values. One value per axis,
    # each value separated with a '|', and each set of axis values
    # separated from the next set with a '\'
    # Strip off the retmaining string as the data string.
    pass

class Glp2GraphParse(object):
    # class constants
    SOG_TOKEN = '|#GR#|'    # Denote Start of the graph
    SOAX_TOKEN = '<'        # Denote the start of axis definition(s)
    EOAX_TOKEN = '>'        # Denote the end of axis definition(s)


    # find the position of the beginning of the graph data (i.e. return the
    # position of the start of graph (SOG) string token. return value is zero based for the
    # beginning of the string, and -1 if not found.
    def _posSOG():
        return self._rawDataStr.find(SOG_TOKEN)

    def _getAxisDfns():
        # get start and end of axis definition positions.
        posSoax = self._rawDataStr.find(SOAX_TOKEN)
        posEoax = self._rawDataStr.find(EOAX_TOKEN)
        lenAx = 
        # If beginning and end were found, and beginning is before end, and
        # overall length is greater than the end position, the the positions 
        # are believable.  Return the substring that defines the axes else
        # return None.
        if posSoax > -1 and posEoax > -1 and posSoax < posEoax and posEoax < len(self._rawDataStr):
            # believable positions. Return the sub string
            return self._rawDataStr[posSoax + 1:posEoax]
        else:
            return None

    def

    def __init__(self, rawDataStr):
        # make sure you can convert the raw data to a string. If so, get it.
        try:
            self._rawDataStr = str(rawDataStr)
        except ValueError as ve:
            print('The raw data must be a string or convertable to a string.')
            print(ve)
            quit()

    def __repr__(self):
        # __repr__ should create a 'representation that
        # should look like a valid Python Expression that could be used
        # to recreate an object with the same value.'
        # The goal of __repr__ is to be unambiguous.
        # Implement __repr__ for any class you implement.
        pass

    def __str__(self):
        # The goal of __str__ is to create a string representation
        # of the object that is readable to a user (not a programmer).
        # Implement __str__ if you think it would be useful to have a string
        # version which errs on the side of readability in favor of more
        # ambiguity
        pass

    # properties
    @property
    def prop_name(self):
        return None

    @prop_name.setter
    def name(self, newName):
        pass
