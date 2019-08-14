# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 10:15:12 2018

@author: LAING3
"""


import os
import sys
import urllib.request
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import time



def who_is(ip):
    """
    Argument:
        ip : ip address to perform a WHOIS query on.
    
    Returns a DataFrame containing the results from a WHOIS query
    for the IP Address entered as argument.
    """
    rooturl = "https://awebanalysis.com/en/ip-lookup/"
    html = urllib.request.urlopen(rooturl + ip.strip())
    soup = BeautifulSoup(html, "lxml")
    whois_response = soup.find_all("table", id_="ipdetails")[0].contents[0].contents[0]
    results = [['IPAddress:', str(ip)]]
    for row in whois_response.split('\n'):   
        results.append(row.split(':', maxsplit=1))
    
    try:
        dic = {t[0]:[''.join(t[1:]).strip()] for t in results}    
        return pd.DataFrame.from_dict(dic, orient="columns")
    except:
        print("Could not lookup IP Address {}".format(ip))



def read_ip_addresses():
    """ 
    Reads the ipaddresses.xlsx file within the same directory as the app and returns
    the list of ip addresses contained within the first column of the first worksheet
    """
    table = pd.read_table('ip.txt', sheet_name = 0, header=None)
    #Checks if the file is empty or not. If not, returns the list of ip addresses
    #contained within the first row of the first sheet.
    try:
        return list(table.iloc[:,0])
    except IndexError as e:
        print("The program could not read the list of IP addresses.")
        print("The list might be empty. Please fill it with the IP addresses to inquire.")
        print("Error details:")
        print(e)


def write_output(df_to_write):
    try:
        df_to_write.to_csv('output_'+ time.strftime("%Y%m%d%H%M%S") + '.csv')
    except PermissionError as e:
        print("Could not write file to disk")
        print(e)
    
    openfile = input("File 'output.csv' written to disk. Would you like to open it? (y/n): ")
    if openfile == 'y':
        os.startfile('output.csv')





combined_results = who_is("127.0.0.1")



for ipaddress in read_ip_addresses():
    # Then, for each ip address, append the results to the empty DataFrame
    print("Please wait: Performing WHOIS query on {}...".format(ipaddress))
    try:
        combined_results = combined_results.append(who_is(ipaddress), ignore_index=False, sort=False)
    except Exception as e:
        print("ERROR: An exception occured when processing ip address {}".format(ipaddress))
        print("Skipping to next address and logging unsuccessful attemps within the 'unsuccessful_attemps.txt' file.")
        with open("unsuccessful_attempts.txt", "a") as unsuccessful_log:
            unsuccessful_log.write(ipaddress + ", " + str(e) + "\n")
        continue
    #Waiting 1 second to prevent overloading the servers.
    time.sleep(1)
    
        
write_output(combined_results)
        

