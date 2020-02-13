#!/usr/bin/env python
# coding: utf-8

"""
(c) 2020 Gabriel Lainesse
"""

import os
import pandas as pd
import numpy as np
import re
import unicodedata
from pandas.api.types import is_string_dtype

xl_files = [x for x in os.listdir() if x.endswith('.xls') or x.endswith('.xlsx')]

portuguese_words = ['BD' ,
'Desenvolvimento' ,
'o negócio' ,
'Vendas' ,
'agentes' ,
'Governo' ,
'Patrocinadores' ,
'Conformidade' ,
'Representante' ,
'lobista' ,
'Autoridade' ,
'Consultor' ,
'terceiro' ,
'Cliente' ,
'prêmio' ,
'contrato' ,
'BP' ,
'Parceiro' ,
'Comercial' ,
'permitir' ,
'Dividendo' ,
'adquirir' ,
'marketing' ,
'Licença' ,
'local' ,
'Corretor' ,
'Orientador' ,
'costumes' ,
'Interação' ,
'em nome de' ,
'Interface' ,
'Funcionários' ,
'relações' ,
'Serviço' ,
'noivado']


# In[71]:


english_words = ['BD', 
'Devel', 
'Business', 
'Sale', 
'agent', 
'Govern', 
'Sponsor', 
'Complia', 
'Represent', 
'lobby', 
'Author', 
'Consul', 
'third party', 
'Client', 
'award', 
'contract', 
'BP', 
'Partner', 
'Commercial', 
'permit', 
'Dividend', 
'acquire', 
'market', 
'License', 
'local', 
'Broker', 
'Advisor', 
'custom', 
'Interact', 
'on behalf', 
'Interf', 
'Official', 
'relation', 
'Service', 
'engage']

words = portuguese_words + english_words

words = [x.lower() for x in words]

pattern = '|'.join(map(re.escape, words))

words_ascii = map(lambda val: unicodedata.normalize('NFKD', val).encode('ascii', 'ignore').decode() 
                                        if isinstance(val, str) else np.nan, words)


pattern_ascii = '|'.join(map(re.escape, words_ascii))


def find_pattern(series, str_pattern):
    if is_string_dtype(series):
        return series.str.lower().str.contains(str_pattern, na=False)
    else:
        return None

def find_pattern_ascii(series, str_pattern):
    return find_pattern(series.apply(lambda val: unicodedata.normalize('NFKD', val).encode('ascii', 'ignore').decode() if isinstance(val, str) else np.nan),
                        str_pattern)


def get_matched_words(series, str_pattern):
    return series.apply(lambda x: re.findall(str_pattern, x.lower()) if isinstance(x, str) else np.nan)
    #series.str.lower().str.contains(str_pattern, na=False)


#def get_matched_words(series, str_pattern):
#    return series.apply(lambda x: re.findall(pattern, x.lower()) if isinstance(x, str) and len(re.findall(pattern, x.lower())) > 0 else np.nan)
#   #series.str.lower().str.contains(str_pattern, na=False)



result_df = pd.DataFrame(None, columns=['Workbook', 'Worksheet', 'Column', 'Row', 'Cell Content'])


result_summary_df_final = pd.DataFrame(None, columns=['Workbook', 'Worksheet', 'Column', 'Matched Words', 'Count'])


for current_workbook in xl_files:
    print("Workbook: {}".format(current_workbook))
    xl_file = pd.ExcelFile(current_workbook)
    for current_worksheet in xl_file.sheet_names:
        print("|---> Worksheet: {}".format(current_worksheet))
        xl = pd.read_excel(xl_file, current_worksheet, index_col=None, na_values=['NA'], dtype=str)
        for column in xl.columns:
            #print(column)
            bool_series = np.array(find_pattern_ascii(xl[column], pattern_ascii))
            matched_words_series = np.array(get_matched_words(xl[column], pattern_ascii))
            
            if bool_series.ndim != 0:
                if sum(bool_series) > 0:
                    extract = xl[column].iloc[np.where(bool_series > 0)]
                    matched_words_extract = matched_words_series[np.where(bool_series > 0)]
                    for row, cell_content, matched_words in zip(extract.index, extract, matched_words_extract):
                        result_df = result_df.append({'Workbook': current_workbook, 'Worksheet': current_worksheet, 
                                          'Column': column, 'Row': row, 'Cell Content': cell_content, 'Matched Words': matched_words}, ignore_index=True)

    # TO DEBUG (SUMMARY TABLE):
    #result_summary_df = result_df['Matched Words'].value_counts()
    #result_summary_df.reset_index()
    #result_summary_df = pd.DataFrame(result_summary_df)
    #result_summary_df['Workbook'] = current_workbook
    #result_summary_df['Worksheet'] = current_worksheet
    #result_summary_df['Column'] = current_column
    #result_summary_df = result_summary_df.reset_index().rename(columns={'index':'Matched Words', 'Matched Words':'Count'})
    #result_summary_df_final = result_summary_df_final.append(result_summary_df, sort=False)

result_df.to_csv('Ultimate Word Search - Results.csv')
#result_summary_df_final.to_csv('Ultimate Word Search - Results.csv')



#result_summary_df_final.to_csv('summary.csv')


#for matched_words, count in zip(result_df['Matched Words'].value_counts():
#    result_summary_df = result_summary_df.append({'Workbook': current_workbook, 'Worksheet': current_worksheet, 
#                              'Column': current_column, 'Matched Words': cell_content, 'Count': matched_words}, ignore_index=True)