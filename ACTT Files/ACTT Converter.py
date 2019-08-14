# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 16:26:32 2018

@author: Gabriel Lainesse
@version 0.1
"""


import sys
import os
import subprocess
import pandas as pd
import logging
logger = logging.getLogger('ACTT Converter log')
hdlr = logging.FileHandler('acttlog.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)


# Get current working directory
inputfolder = 'input\\'
dsvfolder = 'output-dsv\\'
xlsfolder = 'output-xls\\'

#Progress Counter
progress = 0
filecount = len(os.listdir(inputfolder))

#Asks the user for the delimiter to search
delim_search = '|^|'
delim_replace = '|'
delim_search = input('Which delimiter do you want to replace '
                     'in the input files? (default = \'|^|\'): ') or r'|^|'

delim_replace = input(('Which character(s) do you want to '
                      'replace the delimiter with? (default = \'|\'): ')) or '|'

path = os.getcwd()
# Initiate empty files list
acttfiles = []
# Set list to files in the current working directory
acttfiles = os.listdir(inputfolder)
# Reset files list to contain only those with the 'ACTT' file extension
acttfiles = [acttfile for acttfile in acttfiles if acttfile.endswith('ACTT')]

#If no files remain within the list: exit the program
if len(acttfiles) < 1:
    sys.exit()

#Checks if the output folders exist; if not: creates them
os.makedirs(os.path.dirname(dsvfolder), exist_ok=True)
os.makedirs(os.path.dirname(xlsfolder), exist_ok=True)

#Initiates an empty list for files which could not be cleaned.
errorfiles = {}
#Loop over all remaining files
for acttfile in acttfiles:
    print('Processed {} ACTT files out of {}'.format(progress, filecount))
    try:
        with open(inputfolder + acttfile, 'r') as inputfile:
            #Generates the output file's name and path string
            outputfilename = ''.join(map(str,
                                         [acttfile.split('.')[:-1][0], '.dsv']))

            #Creates a new file and write the data line by line
            with open(dsvfolder + outputfilename, 'w') as outputfile:
                for line in inputfile.readlines():
                     #Cleans the line, replacing delimiters |^| to '|', 
                     #or otherwise specified
                    cleanline = line.replace(delim_search, delim_replace)
                    #Writes the line to the new file
                    outputfile.write(cleanline)
    
    #If an error occurs and the file cannot be cleaned the file is added
    #to the errorfiles list and the loop continues on the next file.
    except BaseException as e:
        errorfiles[acttfile] = 'FAILED TO READ SOURCE FILE FOR DELIMITER CLEANUP'
        print(acttfile + ' is not readable and will be skipped.')
        logger.error('Failed to read source file for delimiter cleanup ' + acttfile + ' : ' + str(e))
        continue
    
    progress += 1
#End of loop
        
xlcheck = input('Do you also want to export the files to a single Excel Workbook? (y/n)')
if xlcheck = 'y':
    #Joins all output files to a single Excel File
    #outputfilename = ''.join(map(str,[file.split('.')[:-1][0], '.dsv']))
    progress = 0
    
    dsvfiles = os.listdir(dsvfolder)
    with pd.ExcelWriter(xlsfolder + 'CombinedOutput.xlsx', engine='xlsxwriter') as ew:
    
        for dsvfile in dsvfiles:
            print('Processed {} DSV files out of {}'.format(progress, filecount))
            try:
                tempdf = pd.read_csv(dsvfolder + dsvfile, sep=delim_replace, 
                                     encoding='cp1252', dtype=object)
                tempdf.to_excel(ew, sheet_name=str(os.path.splitext(dsvfile)[0][:30]))
                
            except BaseException as e:
                errorfiles[dsvfile] = 'FAILED TO GENERATE DATAFRAME FOR EXCEL EXPORT'
                print(dsvfile + ' is has not been correctly exported to Excel and will be skipped.')
                logger.error('Failed to generate dataframe for Excel Export for file ' + dsvfile + ' : ' + str(e))
                continue
                
            progress += 1
        ew.save()
else:
    'continue

#If there was at least 1 error file, writes the list of files to '_skipped.txt'
if len(errorfiles) > 0:
    with open(dsvfolder + '_skipped.txt', 'w') as errorlog:
        for key, val in errorfiles:
            errorlog.write(key + ': ' + val)
            errorlog.write('\n')
    with open(xlsfolder + '_skipped.txt', 'w') as errorlog:
        for file, errormessage in errorfiles:
            errorlog.write(key + ': ' + val)
            errorlog.write('\n')


#Opens explorer windows on the output folder.
subprocess.Popen(''.join((r'explorer ', os.getcwd(), xlsfolder)))

#Notify user of the end of the procedure and the status on error files.
if len(errorfiles) == 0:
    print("Output Complete.")
elif len(errorfiles) > 0:
    print("Output Complete.")
    print("There were {} files with issues which were skipped.\n"
                 "The list of skipped files has been saved to"
                 "'\\output\\_skipped.txt'").format(len(errorfiles))
else:
    print("An unexpected error occured with the list of error files.")