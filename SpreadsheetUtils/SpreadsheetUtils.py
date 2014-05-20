__author__ = 'zachdischner'
#
# File name: SpreadsheetUtils.py
# Authors: Zach Dischner
# Created: 5/14/2014
#
# Description:
#   Utilities for dealing with spreadsheets. Yay.
#
# Function List:
#
#
# Todos:
#
#


# -------------------------
# --- IMPORT AND GLOBAL ---
# -------------------------
import pandas as pd
import sys as sys
import numpy as np

# ------------
# --- import_CMD_sheet ---
# ------------
def import_CMD_sheet(fname, sheetname='PDIR_CMD', no_spaces=True):
    """This function parses a CMD spreadsheet formatted as Excel spreadsheet.
    Run: 'help(import_CMD_sheet)' in interactive mode to print this statement out
    Input:  fname - string with filename and path of excel spreadsheet to open
    Returns: data - Pandas data frame

    Example: data = import_excel("CMD_FILES/cmd_Jan_01_2001.xls")
    """
    data = pd.read_excel(fname, sheetname, header=1)
    if no_spaces is True:
        data = reformat_column_names(data)
    return data


# ------------
# --- import_excel ---
# ------------
def import_excel(fname, sheetname='PDIR_CMD',no_spaces=True):
    """This function parses a CMD spreadsheet formatted as Excel spreadsheet.
    Run: 'help(import_excel)' in interactive mode to print this statement out
    Input:  fname - string with filename and path of excel spreadsheet to open
    Returns: data - Pandas data frame

    Example: data = import_excel("CMD_FILES/cmd_Jan_01_2001.xls")
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
    """This function parses a CMD spreadsheet formatted as csv.
    Run: 'help(parst_csv)' in interactive mode to print this statement out
    Input: fname - string with filename and path of csv to open
    Returns: data - Pandas data frame

    Example: data = import_csv("CMD_FILES/cmd_Jan_01_2001.csv")
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
# *Objectify this?, get rid of the "dataframe" argument
def mask(dataframe, key, value):
    """This function masks a dataframe, given a key-value pair
    Run: 'help(mask)' in interactive mode to print this statement out
    Input:  dataframe - a pandas dataframe containing all or part of a CMD spreadsheet
            key - "key" accessing dataframe columns
            value - the value that you wish to mask by dataframe[key]
    Returns: dataframe - Pandas data frame

    Example: data = mask(full_dataframe,"CMD_NAME","On")
    """
    return dataframe[dataframe[key] == value]

# ------------
# --- drop_columns ---
# ------------
def drop_columns(dataframe, matching="Unnamed"):
    """Removes colums with names matching the 'matching' input
    Run: 'help(drop_columns)' in interactive mode to print this statement out
    Input:  matching (op) - string indicating with dataframe colums are to be dropped
    Returns: dataframe - Pandas data frame

    Example: data = drop_columns("Unnamed")
            # Removes all columns that look like "Unnamed*"
    """
    dcols = dataframe.columns
    for col in dcols:
        if col.find("Unnamed") >= 0:
            dataframe = dataframe.drop(col, axis=1)
    return dataframe


# ------------
# --- reformat_column_names ---
# ------------
def reformat_column_names(dataframe, replace_this=" ", with_this="_"):
    """This function is a simple utility to replace string patterns in colum names with something more helpful.
    By default, it replaces spaces in column names with underscores (just to make life easier)
    Run: 'help(reformat_column_names)' in interactive mode to print this statement out
    Input:      *dataframe      - dataframe to manipulate
                *(replace_this) - string to search for
                *(with_this)    - replacement string when matches are found

    Returns:    *dataframe      - Pandas dataframe with adjusted column names

    Example:    dataframe = Parse.reformat_column_names(dataframe,replace_this="data.",with_this="data_")
    """
    dataframe.columns = [col.replace(replace_this, with_this) for col in dataframe.columns]
    return dataframe

