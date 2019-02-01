#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# Glp2TestDfn.py
#
# imports
#
# config file parser
import configparser

class Glp2TestDfn(object):
    def __init__(self, name, fileName=None, fileEncoding='UTF-8'):
        self._name = str(name) # use the string version

        # Get the config specified by the fileName
        if fileName is None:
            self._config = configparser.ConfigParser()
            self._numberOfSteps = 0
        else:
            self._config = configparser.ConfigParser()
            self._config.read(fileName, fileEncoding)
            self._numberOfSteps = self.GetNumOfSteps()




    def __repr__(self):
        outputMsg=  '{:6} {}'.format('\nName: ', self.name + '\n')
        outputMsg+= '{:6} {}'.format('Id: ', self.id)
        outputMsg+=  '{}'.format('\nConfiguraiton:\n')
        outputMsg+= '{:17} {}'.format('\nNumber of Steps: ', self._numberOfSteps)
#        # construct the config data into the message
#        for section in self._config:
#            outputMsg+= section + '\n'
#            for option in self._config[section]:
#                outputMsg+= '  ' + option + ':' + self._config[section][option] + '\n'
        return(outputMsg)

    # this function will determine how many steps are contained in the
    # test definition. Pass a defaulted setion prefix.
    def GetNumOfSteps(self, sectionPrefix='TestStep'):
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
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name = str(newName) # use the string version

    @property
    def id(self):
        if self._config.has_option('General Data', 'GUID'):
            return(self._config['General Data']['GUID'])
        else:
            return None

    @property
    def generalComments(self):
        if self._config.has_option('General Data', 'Comments'):
            return(self._config['General Data']['Comments'])
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

