import os
import pandas as pd
from itertools import *

eifFolder = r"YOUR FOLDER PATH HERE"

def findEIFs(pathIn):
    """
    Finds all files with the extension '.eif' in the given directory and its subdirectories.

    Parameters:
    - pathIn (str): The path to the directory to search for EIF files.

    Returns:
    - list: A list of paths to the found EIF files.
    """
    eifList = []
    if os.path.isdir(pathIn):
        for r, d, k in os.walk(pathIn):
            for f in k:
                if f.endswith('.eif'):
                    eifList.append(os.path.join(r, f))
    else:
        print('Invalid EIF folder path.')
    return eifList

def dataCheck(line):
    """
    Checks if a line in the EIF file contains only alphanumeric characters.

    Parameters:
    - line (str): The line to be checked.

    Returns:
    - bool: True if the line contains only alphanumeric characters, False otherwise.
    """
    r = filter(lambda p: p.replace('-', '').isalpha(), line)
    looks = len(list(r)) == 0
    return looks
    

def checkLooksRight(lineIn, t):
    """
    Checks if the header or data lines in the EIF file appear to be formatted correctly.

    Parameters:
    - lineIn (list): List of lines (header or data) to be checked.
    - t (str): Type of data to check ('header' or 'data').

    Returns:
    - bool: True if the lines appear to be formatted correctly, False otherwise.
    """
    if 'header' in t:
        # they should all be words/letters
        r = filterfalse(lambda p: p.replace('[', '').replace(']', '').replace('/', '').isalpha(), lineIn)
        looks = len(list(r)) == 0
    if 'data' in t:
        r = []
        for line in lineIn:
            r.append(dataCheck(line))
        r = list(set(r))
        looks = len(r) == 1
    # print('looks', looks, 'for', t)
    return looks
   

def scrapeEIF(eifPath):
    """
    Extracts data from an EIF file and returns a Pandas DataFrame.

    Parameters:
    - eifPath (str): The path to the EIF file.

    Returns:
    - pd.DataFrame: A Pandas DataFrame containing the data from the EIF file, if the file is correctly
    formatted; otherwise, an empty DataFrame.
    """
    # EIFs and pd.read_csv can be a bit finicky for some reason; open() will do fine here.
    epd = pd.DataFrame()
    with open(eifPath, 'r') as fr:
        f = [a.strip('\n').strip('#').split(';') for a in fr.readlines()[3:]]
        headers = f[0]
        data = f[1:]
        hTest = checkLooksRight(headers, 'header')
        dTest = checkLooksRight(data, 'data')
        if hTest and dTest:
            epd = pd.DataFrame(data, columns=headers)
    return epd

if __name__ == "__main__":
    print('#################################')
    print('Starting EIF scraper...')
    print('Note: will not work if file path in EIF contents')
    print('#################################')
    # first, find all EIF files. WARNING: THIS WILL SEARCH ALL SUBDIRECTORIES.
    elist = findEIFs(eifFolder)
    pdList = []
    issues = []
    for i in elist:
        # Loop through the found EIF files and convert them to verified pandas dataframes.
        print('scraping %s...' % os.path.basename(i))
        epd = scrapeEIF(i)
        if len(epd) > 0:
            pdList.append(epd)
        else:
            issues.append(i)
    try:
        # Merge all the dataframes. If it fails, we know nothing actually went into the list of
        # successful conversions.
        merged = pd.concat(pdList)
        print('#################################')
        print(len(merged), 'events have been recorded')
    except ValueError:
        print('No files successfully scraped')
    if len(issues) > 0:
        print('the below files had reading issues:')
        for a in issues:
            print(os.path.basename(a))
    else:
        print('No files had issues')
    
    
        
