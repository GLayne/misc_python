# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 14:57:55 2018

@author: LAING3
"""

import os
import sys
import urllib.request
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import time
        

def write_log(line):
    assert type(line) == 'string'
    with open('IPLookup_log.txt', 'a') as log:
        log.writeline(''.join(time.localtime(time.time)) + line)


def who_is(ip):
    """
    Argument:
        ip : ip address to perform a WHOIS query on.
    
    Returns a DataFrame containing the results from a WHOIS query
    for the IP Address entered as argument.
    """
    rooturl = "https://who.is/whois-ip/ip-address/"
    html = urllib.request.urlopen(rooturl + ip.strip())
    soup = BeautifulSoup(html, "lxml")
    whois_response = soup.find_all("div", class_="col-md-12 queryResponseBodyKey")[0].contents[0].contents[0]
    results = [['IPAddress:', str(ip)]]
    for row in whois_response.split('\n'):   
        results.append(row.split(':', maxsplit=1))
    
    try:
        dic = {t[0]:[''.join(t[1:]).strip()] for t in results}    
        return pd.DataFrame.from_dict(dic, orient="columns")
    except:
        print("Could not lookup IP Address {}".format(ip))
        write_log("Could not lookup IP Address " + str(ip))
        

def read_ip_addresses():
    """ 
    Reads the ipaddresses.xlsx file within the same directory as the app and returns
    the list of ip addresses contained within the first column of the first worksheet
    """
    xl = pd.read_excel('ipaddresses.xlsx', sheet_name = 0, header=None)
    #Checks if the file is empty or not. If not, returns the list of ip addresses
    #contained within the first row of the first sheet.
    try:
        return list(xl.iloc[:,0])
    except IndexError as e:
        print("The program could not read the list of IP addresses.")
        print("The list might be empty. Please fill it with the IP addresses to inquire.")
        print("Error details:")
        print(e)
        write_log("The program could not read the list of IP addresses. " +
                  "The list might be empty. Please fill it with the IP addresses to inquire. " +
                  "Error details: " + str(e))
        abort()


def check_for_excel_file():
    if os.path.isfile('ipaddresses.xlsx'):
        print("File 'ipaddresses.xlsx' found!")
        return 1
    else:
        create_file = input("File 'ipaddresses.xlsx' NOT found. Do you want to create it? (y/n): ")
        if create_file:
            emptydf = pd.DataFrame()
            emptydf.to_excel('ipaddresses.xlsx')
            print("\n")
            print("An empty 'ipaddresses.xlsx' file has been created. Fill the first "
                  + "column of the only worksheet with the IP addresses that you want to run " +
                  "WHOIS queries on and then run this program again.")


def write_output(df_to_write):
    try:
        df_to_write.to_csv('output_'+ time.strftime("%Y%m%d%H%M%S") + '.csv')
    except PermissionError as e:
        print("Could not write file to disk")
        print(e)
        write_log("Could not write file to disk.")
        write_log(e)
    
    openfile = input("File 'output.csv' written to disk. Would you like to open it? (y/n): ")
    if openfile == 'y':
        os.startfile('output.csv')


def main_program():
    if check_for_excel_file():
        #Create an empty DataFrame to hold the WHOIS query results
        #First, initiate the empty DataFrame with default column names.
        print("Please wait: Writing columns...")
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
        
        #Then remove the values for "127.0.0.1"
        #combined_results.drop(labels=0, axis=0)
        
        write_output(combined_results)
        
        
def abort():
    print("This program will now quit.")   
    sys.exit()

def terms_refused():
    """
    Handles the case where the user refuses the terms and conditions.
    """
    print("You have refused the terms of use. This program will now quit.")
    time.sleep(2)



def print_terms(): 
    print("**************TERMS OF USE**************")
    print("This program is free software. It comes without any warranty, to the extent permitted by the law.")
    print("The author does not guarantee any result or their validity " + 
          "and shall not be held responsible for any damage that might occur " +
          "as a result of using this program.\nUse this program at your own risk.")
    print("\n")
    print("This program does NOT share any sensitive information, EXCEPT for the " +
          "content of the first column in the ipaddress.xlsx Excel file.\n")
    print("In the general use case, this only consists of IP addresses and should " +
          "not be a security risk.\n")
    print("The only query that is made is a WHOIS query at the following address:\n"+
          "https://who.is/whois-ip/ip-address/")
    print("**************END**************")

def main():
    #Main thread
    print("IP Address WHOIS Inquiry v.0.1")
    print("Author: Gabriel Lainesse")
    print("*******WARNING*******")
    print("To run this program, you need to review and agree with the terms of use.")
    print("To review the terms of use, type 'terms' and press enter.")
    print("To agree with the terms of use and proceed with the program, type 'y'")
    print("To quit the program without agreeing to the terms, type 'n' or close the window")
    main_thread = True
    tries = 0
    while main_thread:
        proceed_input = str(input("Do you want to proceed? (y/n/terms): "))
        if proceed_input == 'y':
            main_program()
            main_thread = False
        elif proceed_input == 'n':
            terms_refused()
            main_thread = False
            break
        elif proceed_input == 'terms':
            print_terms()
        else:
            print("The value entered does not correspond to the provided choices.")
            print("Please enter either 'y', 'n' or 'terms'.")
            tries += 1
            if tries == 5:
                print("Too many attempts. Exiting program.")
                main_thread = False
            else:
                continue


if __name__ == "__main__":
    main()