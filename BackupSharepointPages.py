# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 10:45:51 2018

@author: LAING3
"""
import os
from bs4 import BeautifulSoup
import urllib.request

rooturl = "spl.snclavalin.com/business/IA-DataAnalyticsKB"
localurl = "spl.snclavalin.com/business/IA-DataAnalyticsKB/SitePages"
spurl = "https://spl.snclavalin.com/business/IA-DataAnalyticsKB/_api/web/lists/getbytitle('Documents')/items?$select=Title


page = urllib.request.urlopen9
soup = BeautifulSoup(spurl)