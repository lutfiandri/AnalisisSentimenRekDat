# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VoeJW6JhnrR3hhLUtkVk7043Hwbhvfzt
"""

!pip install git+https://github.com/karuniaperjuangan/twint

!pip install nest-asyncio

import twint # coba pakai library yang baru saja diinstal
import nest_asyncio
from datetime import date
from datetime import timedelta
nest_asyncio.apply()

today = date.today()
yesterday = today - timedelta(days = 1)
today_new = today.strftime("%Y-%m-%d")
yesterday_new = yesterday.strftime("%Y-%m-%d")

c = twint.Config()
c.Search = 'LGBT OR OneLove OR onelove OR LGBTQ'
c.Lang = "id"
c.Since = yesterday_new
c.Until = today_new
c.Filter_retweets = True
c.Store_csv = True
c.Output = "lgbt4.csv"

twint.run.Search(c)

import pandas as pd 
from google.colab import drive
drive.mount('/content/drive')

df = pd.read_csv('lgbt4.csv') #Nama File tadi
df = df[["date","time","username","tweet","replies_count",
         "retweets_count","likes_count"]]
df = df.drop_duplicates(subset=["date","time","username","tweet","replies_count"], ignore_index=True)
#Mengambil 5 data terakhir
df.tail(5)

df.head()

import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

idn_stopwords = stopwords.words('indonesian')
idn_stopwords.extend(
    ['ae','ah','aing','aj','aja','ak','anjir','ayo','banget','belom','bener2','bgt','biar','bikin','blm','btw','bnyk','byk','cuman','d','dah','dapet','deh','deket',
     'dg','dgn','disana','dll','doang','dpt','dr','drpd','duar','duarr','duarrr','duluan','e', 'eh','emang','emg','engga','g','ga','gak','gaada','gamau','gara',
     'gara2','gatau','gegara','gimana','gini','gtu','gitu','gk','gmn','gt','gue','gw','hah', 'haha','jd','jdi','jg','jgn','kagak','ka','kaga','kah','kak','kalo',
     'kali','karna','kau','kayak','kayaknya','kek','kl','klian','klo','knp','kpd','ku','krn','krna','kyk','la','lg','lgsg','lha','lho','lo','loh','lu','ma','mah','mending',
     'min','mo','mrk','msh','na','nder','nge','ngga','nggak','ni','nih','ntar','nya','org','pakai','pake','pd','pdhl','salah','sama2','sampe','sbg','sdh',
     'sebenernya','sat','set','satset','si','sih','situ','skrg','sm','spt','tau','tau2','tbtb','tb2','td','tdk','tiba2','tp','tpi','ttg','trus','trs','tsb',
     'tu','tuh','udah','udh','utk','xixi','w','wes','wkwk','wkwkw','wkwkwk','wkwkwkwk','wow','x','y','yg','ya','yaa','yaaa','yah','ygy','yo','yuk'])
idn_stopwords.extend(
    ['ra','mbak','mas','kui','ki','po','ora','iki','karo','opo','sek','sik','arep','og','wae','ngono','tenan','ben','iso','kudu','sing','nek','dadi','pa','iku','saiki'])

def remove_unnecessary_char(text):
  text = re.sub("\[USERNAME\]", " ", text)
  text = re.sub("\[URL\]", " ", text)
  text = re.sub("\[SENSITIVE-NO\]", " ", text)
  text = re.sub('  +', ' ', text)
  return text

def preprocess_tweet(text):
  text = re.sub('\n',' ',text) # Remove every '\n'
  # text = re.sub('rt',' ',text) # Remove every retweet symbol
  text = re.sub('^(\@\w+ ?)+',' ',text)
  text = re.sub(r'\@\w+',' ',text) # Remove every username
  text = re.sub(r'\#\w+',' ',text) # Remove every hashtag
  text = re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))',' ',text) # Remove every URL
  text = re.sub('/', ' ', text)
  # text = re.sub(r'[^\w\s]', '', text)
  text = re.sub('  +', ' ', text) # Remove extra spaces
  return text
    
def remove_nonaplhanumeric(text):
  text = re.sub('&amp;', ' ', text)
  text = re.sub('[^0-9a-zA-Z,.?!]+', ' ', text) 
  text = re.sub('  +', ' ', text)
  return text

def remove_stopword(text):
  text = re.sub('[.,!?]','',text)
  text = ' '.join(['' if word in idn_stopwords else word for word in text.split(' ')]) #Mengganti stopword dengan ''
  text = re.sub('  +', ' ', text)
  text = text.title()
  text = text.strip() #Menghapus spasi atau newline di awal dan akhir kalimat yang tidak diperlukan
  return text

def fixSingkatan(text):
  text = re.sub(r'\b(aj|ae|aja)\b', 'saja', text)
  text = re.sub(r'\b(ak|gue|gw)\b','aku', text)
  text = re.sub(r'\b(belom|blm)\b', 'belum', text)
  text = re.sub(r'\b(bgt|bngt)\b', 'banget', text)
  text = re.sub(r'\b(bnyk|byk)\b', 'banyak', text)
  text = re.sub(r'\b(dlm)\b', 'dalam', text)
  text = re.sub(r'\b(dr)\b', 'dari', text)
  text = re.sub(r'\b(dg|dgn)\b','dengan',text )
  text = re.sub(r'\b(dpt|dapet)\b', 'dapat', text)
  text = re.sub(r'\b(duar+)\b', 'duar', text)
  text = re.sub(r'\b(emg|emang)\b', 'memang', text)
  text = re.sub(r'\b(gt|gtu)\b', 'gitu', text)
  text = re.sub(r'\b(gatau)\b', 'tidak tau', text)
  text = re.sub(r'\b(gaada)\b', 'tidak ada', text)
  text = re.sub(r'\b(gamau)\b', 'tidak mau', text)
  text = re.sub(r'\b(gimana|gmn)\b', 'bagaimana', text)
  text = re.sub(r'\b(jgn)\b', 'jangan', text)
  text = re.sub(r'\b(jgn2|jangan2)\b', 'jangan jangan', text)
  text = re.sub(r'\b(jd|jdi)\b', 'jadi', text)
  text = re.sub(r'\b(karna|krn|krna)\b', 'karena', text)
  text = re.sub(r'\b(kyk|kek)\b', 'kayak', text)
  text = re.sub(r'\b(kl|klo|kalo)\b', 'kalau', text)
  text = re.sub(r'\b(klian)\b', 'kalian', text)
  text = re.sub(r'\b(knp)\b', 'kenapa', text)
  text = re.sub(r'\b(kpd)\b', 'kepada', text)
  text = re.sub(r'\b(lg)\b', 'lagi', text)
  text = re.sub(r'\b(lgsg)\b', 'langsung', text)
  text = re.sub(r'\b(mrk)\b', 'mereka', text)
  text = re.sub(r'\b(pd)\b', 'pada', text)
  text = re.sub(r'\b(pdhl)\b', 'padahal', text)
  text = re.sub(r'\b(pake)\b', 'pakai', text)
  text = re.sub(r'\b(org)\b', 'orang', text)
  text = re.sub(r'\b(org2)\b', 'orang orang', text)
  text = re.sub(r'\b(sbg)\b', 'sebagai', text)
  text = re.sub(r'\b(skrg)\b', 'sekarang', text)
  text = re.sub(r'\b(sm)\b', 'sama', text)
  text = re.sub(r'\b(spt)\b', 'seperti', text)
  text = re.sub(r'\b(dah|sdh|udh|udah)\b', 'sudah', text)
  text = re.sub(r'\b(tp|tpi)\b', 'tapi', text)
  text = re.sub(r'\b(tiba2|tbtb|tb2)\b', 'tiba tiba', text)
  text = re.sub(r'\b(td|tdi)\b', 'tadi', text)
  text = re.sub(r'\b(tdk|g|ga|gak|gk|engga|enggak|ngga|nggak|kaga|kagak)\b', 'tidak', text)
  text = re.sub(r'\b(trus|trs)\b', 'terus', text)
  text = re.sub(r'\b(tsb)\b', 'tersebut', text)
  text = re.sub(r'\b(ttg)\b', 'tentang', text)
  text = re.sub(r'\b(utk)\b', 'untuk', text)
  text = re.sub(r'\b(ya+h*)\b', 'ya', text)
  text = re.sub(r'\b(yg)\b', 'yang', text)
  return text

def preprocess(text):
  text = text.lower() # Mengecilkan semua hurufnya dahulu agar lebih mudah
  text = remove_unnecessary_char(text)
  text = preprocess_tweet(text) 
  text = remove_nonaplhanumeric(text)
  return text

df["cleanTweet_stopwords_included"] = df["tweet"].apply(preprocess)

# Apply remove_stopword untuk membuat kolom 'cleanTweet_stopwords_removed' berikut
df['cleanTweet_stopwords_removed'] = df["cleanTweet_stopwords_included"].apply(remove_stopword)

pd.options.display.max_colwidth = 295 # Melihat keseluruhan isi tweet
df[["tweet","cleanTweet_stopwords_included","cleanTweet_stopwords_removed"]].sample(10)

df.to_csv('lgbt_clean.csv')