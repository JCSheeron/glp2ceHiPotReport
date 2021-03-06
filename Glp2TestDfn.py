#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# Glp2TestDfn.py
#
# imports
import Glp2Constants as constants
from Glp2TestDfnStep import Glp2TestDfnStep
#
# config file parser
import configparser

class Glp2TestDfn(object):
    # class constants

    def __init__(self, name, fileName=None, fileEncoding='UTF-8'):
        self._name = str(name) # use the string version

        # Get the config specified by the fileName
        if fileName is None:
            self._config = configparser.ConfigParser()
            self._numberOfSteps = 0
            self._steps = () # empty tuple
        else:
            # Make a config object, and read in the config file name.
            # The fileName should be a test definition, and the definition
            # files *.TPR use a format that is like a *.INI config file.
            self._fileName = fileName
            self._config = configparser.ConfigParser()
            self._config.read(fileName, fileEncoding)
            self._numberOfSteps = self._getNumOfSteps(constants.DFN_STEP_SECTION_PREFIX)
            # If there are steps defined, process them and create populated
            # test definition step objects.
            # init list of steps to an empty list. It will say empty if there
            # is not at least one step.
            steps=[]
            if self._numberOfSteps > 0: # there is at least one step
                # there is at least one step. Loop thru, retreive the values
                # from the config object and make dfn step objects
                for step in range(1, self._numberOfSteps + 1):
                    sectionName = constants.DFN_STEP_SECTION_PREFIX + str(step)
                    steps.append(Glp2TestDfnStep(step, self._config.items(sectionName)))
            else: # there are no steps
                pass    # nothing to do!

            # convert steps to a member tuple
            self._steps = tuple(steps)

    def __repr__(self):
        # TODO: Make output a dictionary or someting in line with the goal of __repr__
        # __repr__ should have an unambiguous output and create
        # a 'representation that should look like a valid Python
        # Epression that could be used to recreate an object with
        # the same value.'
        outputMsg=  '\n{:6} {}\n'.format('Name: ', self.name)
        outputMsg+= '{:6} {}\n'.format('Test GUID: ', self.dfnGuid)
        outputMsg+= '{:6} {}\n'.format('General generalComments: ', self.generalComments)
        outputMsg+= '{:17} {}\n'.format('Number of Steps: ', str(self.stepCount))
        outputMsg+=  '{}\n'.format('Test Steps:')
        for step in self._steps:
            outputMsg += str(step)
        # :TODO: :DEBUG:  May not want lengthy header and data. Bypass for now.
        return(outputMsg)
        outputMsg+=  '\n\n{}\n'.format('Entire Test Definition Configuration:')
        for section in self.config:
            outputMsg += '{}\n'.format(section)
            for option in self.config[section]:
                outputMsg += '{}{}{}{}\n'.format('  ', option, ':', self.config[section][option])
        return(outputMsg)

    def __str__(self):
        # The goal of __str__ is to create a string representation
        # of the object that is readable to a user (not a programmer).
        outputMsg=  '\n{:19} {}\n'.format('Name: ', self.name)
        outputMsg+= '{:19} {}\n'.format('Test GUID: ', self.dfnGuid)
        outputMsg+= '{:19} {}\n'.format('General Comments: ', self.generalComments)
        outputMsg+= '{:19} {}\n'.format('Name of Programmer: ', self.nameOfProgrammer)
        outputMsg+= '{:19} {}\n'.format('Number of Steps: ', str(self.stepCount))
        outputMsg+=  '\n{}\n'.format('Test Steps:')
        if self.countSteps > 0:
            for step in self._steps:
                outputMsg += str(step)
        else:
            outputMsg+= '  No Steps Defined!'
        return(outputMsg)


    # this function will determine how many steps are contained in the
    # test definition. Pass a defaulted setion prefix.
    # It is intended to be used internally to set the _numberOfSteps member
    def _getNumOfSteps(self, sectionPrefix=constants.DFN_STEP_SECTION_PREFIX):
        numOfSteps = 0
        stepNum = 1
        # construct section names and look for them until one isn't found
        # No do..while, so emulate with a while loop
        while True:
            sectionName = sectionPrefix + str(stepNum)
            if self._config.has_section(sectionName):
                numOfSteps += 1
                stepNum += 1
            else:
                return numOfSteps

    # properties
    @property
    def fileName(self):
        return self._fileName

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name = str(newName) # use the string version

    @property
    def dfnGuid(self):
        if self._config.has_option(constants.DFN_GENERAL_SECTION, constants.DFN_GENSEC_GUID_OPTNAME):
            return(self._config[constants.DFN_GENERAL_SECTION][constants.DFN_GENSEC_GUID_OPTNAME])
        else:
            return None

    @property
    def generalComments(self):
        if self._config.has_option(constants.DFN_GENERAL_SECTION,
                constants.DFN_GENSEC_COMMENTS_OPTNAME):
            return(self._config[constants.DFN_GENERAL_SECTION][constants.DFN_GENSEC_COMMENTS_OPTNAME])
        else:
            return None

    @property
    def nameOfProgrammer(self):
        if self._config.has_option(constants.DFN_GENERAL_SECTION, constants.DFN_GENSEC_NAME_OF_PROG_OPTNAME):
            return(self._config[constants.DFN_GENERAL_SECTION][constants.DFN_GENSEC_NAME_OF_PROG_OPTNAME])
        else:
            return None

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, newFile, fileEncoding='UTF-8'):
        self._config = configParser.ConfigParser()
        self._config.read(newFile, fileEncoding)

    @property
    def stepCount(self):
        return self._numberOfSteps

    # return the step data set (a tuple)
    @property
    def steps(self):
        return self._steps

    # Return a step given a step number. Step number is 1 based.
    # I.e. step = 1 is the 1st step is also self._steps[0]
    # Not a property since it has an argument
    def getStep(self, stepNo):
        step = int(stepNo)
        if step < 1 or step > self._numberOfSteps:
            # invalid step number
            return None
        else:
            #valid step number
            return self._steps[step - 1]

