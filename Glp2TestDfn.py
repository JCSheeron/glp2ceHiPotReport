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
            self._steps = []
        else:
            # Make a config object, and read in the config file name.
            # The fileName should be a test definition, and the definition
            # files *.TPR use a format that is like a *.INI config file.
            self._config = configparser.ConfigParser()
            self._config.read(fileName, fileEncoding)
            self._numberOfSteps = self.GetNumOfSteps(constants.DFN_STEP_SECTION_PREFIX)
            # If there are steps defined, process them and create populated
            # test definition step objects.
            # init list of steps to an empty list. It will say empty if there 
            # is not at least one step.
            self._steps=[]
            if self._numberOfSteps > 0: # there is at least one step
                # there is at least one step. Loop thru, retreive the values
                # from the config object and make dfn step objects
                for step in range(1, self._numberOfSteps + 1):
                    sectionName = constants.DFN_STEP_SECTION_PREFIX + str(step)
                    self._steps.append(Glp2TestDfnStep(step, self._config.items(sectionName)))
            else: # there are not steps
                pass    # nothing to do!

    def __repr__(self):
        outputMsg=  '{:6} {}'.format('\nName: ', self.name + '\n')
        outputMsg+= '{:6} {}'.format('Test GUID: ', self.id + '\n')
        outputMsg+=  '{}'.format('Test Configuraiton:\n')
        outputMsg+= '{:17} {}'.format('Number of Steps: ', self._numberOfSteps + '\n')
        for step in self._steps:
            outputMsg += str(step)
#        # construct the config data into the message
#        for section in self._config:
#            outputMsg+= section + '\n'
#            for option in self._config[section]:
#                outputMsg+= '  ' + option + ':' + self._config[section][option] + '\n'
        return(outputMsg)

    # this function will determine how many steps are contained in the
    # test definition. Pass a defaulted setion prefix.
    def GetNumOfSteps(self, sectionPrefix=constants.DFN_STEP_SECTION_PREFIX):
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
    #def GetStepValues(self, sectionPrefix='TestS'
    # properties
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
            return(self._config([constants.DFN_GENERAL_SECTION][constants.DFN_GENSEC_COMMENTS_OPTNAME]))
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
    def numberOfSteps(self):
        return self._numberOfSteps

