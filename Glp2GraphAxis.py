#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# ClassName.py
#
# imports
#
# config file parser

class ClassName(object):
    # class constants
    # (none)


    def __init__(self, param):
        pass

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
