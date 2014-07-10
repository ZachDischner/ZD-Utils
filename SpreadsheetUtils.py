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

This module provides some basic functions for parsing spreadsheets/csv/tab deliminated files

The aim is to provide common utilities to format said file into a Pandas dataframe that is easily manipulatable by the
user. 

Have fun! 

Todos:
     None for now!  Might want to make this into a class that wraps a dataframe. IDK.
"""

# -------------------------
# --- IMPORT AND GLOBAL ---
# -------------------------
import pandas as pd
import sys as sys
import numpy as np
import stringlksjd

# ------------
# --- import_excel ---
# ------------
def import_excel(fname, sheetname='PDIR_CMD',no_spaces=True):
    """This function imports an excel spreadsheet, converts to a pandas dataframe.

    Args:
        fname:  String with filename and path of excel spreadsheet to open

    Kwargs:
        sheetname:  Name of sheet to parse. 
        no_spaces:  Boolean indicator to remove spaces and fill with '_'
    
    Returns:
        data:   Pandas data frame

    Example:
        data = import_excel("CMD_FILES/cmd_Jan_01_2001.xls")
    """
    data = pd.read_excel(fname, sheetname, header=1)
    if no_spaces is True:
        data = reformat_column_names(data)
    # Drop "Unnamed" columns, artifact of csv spreadsheet
    data = drop_columns(data)

    return data


# ------------
# --- import_csv ---
# ------------
def import_csv(fname, no_spaces=True):
    """This function parses a CMD spreadsheet formatted as Excel spreadsheet.

    Args:
        fname:  String with filename and path of excel spreadsheet to open

    Kwargs:
        no_spaces:  Boolean indicator to remove spaces and fill with '_'
    
    Returns:
        data:   Pandas data frame

    Example:
        data = import_csv("CMD_FILES/cmd_Jan_01_2001.csv")\endcode
    """
    data = pd.read_csv(fname, header=1)
    # Reformat column indices to replace spaces with underscores
    if no_spaces is True:
        data = reformat_column_names(data)
    # Drop "Unnamed" columns, artifact of csv export
    data = drop_columns(data)

    return data


# ------------
# --- mask ---
# ------------
def mask(dataframe, key, value):
    """This function masks a dataframe, given a key-value pair

    Key/Value pair can be a string, or number. Logic handles both. 
    Logic reads like: 'Return a dataframe subset of the original dataframe where the dataframe.key == value' 
    NOTE that this works based on string.contains, not exact comparison. Take this into account   

    Args:
        dataframe:      Pandas Dataframe to apply the mask on
        key:            "key" accessing dataframe columns
        value:          (string or numeric) the value you wish to mask by dataframe[key]
    
    Returns:
        data:   Masked pandas data frame

    Todos:
        Refactor with a new match_condition() function or something that does this:
            return True in [fnmatch.fnmatch(alice.COMMAND.iloc[0],match_key) for match_key in start_condition]

    Example:
        data = mask(full_dataframe,"CMD_NAME","On")
    """
    
    if type(key) == str:
        return dataframe.loc[(dataframe[key]).apply(string.upper).str.contains(value)]

    return dataframe[dataframe[key] == value]

# ------------
# --- drop_columns ---
# ------------
def drop_columns(dataframe, drop_key="Unnamed"):
    """Removes colums with names specified by input

    Args:
        dataframe:  Pandas dataframe 

    Kwargs:
        drop_key:   string indicating which dataframe columns to drop
    
    Returns:
        dataframe:  New dataframe with columns dropped

    Example:
        data = drop_columns("Unnamed") 
    """
    dcols = dataframe.columns
    for col in dcols:
        if col.find(drop_key) >= 0:
            dataframe = dataframe.drop(col, axis=1)
    return dataframe


# ------------
# --- reformat_column_names ---
# ------------
def reformat_column_names(dataframe, replace_this=" ", with_this="_"):
    """This function is a simple utility to replace string patterns in colum names with something more helpful.
    By default, it replaces spaces in column names with underscores (just to make life easier)

    Args:
        dataframe:  A pandas dataframe 

    Kwargs:
        replace_this:   A string to be replaced in column names
        with_this:      Replacement string when matches are found
    
    Returns:
        dataframe:  New dataframe with renamed columns

    Example:
        dataframe = Parse.reformat_column_names(dataframe,replace_this="data.",with_this="data_")
    """
    dataframe.columns = [col.replace(replace_this, with_this) for col in dataframe.columns]
    return dataframe

