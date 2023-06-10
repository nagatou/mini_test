# 
#
# Copyright Naoyuki Nagatou
# Mode: python3
###

from pathlib import Path
import os
import sys
import re
import gc
import psutil
import pandas as pd
import numpy as np
import configparser
import glob
from mimetypes import guess_type

def csv_file_list(path,lecture_class,suffix):
         file_list = glob.glob(path+'*'+lecture_class+suffix,recursive=True)
         if (file_list):
            return(file_list)
         else:
            print("total_result: No csv files")
            quit(1)

def read_chunks(entry):
   if (os.name != 'nt'):
      minetype = 'text/csv'
   else:
      minetype = 'application/vnd.ms-excel'
   if (guess_type(entry)[0]!=minetype):
      print("total_result: No CSV file")
      quit(1)
   else:
      return(pd.read_csv(entry,skipinitialspace=True,encoding='utf-8',chunksize=100000,usecols=[0,1,2,7],na_values=['-']))

def retrieve_columns(df_csv,quiz_num):
   df_tmp = df_csv.rename(columns=(lambda name: quiz_num if '評' in name else name)).set_index('氏名').drop('全平均').reset_index()
   #df_tmp = df_tmp.astype({quiz_num: float})
   del df_csv
   print(quiz_num)
   return(df_tmp)

def total(df):
   df_total = df.sum(numeric_only=True,axis=1).agg(np.ceil).rename('Total',inplace=True).astype('int')
   return(pd.concat([df,df_total],axis='columns',ignore_index=False).set_index('学籍番号').sort_index())

def local_quiz(df,entry):
   if (os.name != 'nt'):
      minetype = 'text/csv'
   else:
      minetype = 'application/vnd.ms-excel'
   if (guess_type(entry)[0]!=minetype):
      print("total result: No CSV file")
      quit(1)
   else:
      if (os.path.exists(entry)):
         print(entry)
         return(df.merge(pd.read_csv(entry,skipinitialspace=True,encoding='utf-8')[['学籍番号','評点']].rename(columns={'評点':'QuizS'}),how='outer',on=['学籍番号']))
      else:
         print("total result: No local quize score")
         return(df)
      

if __name__ == "__main__":
   if (os.path.exists(os.path.join(os.getcwd(),'total_result.ini'))):
      config = configparser.ConfigParser()
      config.read(os.path.join(os.getcwd(),'total_result.ini'))
      if 'PATH' in config:
         path = config.get('PATH','csv_file_path')
         lecture_class = config.get('PATH','class')
         suffix = config.get('PATH','csv_file_suffix')
         df_tmp = pd.DataFrame(columns=['学籍番号','氏名','Name'])
         for csv_file in csv_file_list(path,lecture_class,suffix):
            for chunk in read_chunks(csv_file):
               df_partial = retrieve_columns(chunk,str(csv_file.split('/')[1]).split('-')[0])
               df_tmp = df_tmp.merge(df_partial,how='outer',on=['学籍番号','氏名','Name'])
         df_tmp = local_quiz(df_tmp,path+config.get('PATH','local_quiz'))
         save_file = config.get('PATH','save_path')+config.get('PATH','save_file_prefix')+lecture_class+'.csv'
         if (os.path.exists(save_file)):
            os.remove(save_file)
         total(df_tmp).to_csv(save_file)
      else:
         print("total_result: No PATH variable")
         quit(1)
   else:
      print("total_result: No configuration file")
      quit(1)
