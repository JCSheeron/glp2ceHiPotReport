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
            self._id = None
        else:
            self._config = configparser.ConfigParser()
            self._config.read(fileName, fileEncoding)
            if self._config.has_option('General Data', 'GUID'):
                self._id = self._config['General Data']['GUID']
            else:
                self._id = 'No GUID found'

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

