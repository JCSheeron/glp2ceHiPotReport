#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# bpsCPdf.py
#
# imports
# pdf creation
from fpdf import FPDF
# managing fonts
import matplotlib.font_manager as fontmgr

# Extend the FPDF class to add a header and a footer.
# This class also contains a tuple of font names (fontNames) that can be
# compared with the default font names (defaultFontNames).
# If non-default fonts are used, they must first be added using add_font().
# If default font names are used, an add_font() call results in an error.
# Supply a desired header text.
# The footer text or page numbers are optional.  If a footerText is supplied,
# it will be printed. If the number of pages is fixed and known, and for
# whatever reason different than what will be calculated by FPDF (like pdf(s)
# being later appended), then the number of pages can be supplied, and it will
# be used in place of the auto figured value {nb}. If no footerText is supplied,
# then the footer will be "Page n of m". If footerText is supplied, it will
# override this page numbering message.
class cPdf(FPDF):
    def __init__(self, orientation, unit, format, headerText, footerText=None, totalPages=None):
        # init the base FPDF
        super().__init__(orientation=orientation, unit=unit, format=format)
        # define a tuple holding default font names
        # (regular mono, bold mono, regular proportional, bold proportional)
        # These are intended to be safe (read: always installed) fonts.
        self.defaultFontNames= ("Courier", "Courier", "Helvetica", "Helvetica")

       # Init the desired font names in a tuple
        # Get a font list
        fontList= fontmgr.findSystemFonts()
        self.fontNames= self.getFontNames(fontList)
        # Add non-default font names. Explicitly adding a default
        # font is an error.
        if self.fontNames[0] != self.defaultFontNames[0]:
            self.add_font(family="regularMono", style='',
                        fname=self.fontNames[0], uni=True)
        if self.fontNames[1] != self.defaultFontNames[1]:
            self.add_font(family="boldMono", style='',
                        fname=self.fontNames[1], uni=True)
        if self.fontNames[2] != self.defaultFontNames[2]:
            self.add_font(family="regularProp", style='',
                        fname=self.fontNames[2], uni=True)
        if self.fontNames[3] != self.defaultFontNames[3]:
            self.add_font(family="boldProp", style='',
                        fname=self.fontNames[3], uni=True)

        # capture the header text, and footer info
        self._headerText = str(headerText)
        if footerText is not None:
            self._footerText = str(footerText)
        else:
            self._footerText = None

        if totalPages is not None:
            self._totalPages = int(totalPages)
        else:
            self._totalPages = None

    # define the page header
    def header(self):
        # use the bold proportional font
        if self.fontNames[3] != self.defaultFontNames[3]:
            # non-default
            self.set_font("boldProp", '', 10)
        else:
            # default
            self.set_font(self.defaultFontNames[3], 'B', 10)

        # header text
        self.cell(20, -40, self._headerText)

        # set to regular proportional font
        if self.fontNames[2] != self.defaultFontNames[2]:
            # non-default
            self.set_font("regularProp", '', 10)
        else:
            # default
            self.set_font(self.defaultFontNames[2], '', 10)
        self.ln(10) # line break

    # define the page footer
    def footer(self):
        # use the regular proportional font
        if self.fontNames[2] != self.defaultFontNames[2]:
            # non-default
            self.set_font("regularProp", '', 10)
        else:
            # default
            self.set_font(self.defaultFontNames[2], '', 10)
        # position off the bottom
        self.set_y(-40)
        # If a message is displayed, use if for a footer.
        # If not, then print Page n of m. If totalPages is
        # supplied, then use it in place of the calculated value.
        if self._footerText is not None:
            # use supplied message for footer
            self.cell(20, 0, self._footerText)
        elif self._totalPages is None:
            # total pages not supplied, calculate it
            # print Page n of m
            # {nb} is magic. It is the total number of pages that gets updated
            # after the data pdf is created
            self.cell(20, 0, 'Page ' + str(self.page_no()) + ' of {nb}')
        else:
            # total pages is supplied. Use it rather than calculate it
            # print Page n of m
            self.cell(20, 0, 'Page ' + str(self.page_no()) + ' of ' + str(self._totalPages))

    # Create a function which, given a font list,
    # returns a tuple of font names for 4 fonts:
    # (regular mono, bold mono, regular prop, bold prop)
    def getFontNames(self, fontList):
        # Want to use a monospace font for the body text,
        # so the tables look good, but a proportional spaced font
        # for the headings. For non-standard fonts, it cannot be
        # assumed they are installed. In order of preference, try
        # source code pro, then DejaVuSansMono, then default to
        # Courier, which comes with pyfpdf.
        # For the porportional fonts, use Helvetica, which comes
        # with pyfpdf.
        #
        # Assume a list of avialable fonts is passed in.
        # *** Regular Mono Style
        fontShortName= 'SourceCodePro-Regular.ttf'
        # generator returning an iterable being accessed with next
        # This will return the path to the font install location
        # if it is installed, or come back with None.
        regularMonoName= next((font for font in fontList if fontShortName in font), None)
        if regularMonoName is None:
            # source code pro is not installed.
            # try DejaVu
            fontShortName= 'DejaVuSansMono.ttf'
            regularMonoName= next((font for font in fontList if fontShortName in font), None)
        if regularMonoName is None:
            # DejaVu Sans Mono not installed.
            # default to Courier
            regularMonoName= 'Courier'
        # *** Bold Mono Style
        fontShortName= 'SourceCodePro-Bold.ttf'
        # This will return the path to the font install location
        # if it is installed, or come back with None.
        boldMonoName= next((font for font in fontList if fontShortName in font), None)
        if boldMonoName is None:
            # source code pro is not installed.
            # try DejaVu
            fontShortName= 'DejaVuSansMono-Bold.ttf'
            boldMonoName= next((font for font in fontList if fontShortName in font), None)
        if boldMonoName is None:
            # DejaVu Sans Mono Bold not installed.
            # default to Courier
            boldMonoName= 'Courier'
        # *** Regular Proportional Style
        regularPropName= 'Helvetica'
        boldPropName= 'Helvetica'

        # return the tuple of font names
        return(regularMonoName, boldMonoName, regularPropName, boldPropName)

    # Given the width, height, and a string, determine how high the multi-cell
    # will be (auto line wrap).  Use the passed in unit and parameter so the 
    # calculated value takes into account the target font and unit.
    def GetMultiCellHeight(self, pdf, font_family, unit, w, h, txt, border = 0, align = 'J', fill = False):
        '''Return the height of a multi-cell given a height, width, and string.'''
        # Note that the border and align and fill are there to make the call
        # consistent with the multi_cell ctor.
        # This routine is a bit brute force:  Make a pdf and a multicell that
        # will never be seen, and calc and return the delta Y value.
        #
        # Get params from passed in pdf
        font_style = pdf.font_style
        font_size_pt = pdf.font_size_pt
        print('font family: ' + str(font_family))
        # make a local pdf
        tpdf = FPDF(format='letter', unit = unit)
        tpdf.add_page()
        #tpdf.set_font(font_family, font_style, font_size_pt)
        tpdf.set_font(font_family)
        startY = tpdf.get_y()
        tpdf.multi_cell(w, h, txt, border, align, fill)
        endY = tpdf.get_y()
        return (endY - startY)
