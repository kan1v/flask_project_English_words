import math 
import sqlite3
import time 
import random

class FDataBase:
    def __init__(self,db):
        self.__db = db
        self.__cur = db.cursor()
    
    def getMenu(self):
        sql = '''SELECT * FROM mainmenu'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print('Ошибка чтения из базы данных')

    def getRandomWord(self):
        try:
            self.__cur.execute('SELECT eng_word, ru_word FROM words')
            words = self.__cur.fetchall()
            if words:
                return random.choice(words)
        except sqlite3.Error as e:
            print(f'Ошибка получения слов из базы данных: {e}')
        
        return None
    
    def getUserUsername(self, username):
        try:
            self.__cur.execute(f"SELECT COUNT() as 'count' FROM users WHERE username LIKE ?", (username,))
            res = self.__cur.fetchone()
            if res['count'] > 0:
                return res
        except sqlite3.Error as e:
            print(f'Ошибка проверки по username пользователя в БД: {e}')

        
    def getUserEmail(self, email):
        try:
            self.__cur.execute(f"SELECT COUNT() as 'count' FROM users WHERE email LIKE ?", (email,))
            res = self.__cur.fetchone()
            if res['count'] > 0:
                return res
        except sqlite3.Error as e:
            print(f'Ошибка проверки по email пользователя в БД: {e}')

    def getUSer(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = ? LIMIT 1", (user_id,))
            res = self.__cur.fetchone()
            if not res:
                print('Пользователь не найден')
                return False
        except sqlite3.Error as e:
            print(f'Ошибка получения данных из БД: {e}')

    def addUser(self, username, email, hashpsw):
        try:
            tm = math.floor(time.time())
            self.__cur.execute(f"INSERT INTO users VALUES(NULL, ?,?,?,?)", (username, email, hashpsw, tm)) 
            self.__db.commit()
        except sqlite3.Error as e:
            print(f'Ошибка добавления пользоваетля в БД: {e}')     
            return False

        return True

    def getUserByEmail(self, email):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE email = ? LIMIT 1", (email,))
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False
            
            return res
        except sqlite3.Error as e:
            print(f'Ошибка получения данных из БД: {e}')

        return False

    def addNewWords(self, eng_word, ru_word):
        try:
            self.__cur.execute(f"INSERT INTO words VALUES(NULL, ?, ?)", (eng_word, ru_word)) 
            self.__db.commit()
        except sqlite3.Error as e:
            print(f"Ошибка добавления слов в БД: {e}")
            return False

        return True       
