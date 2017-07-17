# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd


df = pd.read_csv('C:\\Users\\15418\\Desktop\\test\\cleaned_USB_1_4.csv')
df_c = df.loc[:,['comment']]
dict = df_c.to_dict()
for i in range(1,len(df_c)):    
    t = df_c['comment'][i]
    t1 = t.find('[')
    t2 = t.find(']')
    aa = t[t1+1:t2].replace(',','').replace('\'','').replace(' ','')
    print(aa)
    f = open('LDA.txt','a')
    f.write(aa+'\n')
    f.close