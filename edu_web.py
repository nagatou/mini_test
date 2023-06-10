# 
#
# Copyright (2023) Naoyuki Nagatou
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

if __name__ == "__main__":
   if (os.path.exists(os.path.join(os.getcwd(),'total_result.ini'))):
      config = configparser.ConfigParser()
      config.read(os.path.join(os.getcwd(),'total_result.ini'))
      score_file = config.get('PATH','score_file')
      if (os.path.exists(score_file)):
         fd_seiseki = pd.read_csv(score_file,skipinitialspace=True,encoding='cp932').sort_values('学籍番号')
      else:
         print("edu_web: No score file")
         quit(1)
      short_exm = config.get('PATH','save_path')+config.get('PATH','save_file_prefix')+config.get('PATH','class')+'.csv'
      if (os.path.exists(short_exm)):
         fd_total = pd.read_csv(short_exm,skipinitialspace=True,encoding='utf-8').sort_values('学籍番号')
         fd_seiseki['成績記入欄'] = fd_total['Total']
         fd_seiseki.set_index('科目コード').to_csv('seiseki_LAS.I111-05.csv',encoding='cp932')
      else:
         print("edu_web: No total result file")
         quit(1)

   else:
      print("edu_web: No configuration file")
      quit(1)
