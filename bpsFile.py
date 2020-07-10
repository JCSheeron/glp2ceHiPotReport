#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# bpsFile.py
# OS and File related functions
#   listFiles(path) -- return a list of files in a given path, excluding directories.
#
from os import listdir
from os.path import isfile, join
def listFiles(path):
    '''return a list of files in a given path, excluding directories.'''
    # Make sure path has something in it.
    try:
        path = str(path)
    except ValueError as ve:
        print('The sepcified path must be convertable to a string.')
        print(ve)
        return None

    if path == '' or path is None:
        print('The specified path must be specified, and not be an empty string.')
        return None

    # if we get here, path at least is a string with something in it.  Assume
    # it is valid and use it.
    return [f for f in listdir(path) if isfile(join(path,f))]
