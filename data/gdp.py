import pandas as pd
import numpy as np
import matplotlib as plt
import sys


"""
USAGE:

1) Download the following table
    - https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=3610011201 : be sure to use the "Download Entire table" option"
2) make sure you save it as 'canadian-gdp-1960-2020.csv' file inside of the data folder
3) create actionable dataframe like so:

import gdp as getgdp

gdp = getgdp()

"""

pivot = 'Current and capital accounts - Households, Canada, quarterly'

gdp = pd.read_csv('data/canadian-gdp-1960-2020.csv')


def truncate_top_bottom():
    global gdp
    print(gdp)
    """
    We replace nan's with empty strings in the first column
    """
    gdp[pivot] = gdp[pivot].replace(np.nan, '', regex=True)
    """
    First find where to truncate the top part of the 
    """
    topRow = gdp[pivot].loc[lambda x: x=='Estimates'].index
    """
    Then we find as of where to truncate the bottom part of the frame
    """
    bottomRow = gdp[pivot].loc[lambda x: x=='Symbol legend:'].index
    lastRow = gdp[gdp[pivot].str.contains("DOI:")].index
    dollarRows = gdp[gdp['Unnamed: 1'] == 'Dollars'].index
    percRows = gdp[gdp['Unnamed: 1'] == 'Percent'].index
    rowsToDrop = [i for i in range(topRow[0])]
    rowsToDrop += list(dollarRows)
    rowsToDrop += list(percRows)
    rowsToDrop += [i for i in range(bottomRow[0] - 1, lastRow[0] + 1)]
    gdp.drop(rowsToDrop, inplace=True)

def reassign_column_names():
    global gdp
    names = {}
    for column in gdp.columns:
        if column == pivot:
            names[pivot] = 'Period'
        else:
            names[str(column)] = gdp.iloc[0][column]
    gdp = gdp.rename(columns=names)
    estimatesRow = gdp['Period'].loc[lambda x: x=='Estimates'].index
    gdp.drop(estimatesRow, inplace=True)
    preTColumns = gdp.columns
    gdp = gdp.transpose()
    newNames = {}
    for column in gdp.columns:
        """
        This will cleanup the column names
        """
        newNames[column] = gdp.iloc[0][column].split(' (')[0]
    gdp = gdp.rename(columns=newNames)
    gdp.drop(['Period'], inplace=True)
    
def apply_new_indexes():
    global df
    global gdp
    gdp['Quarter Year'] = gdp.index
    def quarter_year(row):
        splits = row['Quarter Year'].split(' ')
        return pd.Series(data={
            'Year': splits[1],
            'Quarter': splits[0]
        })
    gdp = gdp.merge(gdp.apply(lambda row: quarter_year(row), axis=1), left_index=True, right_index=True)
    gdp = gdp.set_index('Year')
    

def cleanup_gdp():
    truncate_top_bottom()
    reassign_column_names()
    apply_new_indexes()
        
def get_gdp_df():
    global gdp
    cleanup_gdp()
    return gdp


sys.modules[__name__] = get_gdp_df