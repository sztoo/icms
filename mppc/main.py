# MPPC 2015

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

from collections import Counter

# silences chained assignment warnings 
pd.options.mode.chained_assignment = None # None|'warn'|'raise'

file = 'mppc2015.csv'
data = pd.read_csv(file)
headers = ['Name', 'Course of Study', 'Field of Study', 'Year of Study', 'Institution of Study', 'Country of Study']

def sanatize():
  df = pd.DataFrame(data)
  retained_df = df[headers]

  # drop
  retained_df.dropna(axis=0, how='all', inplace=True)

  # country_nan = retained_df['Country of Study'].isnull().sum() # sum of nans ; explict check
  country_list = sorted(set([x.lower() for x in set(retained_df['Country of Study']) if type(x) is str])) # 
  country_code = {'HK':['hong kong', 'hk'],
                  'US':['united states','us'],
                  'UK':['united kingdom', 'uk'],
                  'SG':['singapore', 'sg'],
                  'MY':['malaysia', 'my'], 
                  'AU':['australia', 'au'],
                  'CA':['canada', 'ca'],
                  'TW':['taiwan', 'tw']
                  }
  year_code = {0:'pre-u', 1:'1st', 2:'2nd', 3:'3rd', 6:['awaiting commencement','graduated']}
  
  dict_code = [country_code, year_code]
  for dic in dict_code: 
    col = 'Country of Study' if dic == country_code else 'Year of Study'
    for idx, val in enumerate(retained_df[col]):
      retained_df[col].iloc[idx] = ''.join([str(k) for k,v in dic.items() if val.lower() in v])

  return retained_df

def count_plot(df):
  cols = ['Course of Study', 'Field of Study', 'Year of Study', 'Institution of Study', 'Country of Study']
  for col in cols:
    res = df.groupby(col).size().sort_values()#.plot(kind='barh', figsize=(8,8),title=col)
    res.plot(kind='barh', figsize=(8,8), title=col)
    for col_idx, col_count in enumerate(res):
      plt.annotate(s=("  {}".format(str(col_count))), xy=(col_count, col_idx), va='center')
    plt.show()

def main(): 
  df = sanatize()
  count_plot(df)
  
if __name__ == "__main__":
  main()