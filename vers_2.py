import shutil
import os
import re
import string
import sqlite3
from typing import List
from pathlib import Path

mypath = Path().absolute()  # here
os.chdir(mypath/'input')  # here
source = os.listdir(mypath/'input')  # here
destination = mypath/'incorrect_input'  # here
for files in source:
    if not files.endswith(".fb2"):
        shutil.move(files, destination)

#count paragraphs
from lxml import etree as ET
tree = ET.parse("Example.fb2")
root = tree.getroot()
import xml.etree.ElementTree as ET
number_of_paragraph = []
paragraphs = tree.findall('//{http://www.gribuser.ru/xml/fictionbook/2.0}p')
number_of_paragraph.append(len(paragraphs))
print(number_of_paragraph)


#book name
with open('Example.fb2', 'r', encoding='utf8') as file:
    raw_file = file.read()
book_name_pattern = r'<book-name>(.*?)<\/book-name>'
title = re.findall(book_name_pattern, raw_file)
print(title)
book_text_pattern = r"<body>(.*?)<\/body>"
text_of_book = re.findall(book_text_pattern, raw_file, flags=re.DOTALL)
#print(text_of_book)
clean_pattern = re.compile('[^а-яА-ЯёЁ]')
book_text = re.sub(clean_pattern, ' ', str(text_of_book))
extra_symbols = string.punctuation.join('«»…—№\\n’' + string.digits)
clean_text = ''.join(word for word in book_text if word not in extra_symbols)
#print(clean_text)
#number of words
number_of_words = []
words = re.findall(r'\w+', clean_text)
number_of_words.append(len(words))
print(number_of_words)

#number of letters
number_of_letters =[]
letters = re.findall(r'\w', clean_text)
number_of_letters.append(len(letters))
print(number_of_letters)

#upper and lower
word_Upper = 0
word_lower = 0
for word in clean_text.split():
    if word == word.lower():
        word_lower += 1
    else:
        word_Upper += 1
print(word_Upper, word_lower)

#word stat
words = {}
for word in clean_text.split():
    if word.capitalize() not in words and word == word.lower():
        words[word.capitalize()] = [1,0]
    elif word.capitalize() not in words and word != word.lower():
        words[word.capitalize()] = [1, 1]
    elif word.capitalize() in words and word == word.lower():
        words[word.capitalize()][0] += 1
    else:
        words[word.capitalize()][0] += 1
        words[word.capitalize()][1] += 1
print(words)

temp = []
dictlist = []
for key, (value1, value2) in words.items():
    temp = [key, value1, value2]
    dictlist.append(temp)
print(dictlist)

#connection to SQLlite
from sqlite3 import Error
def sql_connection():
    try:
        con = sqlite3.connect('mpdatabase.db')
        print("Connection is established: Database is created")
        return con
    except Error:
        print(Error)
def sql_table(con):
     cursorObj = con.cursor()
     cursorObj.execute("CREATE TABLE book_stat(book_name text, number_of_paragraph number, number_of_words number,"
                       "number_of_letters number, words_with_capital_letters number, words_in_lowercase number)")
     cursorObj.execute("CREATE TABLE input_file_stat(word text, count INT, count_uppercase INT)")
     cursorObj.execute("INSERT INTO book_stat VALUES (?, ?, ?, ?, ?, ?)", (title[0], number_of_paragraph[0], number_of_words [0], number_of_letters [0], word_Upper, word_lower))
     cursorObj.executemany("INSERT INTO input_file_stat VALUES (?, ?, ?)", dictlist)
     con.commit()
con = sql_connection()
sql_table(con)


