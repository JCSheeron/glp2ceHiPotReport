#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# Glp2TestDfn.py
#
#
# TODO: Get values and definitions for step method, and mode
# imports
#
class Glp2TestDfnStep(object):
    def __init__(self, stepNum=None, stepGuid=None, stepMethod=None,
                 stepMode=None, stepDescription=None, currentRange=None,
                 currentLimit=None, testTime=None, rampTime=None, delayTime=None,
                 testVoltage=None ):
        try:
            self._stepNum = int(stepNum)
        except ValueError as ve:
            print('Error: When creating a test definition step, the test number \
must be an integer, or something convertable to an integer. Step number not set.')
            self._stepNum = None
            print(ve)

        try:
            self._stepGuid = str(stepGuid)
        except ValueError as ve:
            print('Error: When creating a test definition step, the step GUID \
must be a string, or something convertable to a string. Step GUID not set.')
            self._stepGuid = None
            print(ve)

        try:
            self._stepMethod = int(stepMethod)
        except ValueError as ve:
            print('Error: When creating a test definition step, the step method \
must be an integer, or something convertable to an integer. Step method not set.')
            self._Method = None
            print(ve)

        try:
            self._stepMode = int(stepMode)
        except ValueError as ve:
            print('Error: When creating a test definition step, the step mode \
must be an integer, or something convertable to an integer. Step mode not set.')
            self._stepMode = None
            print(ve)

        try:
            self._stepDescription = str(stepDescription)
        except ValueError as ve:
            print('Error: When creating a test definition step, the step description \
must be a string, or something convertable to a string. Step description not set.')
            self._stepDescription = None
            print(ve)

        try:
            self._currentRange = str(currentRange)
            # TODO: derive and store current units from the given limit (mA, uA, etc)
        except ValueError as ve:
            print('Error: When creating a test definition step, the current range \
must be a string, or something convertable to a string. Current range not set.')
            self._currentRange = None
            print(ve)

        try:
            self._currentLimit = float(currentLimit)
        except ValueError as ve:
            print('Error: When creating a test definition step, the current limit\
must be a floating point value or something convertable to a floating point value. \
Current limit not set.')
            self._currentLimit= None
            print(ve)

        try:
            self._testTime = float(testTime)
        except ValueError as ve:
            print('Error: When creating a test definition step, the test time \
must be a floating point value or something convertable to a floating point value. \
Test time not set.')
            self._testTime = None
            print(ve)

        try:
            self._rampTime = float(rampTime)
        except ValueError as ve:
            print('Error: When creating a test definition step, the ramp time \
must be a floating point value or something convertable to a floating point value. \
Ramp time not set.')
            self._rampTime = None
            print(ve)

        try:
            self._delayTime = float(delayTime)
        except ValueError as ve:
            print('Error: When creating a test definition step, the delay time \
must be a floating point value or something convertable to a floating point value. \
Delay time not set.')
            self._delayTime = None
            print(ve)

        try:
            self._testVoltage = float(testVoltage)
        except ValueError as ve:
            print('Error: When creating a test definition step, the test voltage \
must be a floating point value or something convertable to a floating point value. \
Test voltage not set.')
            self._testVoltage = None
            print(ve)



    def __repr__(self):
        outputMsg =  '{:15} {:6} {:15} {:36}'.format('\nStep Number: ', \
                self.stepNum, 'Step GUID: ', self.stepGuid)
        outputMsg += '{:18} {}'.format('\nStep Description: ', self.stepDescription)
        outputMsg += '{:15} {:6} {:15} {:36}'.format('\nStep Method: ', \
                self.stepMethod, 'Step Mode: ', self.stepMode)
        outputMsg += '{:15} {:6} {:15} {:36}'.format('\nCurrent Range: ', \
                self.currentRange, 'Current Limit: ', self.currentLimit)
        outputMsg += '{:15} {:6} {:15} {:36}'.format('\nTest Time: ', \
                self.testTime, 'Ramp Time: ', self.rampTime)
        outputMsg += '{:15} {:6} {:15} {:36}'.format('\nDelay Time: ', \
                self.delayTime, 'Test Voltage: ', self.testVoltage)

        return(outputMsg)

    # properties
    @property
    def stepNum(self):
        return self._stepNum

    @stepNum.setter
    def stepNum(self, stepNum):
        try:
            self._stepNum = int(stepNum)
        except ValueError as ve:
            print('Error: When setting the test definition step number, the step number \
must be an integer, or something convertable to an integer. Step number not set.')
            self._stepNum = None
            print(ve)

    @property
    def stepGuid(self):
        return self._stepGuid

    @stepGuid.setter
    def stepGuid(self, stepGuid):
        try:
            self._stepGuid = str(stepGuid)
        except ValueError as ve:
            print('Error: When setting the definition step GUID, the step GUID \
must be a string, or something convertable to a string. Step GUID not set.')
            self._stepGuid = None
            print(ve)

    @property
    def stepMethod(self):
        return self._stepMethod

    @stepMethod.setter
    def stepMethod(self, stepMethod):
        try:
            self._stepMethod = int(stepMethod)
        except ValueError as ve:
            print('Error: When setting the test definition step method, the step method \
must be an integer, or something convertable to an integer. Step method not set.')
            self._Method = None
            print(ve)

    @property
    def stepMode(self):
        return self._stepMode

    @stepMode.setter
    def stepMode(self, stepMode):
        try:
            self._stepMode = int(stepMode)
        except ValueError as ve:
            print('Error: When setting the test definition step mode, the step mode \
must be an integer, or something convertable to an integer. Step mode not set.')
            self._stepMode = None
            print(ve)

    @property
    def stepDescription(self):
        return self._stepDescription

    @stepDescription.setter
    def stepDescription(self, stepDescription):
        try:
            self._stepDescription = str(stepDescription)
        except ValueError as ve:
            print('Error: When setting the test definition step description, the step description \
must be a string, or something convertable to a string. Step description not set.')
            self._stepDescription = None
            print(ve)

    @property
    def currentRange(self):
        return self._currentRange

    @currentRange.setter
    def currentRange(self, currentRange):
        try:
            self._currentRange = str(currentRange)
            # TODO: derive and store current units from the given limit (mA, uA, etc)
        except ValueError as ve:
            print('Error: When setting the test definition current range, the current range \
must be a string, or something convertable to a string. Current range not set.')
            self._currentRange = None
            print(ve)

    @property
    def currentLimit(self):
        return self._currentLimit

    @currentLimit.setter
    def currentLimit(self, currentLimit):
        try:
            self._currentLimit = float(currentLimit)
        except ValueError as ve:
            print('Error: When creating a test definition step, the current limit\
must be a floating point value or something convertable to a floating point value. \
Current limit not set.')
            self._currentLimit= None
            print(ve)

    @property
    def testTime(self):
        return self._testTime

    @testTime.setter
    def testTime(self, testTime):
        try:
            self._testTime = float(testTime)
        except ValueError as ve:
            print('Error: When setting the test definition test time, the test time \
must be a floating point value or something convertable to a floating point value. \
Test time not set.')
            self._testTime = None
            print(ve)

    @property
    def rampTime(self):
        return self._rampTime

    @rampTime.setter
    def rampTime(self, rampTime):
        try:
            self._rampTime = float(rampTime)
        except ValueError as ve:
            print('Error: When setting the test definition rampt time, the ramp time \
must be a floating point value or something convertable to a floating point value. \
Ramp time not set.')
            self._rampTime = None
            print(ve)

    @property
    def delayTime(self):
        return self._delayTime

    @delayTime.setter
    def delayTime(self, delayTime):
        try:
            self._delayTime = float(delayTime)
        except ValueError as ve:
            print('Error: When setting the test definition delay time, the delay time \
must be a floating point value or something convertable to a floating point value. \
Delay time not set.')
            self._delayTime = None
            print(ve)

    @property
    def testVoltage(self):
        return self._testVoltage

    @testVoltage.setter
    def testVoltage(self, testVoltage):
        try:
            self._testVoltage = float(testVoltage)
        except ValueError as ve:
            print('Error: When creating a test definition test voltage, the test voltage \
must be a floating point value or something convertable to a floating point value. \
Test voltage not set.')
            self._testVoltage = None
            print(ve)

