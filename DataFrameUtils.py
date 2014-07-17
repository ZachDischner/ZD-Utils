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
import string

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

def saveDataFrame(dataframe, savedir='Output/', filenameNoExt="DataframeData", to_csv=True, to_html=False, to_Excel=False):
    """Saves dataframes in a variety of formats. 

    Save single dataframe as csv or HTML, or pass in a dictionary of dataframes to put all dataframes into an
    Excel file with each frame on a different sheet.

    Args:
        dataframe:  Dataframe datastructures

    Kwargs:
        savedir:        Locally referenced file to place output files in
        filenameNoExt:  Template filename. I.E. 'myresults', not 'myresults.xlsx'
        to_csv:         Save data to csv file
        to_html:        Save data to html file, opens as a table in your browser
        to_Excel:       Save to excel spreadsheet (ick)


    Examples:
        df1=pd.DataFrame({'a':['foo','bar'],'b':['sarah','ryan']})
        df2=pd.DataFrame({'c':[99,100],'d':[4444444,-2]})
        df_dict = dict{'foo':df1, 'bar':df2}
        saveDataFrame(df_dict,to_Excel=True,to_csv=False,filenameNoExt='myfile')
        saveDataFrame(df1,to_csv=True,to_html=True,filenameNoExt='df1')
    """
    if to_Excel:
        writer=pd.ExcelWriter(savedir+filenameNoExt + ".xlsx")
        if type(dataframe) is pd.DataFrame: ## I'd Rather you passed in a dictionary...
            dataframe.to_excel(writer,'Sheet1')
        elif type(dataframe) is dict:
            [dataframe[sheetname].to_excel(writer,sheetname) for idx,sheetname in enumerate(dataframe)]
            writer.close()
        else:
            raise Warning("Unknown datatype bro!")

    if to_csv:
        if type(dataframe) is not pd.DataFrame:
            raise Warning("ERROR must pass a dataframe for saving not: " + str(type(dataframe)))
        dataframe.to_csv(savedir+filenameNoExt+".csv")

    if to_html:
        if type(dataframe) is not pd.DataFrame:
            raise Warning("ERROR must pass a dataframe for saving not: " + str(type(dataframe)))
        dataframe.to_html(savedir+filenameNoExt+".html")

