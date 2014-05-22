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

@brief This module provides some basic functions for parsing spreadsheets/csv/tab deliminated files

The aim is to provide common utilities to format said file into a Pandas dataframe that is easily manipulatable by the
user. 

Have fun! 

@todos None for now!  Might want to make this into a class that wraps a dataframe. IDK.
"""

# -------------------------
# --- IMPORT AND GLOBAL ---
# -------------------------
import pandas as pd
import sys as sys
import numpy as np

# ------------
# --- import_excel ---
# ------------
def import_excel(fname, sheetname='PDIR_CMD',no_spaces=True):
    """@brief This function imports an excel spreadsheet, converts to a pandas dataframe.

    @param [fname]  String with filename and path of excel spreadsheet to open
    @param [sheetname='Sheet1'] Name of sheet to parse. 
    @param [no_spaces=True] Boolean indicator to remove spaces and fill with '_'
    
    @retval [data]  Pandas data frame

     \bExample
         \code data = import_excel("CMD_FILES/cmd_Jan_01_2001.xls")\endcode
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
    """@brief This function parses a CMD spreadsheet formatted as Excel spreadsheet.

    @param [fname]  String with filename and path of excel spreadsheet to open
    @param [no_spaces=True] Boolean indicator to remove spaces and fill with '_'
    
    @retval [data]  Pandas data frame

     \bExample
         \code data = import_csv("CMD_FILES/cmd_Jan_01_2001.csv")\endcode
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
    """@brief This function masks a dataframe, given a key-value pair

    Key/Value pair can be a string, or number. Logic handles both 
    NOTE that this works based on string.contains, not exact comparison. Take this into account   

    @param [dataframe: Pandas dataframe]  a pandas dataframe 
    @param [key: string] "key" accessing dataframe columns
    @param [value: string or numeric] the value you wish to mask by dataframe[key]
    
    @retval [data]  Masked pandas data frame

     \bExample
         \code data = mask(full_dataframe,"CMD_NAME","On") \endcode
    """
    
    if type(key) == str:
        return df.loc[(df[key]).apply(string.upper).str.contains()]

    return dataframe[dataframe[key] == value]

# ------------
# --- drop_columns ---
# ------------
def drop_columns(dataframe, drop_key="Unnamed"):
    """@brief Removes colums with names specified by input

    @param [dataframe: Pandas dataframe]  a pandas dataframe 
    @param [drop_key='Unnamed'] string indicating which dataframe columns to drop
    
    @retval [dataframe]  New dataframe with columns dropped

     \bExample
         \coded ata = drop_columns("Unnamed") \endcode
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
    """@brief This function is a simple utility to replace string patterns in colum names with something more helpful.
    By default, it replaces spaces in column names with underscores (just to make life easier)

    @param [dataframe: Pandas dataframe]  a pandas dataframe 
    @param [replace_this=" "] A string to be replaced in column names
    @param [with_this="_"] Replacement string when matches are found
    
    @retval [dataframe]  New dataframe with renamed columns

     \bExample
         \code dataframe = Parse.reformat_column_names(dataframe,replace_this="data.",with_this="data_") \endcode
    """
    dataframe.columns = [col.replace(replace_this, with_this) for col in dataframe.columns]
    return dataframe

