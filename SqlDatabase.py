import sqlite3
import os
import logging


logging.basicConfig(filename="loggingmp.log", level=logging.INFO)


class SqlDatabase:
    def __init__(self, db_folder, name):
        self.db_folder = db_folder
        self.name = name

    def sql_connection(self):
        os.chdir(self.db_folder)
        try:
            con = sqlite3.connect(self.name)
            logging.info("Connection is established: Database is created")
            return con
        except sqlite3.Error:
            print(sqlite3.Error)

    def create_book_stat_table(self):
        connection = sqlite3.connect(self.db_folder + '/' + self.name)
        cursorObj = connection.cursor()
        if not cursorObj.execute("Select * FROM book_stat WHERE 1=2"):
            cursorObj.execute("CREATE TABLE book_stat(book_name text, number_of_paragraph number, number_of_words number,"
                       "number_of_letters number, words_with_capital_letters number, words_in_lowercase number)")

    def create_input_file_stat_table(self):
        connection = sqlite3.connect(self.db_folder + '/' + self.name)
        cursorObj = connection.cursor()
        cursorObj.execute("CREATE TABLE input_file_stat(word text, count INT, count_uppercase INT)")

    def insert_book_stat_values(self, book_name,number_of_paragraph, number_of_words, number_of_letters,
                                word_Upper, word_lower):
        connection = sqlite3.connect(self.db_folder + '/' + self.name)
        cursorObj = connection.cursor()
        cursorObj.execute("INSERT INTO book_stat VALUES (?, ?, ?, ?, ?, ?)", (
        book_name, number_of_paragraph, number_of_words, number_of_letters, word_Upper, word_lower))
        connection.commit()

    def insert_input_file_stat_values(self, word, total, capital):
        connection = sqlite3.connect(self.db_folder + '/' + self.name)
        cursorObj = connection.cursor()
        cursorObj.execute("INSERT INTO input_file_stat VALUES (?, ?, ?)", (word, total, capital))
        connection.commit()

    def drop(self, table):
        connection = sqlite3.connect(self.db_folder + '/' + self.name)
        cursor = connection.cursor()
        cursor.execute('drop table {}'.format(table))
        cursor.close()
        connection.close()