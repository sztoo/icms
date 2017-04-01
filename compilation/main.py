import re
import pandas as pd
from os import path 

pd.options.mode.chained_assignment = None # None|'warn'|'raise'

file_names = ['csv/na.csv','csv/hk.csv','csv/sg.csv','csv/uk.csv','csv/my.csv']
headers = ['name', 'gender', 'race', 'institution', 'course']

def sanitize(name):
  print("Sanitizing {}...".format(name))
  data = pd.read_csv(name)
  df = pd.DataFrame(data).drop_duplicates()

  df.columns = [col.lower() for col in list(df.columns)]
  df.insert(0, 'name', df['first name']+" "+df['last name'])
  if('chapter' in df.columns):
    df.drop(df[['chapter','first name','last name']] , axis=1, inplace=True)

  ethnicity_dic = {'chinese':['malaysian chinese','chinese'], 'malay':'malay', 'indian':'indian', 'others':'kadazan'}
  year_dic = {0:['0','others','graduated','pre-u'],
              1:['1','1st','first','freshman','year 1','1st year of study','1st year'],
              2:['2','2nd','second','second year','sophomore', 'year 2'],
              3:['3','3rd', 'junior', 'year 3', '3rd year'],
              4:['4','senior'],
              5:['5','1st year masters','masters']}

  dicts = [ethnicity_dic, year_dic]
  for dic in dicts:
    col = 'race' if dic == ethnicity_dic else 'year of study'
    update(df, col, dic)
  
  return(df)

def update(df, col, dic):
  for idx, val in enumerate(df[col]):
    df[col].iloc[idx] = ''.join([str(k) for k,v in dic.items() if str(val).lower() in v])
  
def sort_write(df, mode, name):
  with open('results.txt', mode) as f:
    f.write("{}\n".format(name))
    cols = ['gender','race','year of study','institution','course']
    for col in cols:
      res = df.groupby(col).size().sort_values(ascending=True)
      f.write("\n> {}\n{}\n".format(col.upper(), res))
    f.write("-"*60+"\n\n")
  f.close()

def checking(df, name):
  mode = 'w' if not path.exists(name) else 'a'
  sort_write(df=df, mode=mode, name=name)

def main():
  for name in file_names:
    df = sanitize(name)
    checking(df, name)

if __name__ == "__main__":
  main()