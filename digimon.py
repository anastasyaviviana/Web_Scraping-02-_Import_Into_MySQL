#web scraping digimon and import into csv and mysql

import requests
from bs4 import BeautifulSoup as bs
import csv
import MySQLdb
from secret import nama, passwd     #import username and password for connect to my mysql

link=requests.get('https://wikimon.net/Visual_List_of_Digimon')
soup=bs(link.content,'html.parser')

name=[]
picture=[]

for a in soup.find_all('div',{'id':'mw-content-text'}):
    for b in a.find_all('table',style='text-align: center; width: 130px; float: left; margin: 0px 4px 2px 0px; background-color: #222222;'):
        dataperitem=""
        for c in b.find_all('a'):
            if c.text=='':
                continue
            else:
                name.append(c.text)
            for d in b.find_all('img'):
                picture.append('https://wikimon.net'+d['src'])

alldata=[]
n=0
while n<len(name):
    alldata.append([name[n],picture[n]])
    n+=1

#import to csv
datadigimon=open('./file excel/digimon.csv','w',newline='',encoding='utf8')
writer=csv.writer(datadigimon)
writer.writerow(["name", "picture"])
writer.writerows(alldata)

#import to mysql
mydb = MySQLdb.connect(host='localhost',
    user=nama,
    passwd=passwd,
    db='digimon',
    autocommit=True,
    charset = 'utf8')
cursor = mydb.cursor()

for i in range(len(alldata)):
    name=alldata[i][0]
    picture=alldata[i][1]
    sql = 'INSERT INTO digimon (name, picture) VALUES(%s,%s)'
    
    cursor.execute(sql, (name, picture))
    mydb.commit()