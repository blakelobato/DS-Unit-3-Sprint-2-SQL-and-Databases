import os
import sqlite3
import pandas as pd
import numpy as np


df = pd.read_csv('buddymove_holdiayiq.csv')

print(df.shape)

#make new connection 
conn = sqlite3.connect('buddymove_holidayiq.sqlite3')

#sqlite to df
df.to_sql(name='bm', con = conn, if_exist = 'replace')

cursor = conn.cursor()

#2.1 how many rows
cursor.execute("""SELECT COUNT(*) FROM bm;""")

#2.2 have over 100 nature and shopping
cursor.executre("""SELECT COUNT(*) FROM bm WHERE Nature >= 100 AND Shopping >= 100""").fetchone()