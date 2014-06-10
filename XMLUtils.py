##! /usr/bin/python
__author__ = 'Zach Dischner'
__copyright__ = "NA"
__credits__ = ["NA"]
__license__ = "NA"
__version__ = "1.0.0"
__maintainer__ = "Zach Dischner"
__email__ = "zach.dischner@gmail.com"
__status__ = "Dev"

"""
File name: SpreadsheetUtils.py
Authors: Zach Dischner
Created: 1/1/2014
Modified: 5/21/2015

This module wraps some useful functions I've come up with and stumbled across for XML file manipulation


Todos: Fill er up
"""


#http://norwied.wordpress.com/2013/08/27/307/
def indent(elem, level=0):
    """ Makes ElementTree XML object pretty for printing

    Args:
        elem:  object to prettify

    Kwargs:
        level: Internally used

    Example:
        root = ET.ElementTree("SomeFile.xml")
        XML_Utils.indent(root)
    """
    i = "\n" + level*"    "

    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "    "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i