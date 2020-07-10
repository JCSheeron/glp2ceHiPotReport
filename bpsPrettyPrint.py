#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# bpsPrettyPrint.py
# Functions related to printing out things that look nice.

def listPrettyPrint2Col(foolist, width=45):
    '''Print a list in two columns, given a column width.'''
    # the passed in thing must be a list, or convertable to one
    try:
        lst = list(foolist)
    except ValueError as ve:
        print('First parameter passed to listPrettyPrint2Col must be a list, \
or something convertable to a list.')
        print(ve)
        return

    try:
        w = int(width)
    except ValueError as ve:
        print('Second parameter passed to listPrettyPrint2Col must be an integer, \
or something convertable to an integer.')
        print(ve)
        return

    # now print the list in two columns
    for c1, c2 in zip(lst[::2], lst[1::2]):
        print('{:<{width}}{:<}'.format(c1, c2, width=w))

def listPrettyPrint2ColStr(foolist, width=45):
    '''Produce a string list in two columns, given a column width.'''
    # the passed in thing must be a list, or convertable to one
    try:
        lst = list(foolist)
    except ValueError as ve:
        print('First parameter passed to listPrettyPrint2Col must be a list, \
or something convertable to a list.')
        print(ve)
        return str(foolist)

    try:
        w = int(width)
    except ValueError as ve:
        print('Second parameter passed to listPrettyPrint2Col must be an integer, \
or something convertable to an integer.')
        print(ve)
        return str(foolist)

    # now print the list in two columns
    listStr = ''
    for c1, c2 in zip(lst[::2], lst[1::2]):
        listStr += ('\n{:<{width}}{:<}'.format(c1, c2, width=w))
    return listStr

def listPrettyPrint3Col(foolist, width=30):
    '''Print a list in three columns, given a column width.'''
    # the passed in thing must be a list, or convertable to one
    try:
        lst = list(foolist)
    except ValueError as ve:
        print('First parameter passed to listPrettyPrint2Col must be a list, \
or something convertable to a list.')
        print(ve)
        return

    try:
        w = int(width)
    except ValueError as ve:
        print('Second parameter passed to listPrettyPrint2Col must be an integer, \
or something convertable to an integer.')
        print(ve)
        return

    # now print the list in three columns
    for c1, c2, c3 in zip(lst[::3], lst[1::3], lst[2::3]):
        print('{:<{width}}{:<{width}}{:<}'.format(c1, c2, c3, width=w))

def listPrettyPrint3ColStr(foolist, width=30):
    '''Produce a string list in three columns, given a column width.'''
    # the passed in thing must be a list, or convertable to one
    try:
        lst = list(foolist)
    except ValueError as ve:
        print('First parameter passed to listPrettyPrint2Col must be a list, \
or something convertable to a list.')
        return str(foolist)

    try:
        w = int(width)
    except ValueError as ve:
        print('Second parameter passed to listPrettyPrint2Col must be an integer, \
or something convertable to an integer.')
        print(ve)
        return str(foolist)

    # now print the list in three columns
    listStr = ''
    for c1, c2, c3 in zip(lst[::3], lst[1::3], lst[2::3]):
        listStr += ('\n{:<{width}}{:<{width}}{:<}'.format(c1, c2, c3, width=w))
    return listStr

