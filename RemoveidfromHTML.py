# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 10:01:38 2018

@author: LAING3
"""
import os
from bs4 import BeautifulSoup
from cssutils import parseStyle

os.chdir(r'C:\Users\LAING3\Documents\_Audit Mandates\2018\2018-06 - Data Analytics\Sharepoint Site\ideadocs')
oswalklist = os.walk(os.getcwd())
rootpath = os.getcwd()
outputrootpath = os.getcwd() + r'\_output'
htmlfiles = []
outputfiles = []


for path, folders, files in oswalklist:
    for file in files:
        if file.endswith('htm') or file.endswith('html'):
            htmlfiles.append(path + '\\' + file)
            outputfiles.append(outputrootpath + path.split(rootpath)[1] + '\\' + file)

#print(htmlfiles)

for i, htmlfile in enumerate(htmlfiles):
    with open(htmlfile, 'r') as doc:
        try:
            soup = BeautifulSoup(doc, 'html.parser')
        except UnicodeDecodeError as e:
            print(e)
            print('Cannot open file (not unicode):{}'.format(htmlfile))
            continue
#        # Remove iframe with id=mctoolbar
#        try:
#            soup.find('iframe', id='mctoolbar').decompose()
#        except AttributeError as e:
#            print(e)
#            print('Attributes not found within document')
#            continue
        # Remove iframe with id=mctoolbar
        try:
            tag = soup.find('iframe', id='mctoolbar')
            style = parseStyle(tag['style'])
            style['visibility'] = 'visible'
            tag['style'] = style.cssText
         
        except AttributeError as e:
            print(e)
            print('Attributes not found within document')
            continue
        except TypeError as e:
            print(e)
            print('Attributes not found within document')
            continue
        # Remove p tag with class=feedback
        try:
            soup.find('p', {'class':'feedback'}).decompose()
        except AttributeError as e:
             print(e)
             print('Attributes not found within document')
             continue
    
    # Create output directory if it does not yet exists
    temppath = '\\'.join(outputfiles[i].split('\\')[:-1 or None])
    if not os.path.exists(temppath):
        os.makedirs(temppath)
    
    # Output modified HTML to file
    with open(outputfiles[i], 'w') as outputdoc:
        try:
            outputdoc.write(str(soup.prettify()))
        except Exception as e:
            print(e)
            print('Unable to write file:{}'.format(outputfiles[i]))
            continue
#id="mctoolbar"
#class="feedback"