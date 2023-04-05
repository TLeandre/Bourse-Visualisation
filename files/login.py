
import  sqlite3
import os 

from passlib.hash import sha256_crypt
from threading import Lock

db = sqlite3.connect('database.db', check_same_thread=False)
cursor = db.cursor()

lock = Lock()

def connect(email, password):

    try:
        lock.acquire(True)
        cursor.execute("""SELECT PASSWORD, 
                            ID_USER FROM USERS 
                            WHERE EMAIL = '%s' """ % (str(email)) )
        pw = cursor.fetchall()
        return sha256_crypt.verify(password, pw[0][0]), pw[0][1]
    except:
        return False, 0
    finally:
        lock.release()
    
def sign_in(name, surname, email, password):

    cursor.execute("""SELECT EMAIL FROM USERS WHERE EMAIL = '%s' """ % (str(email)))
    mail = cursor.fetchall()

    if len(mail) <= 0:

        pw = sha256_crypt.hash(password)
        cursor.execute("""INSERT INTO USERS(NAME, SURNAME, EMAIL, PASSWORD) 
                        VALUES ('%s','%s','%s','%s')""" % (name, surname, email, pw))
        db.commit()
        return 0
    else :
        return -1 
