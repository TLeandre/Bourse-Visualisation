import sqlite3

con = sqlite3.connect('database.db')
cur = con.cursor()

sql = '''CREATE TABLE USERS (
                  ID_USER INTEGER PRIMARY KEY AUTOINCREMENT,
                  NAME VARCHAR(10) NOT NULL,
                  SURNAME VARCHAR(10) NOT NULL,
                  EMAIL VARCHAR(10) NOT NULL,
                  PASSWORD VARCHAR(10) NOT NULL
           )'''
cur.execute(sql)
con.commit()

sql = '''CREATE TABLE ACTIONS (
                ID_ACTION INTEGER PRIMARY KEY AUTOINCREMENT,
                NAME VARCHAR(64) NOT NULL,
                SYMBOLE VARCHAR(16) NOT NULL
           )'''
cur.execute(sql)
con.commit()

sql = '''CREATE TABLE WALLETS (
                ID_WALLET INTEGER PRIMARY KEY AUTOINCREMENT,
                DATE TEXT NOT NULL,
                AMOUNT FLOAT NOT NULL,
                ID_USER INTEGER NOT NULL,
                FOREIGN KEY(ID_USER) REFERENCES USERS(ID_USER)
           )'''
cur.execute(sql)
con.commit()

sql = '''CREATE TABLE OPERATIONS (
                ID_OPERATION INTEGER PRIMARY KEY AUTOINCREMENT,
                DATE TEXT NOT NULL,
                PRICE FLOAT NOT NULL,
                QUANTITY INTEGER NOT NULL,
                ID_ACTION INTEGER NOT NULL,
                ID_USER INTEGER NOT NULL,
                FOREIGN KEY(ID_ACTION) REFERENCES ACTIONS(ID_ACTION),
                FOREIGN KEY(ID_USER) REFERENCES USERS(ID_USER)
           )'''
cur.execute(sql)
con.commit()

sql = '''CREATE TABLE DIVIDENDES (
                ID_DIVIDENDE INTEGER PRIMARY KEY AUTOINCREMENT,
                DATE TEXT NOT NULL,
                AMOUNT FLOAT NOT NULL,
                ID_ACTION INTEGER NOT NULL,
                ID_USER INTEGER NOT NULL,
                FOREIGN KEY(ID_ACTION) REFERENCES ACTIONS(ID_ACTION),
                FOREIGN KEY(ID_USER) REFERENCES USERS(ID_USER)
           )'''
cur.execute(sql)
con.commit()