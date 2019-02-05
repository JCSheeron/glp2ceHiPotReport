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
        outputMsg =  '{:19}{:<9}{:15}{:<36}'.format('\n\nStep Number: ', \
                self.stepNum, 'Step GUID: ', self.stepGuid)
        outputMsg += '{:19}{}'.format('\nStep Description: ', self.stepDescription)
        outputMsg += '{:18}{:<9}{:15}{:<36}'.format('\nStep Method: ', \
                self.stepMethod, 'Step Mode: ', self.stepMode)
        outputMsg += '{:18}{:<9}{:15}{:<36}'.format('\nCurrent Range: ', \
                self.currentRange, 'Current Limit: ', self.currentLimit)
        outputMsg += '{:18}{:<9.3f}{:15}{:<.3f}'.format('\nTest Time: ', \
                self.testTime, 'Ramp Time: ', self.rampTime)
        outputMsg += '{:18}{:<9}{:15}{:<36}'.format('\nDelay Time: ', \
                self.delayTime, 'Test Voltage: ', self.testVoltage)

        return(outputMsg)

    # properties
    @property
    def stepNum(self):
        return self._stepNum

    @stepNum.setter
    def stepNum(self, stepNum):
        # step number must be an integer, or something convertable to an integer
        try:
            self._stepNum = int(stepNum)
        except ValueError as ve:
            self._stepNum = None
            print('Error: When createing a test definition step, the step number \
must be an integer, or something convertable to an integer. Step number not set.')
            print(ve)

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
            return int(self._stepData.get(constants.DFN_STEP_MODE_OPTNAME.lower()))
        except ValueError as ve:
            return None

    @property
    def stepDescription(self):
        return str(self._stepData.get(constants.DFN_STEP_DESC_OPTNAME.lower()))

    @property
    def currentRange(self):
        return str(self._stepData.get(constants.DFN_STEP_CURR_RNG_OPTNAME.lower()))

    @property
    def currentLimit(self):
        try:
            return float(self._stepData.get(constants.DFN_STEP_CURR_LIM_OPTNAME.lower()))
        except ValueError as ve:
            return None

    @property
    def testTime(self):
        try:
            return float(self._stepData.get(constants.DFN_STEP_TEST_TIME_OPTNAME.lower()))
        except ValueError as ve:
            return None

    @property
    def rampTime(self):
        try:
            return float(self._stepData.get(constants.DFN_STEP_RAMP_TIME_OPTNAME.lower()))
        except ValueError as ve:
            return None

    @property
    def delayTime(self):
        try:
           return float(self._stepData.get(constants.DFN_STEP_DLY_TIME_OPTNAME.lower()))
        except ValueError as ve:
            return None

    @property
    def testVoltage(self):
        try:
            return float(self._stepData.get(constants.DFN_STEP_TEST_VOLT_OPTNAME.lower()))
        except ValueError as ve:
            return None

