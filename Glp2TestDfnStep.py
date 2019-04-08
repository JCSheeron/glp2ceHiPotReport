#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# Glp2TestDfn.py
#
#
# TODO: Get values and definitions for step method, and mode. Probably use
# a dictionary or some sort of enumeration to give values meaningful names.
#
# imports
import Glp2Constants as constants
#
class Glp2TestDfnStep(object):
    def __init__(self, stepNum, data=None):

        # step number must be an integer, or something convertable to an integer
        try:
            self._stepNum = int(stepNum)
        except ValueError as ve:
            self._stepNum = None
            print('Error: When createing a test definition step, the step number \
must be an integer, or something convertable to an integer. Step number not set.')
            print(ve)

        if data is not None: # data specified
            # data must be a dictionary, or something convertable to a dictionary
            try:
                self._stepData = dict(data)
            except ValueError as ve:
                self._stepData = None
                print('Error: When creating a test definition step, the data \
must be a dictionary, or something convertable to an dictionary. Step data not set.')
                print(ve)
        else: # no data specified
            self._stepData = None

    def __repr__(self):
        # TODO: Make output a dictionary or someting in line with the goal of __repr__
        # __repr__ should have an unambiguous output and create
        # a 'representation that should look like a valid Python
        # Epression that could be used to recreate an object with
        # the same value.'
        outputMsg =  '\n{:19}{:<9}{:15}{:<36}'.format('Step Number: ', \
                self.stepNum, 'Step GUID: ', self.stepGuid)
        outputMsg += '\n{:19}{}'.format('Step Description: ', self.stepDescription)
        outputMsg += '\n{:18}{:<9}{:15}{:<36}'.format('Step Method: ', \
                self.stepMethod, 'Step Mode: ', self.stepMode)
        outputMsg += '\n{:18}{:<9}{:15}{:<36}'.format('Current Range: ', \
                self.currentRange, 'Current Limit: ', self.currentLimit)
        outputMsg += '\n{:18}{:<9.3f}{:15}{:<.3f}'.format('Test Time: ', \
                self.testTime, 'Ramp Time: ', self.rampTime)
        outputMsg += '\n{:18}{:<9}{:15}{:<36}\n'.format('Delay Time: ', \
                self.delayTime, 'Test Voltage: ', self.testVoltage,)
        outputMsg += '\n\nRaw Step Data:'
        for key in self.stepData:
            outputMsg += '\n' + key + ': ' + self.stepData[key]
        return(outputMsg)

    def __str__(self):
        # The goal of __str__ is to create a string representation
        # of the object that is readable to a user (not a programmer).
        outputMsg =  '{:18}{:<9}{:15}{:<36}'.format('Step Number: ', \
                self.stepNum, 'Step GUID: ', self.stepGuid)
        outputMsg += '\n{:18}{}'.format('Step Description: ', self.stepDescription)
        outputMsg += '\n{:18}{:<9}{:15}{:<36}'.format('Step Method: ', \
                self.stepMethod, 'Step Mode: ', self.stepMode)
        outputMsg += '\n{:18}{:<9}{:15}{:<36}'.format('Current Range: ', \
                self.currentRange, 'Current Limit: ', self.currentLimit)
        outputMsg += '\n{:18}{:<9.3f}{:15}{:<.3f}'.format('Test Time: ', \
                self.testTime, 'Ramp Time: ', self.rampTime)
        outputMsg += '\n{:18}{:<9}{:15}{:<36}\n\n'.format('Delay Time: ', \
                self.delayTime, 'Test Voltage: ', self.testVoltage,)
        return(outputMsg)
    # properties
    @property
    def stepNum(self):
        return self._stepNum

    @stepNum.setter
    def stepNumber(self, stepNum):
        # step number must be an integer, or something convertable to an integer
        try:
            self._stepNum = int(stepNum)
        except ValueError as ve:
            self._stepNum = None
            print('Error: When createing a test definition step, the step number \
must be an integer, or something convertable to an integer. Step number not set.')
            print(ve)

    @property
    def stepData(self):
        return self._stepData

    @property
    def stepGuid(self):
        # returned option names are all lower case
        return str(self._stepData.get(constants.DFN_STEP_GUID_OPTNAME.lower()))

    @property
    def stepMethod(self):
        # returned option names are all lower case
        try:
            return int(self._stepData.get(constants.DFN_STEP_METHOD_OPTNAME.lower()))
        except ValueError as ve:
            return None

    @property
    def stepMode(self):
        try:
            # returned option names are all lower case
            return int(self._stepData.get(constants.DFN_STEP_MODE_OPTNAME.lower()))
        except ValueError as ve:
            return None

    @property
    def stepDescription(self):
        # returned option names are all lower case
        return str(self._stepData.get(constants.DFN_STEP_DESC_OPTNAME.lower()))

    @property
    def currentRange(self):
        # returned option names are all lower case
        return str(self._stepData.get(constants.DFN_STEP_CURR_RNG_OPTNAME.lower()))

    @property
    def currentLimit(self):
        try:
            # returned option names are all lower case
            return float(self._stepData.get(constants.DFN_STEP_CURR_LIM_OPTNAME.lower()))
        except ValueError as ve:
            return None

    @property
    def testTime(self):
        try:
            # returned option names are all lower case
            return float(self._stepData.get(constants.DFN_STEP_TEST_TIME_OPTNAME.lower()))
        except ValueError as ve:
            return None

    @property
    def rampTime(self):
        try:
            # returned option names are all lower case
            return float(self._stepData.get(constants.DFN_STEP_RAMP_TIME_OPTNAME.lower()))
        except ValueError as ve:
            return None

    @property
    def delayTime(self):
        try:
            # returned option names are all lower case
           return float(self._stepData.get(constants.DFN_STEP_DLY_TIME_OPTNAME.lower()))
        except ValueError as ve:
            return None

    @property
    def testVoltage(self):
        try:
            # returned option names are all lower case
            return float(self._stepData.get(constants.DFN_STEP_TEST_VOLT_OPTNAME.lower()))
        except ValueError as ve:
            return None

