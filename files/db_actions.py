import pandas as pd
import actions_info
import sqlite3

db = sqlite3.connect('database.db', check_same_thread=False)
cursor = db.cursor()

def get_actions(id):
    cursor.execute("""SELECT OPERATIONS.DATE, ACTIONS.SYMBOLE, ACTIONS.NAME, OPERATIONS.PRICE, OPERATIONS.QUANTITY 
                    FROM OPERATIONS 
                    INNER JOIN ACTIONS 
                    ON OPERATIONS.ID_ACTION = ACTIONS.ID_ACTION 
                    WHERE OPERATIONS.ID_USER = 
                    """ + str(id) )
    columns = list(map(lambda x: x[0], cursor.description))

    actions = pd.DataFrame(cursor.fetchall())
    actions = actions.set_axis(columns, axis='columns')
    actions = actions.set_index([columns[0]])

    return actions 

def get_quantity_actions(id):
    cursor.execute("""SELECT AVERAGE.SYMBOLE, AVERAGE.PRICE, SUM(OPERATIONS.QUANTITY) as QUANTITY
                        FROM (SELECT OP.ID_ACTION, ROUND(AVG(OP.PRICE),2) as PRICE, ACTIONS.SYMBOLE
                            FROM OPERATIONS as OP
                            INNER JOIN ACTIONS ON ACTIONS.ID_ACTION=OP.ID_ACTION
                            WHERE OP.QUANTITY > 0 AND OP.ID_USER = %s
                            GROUP BY OP.ID_ACTION) as AVERAGE
                        INNER JOIN OPERATIONS ON AVERAGE.ID_ACTION=OPERATIONS.ID_ACTION
                        WHERE OPERATIONS.ID_USER = %s
                        GROUP BY OPERATIONS.ID_ACTION
                        HAVING QUANTITY > 0 """ % (id,id)) 
    columns = list(map(lambda x: x[0], cursor.description))

    actions = pd.DataFrame(cursor.fetchall())
    actions = actions.set_axis(columns, axis='columns')

    return actions 

def add_operation(symbole, date, price, quantity, id_user, buy):
    
    ## Récupère l'id de l'action souhaité 
    cursor.execute("""SELECT ID_ACTION FROM ACTIONS where SYMBOLE = '%s' """ % (symbole))
    id_action = cursor.fetchall()
    
    ## Verification que l'action est dans la base de donnée 
    if len(id_action) <= 0:

        
        ## ajouter une verification que l'action existe bien 
        if actions_info.action_exit(symbole) == 0:
            
            ## Ajout de l'action dans la base de donnée
            cursor.execute("""INSERT INTO ACTIONS(NAME, SYMBOLE) 
                    VALUES ('%s','%s')""" % (symbole, symbole))
            db.commit() 
        
            ## relance la fonction
            return add_operation(symbole, date, price, quantity, id_user, buy)
        
        else:
            return -1
        
    else :
        if buy == -1:
            try: 
                cursor.execute( """SELECT SUM(QUANTITY) AS QUANTITY FROM OPERATIONS WHERE ID_USER = %s AND ID_ACTION = %s""" % (id_user, id_action[0][0]))
                quant  = cursor.fetchall()

                if int(quant[0][0]) + quantity * buy >= 0:

                    ## Ajout de l'opération
                    cursor.execute("""INSERT INTO OPERATIONS(DATE, PRICE, QUANTITY, ID_ACTION, ID_USER)
                            VALUES ('%s','%s','%s','%s','%s')""" % (date, price, quantity * buy, id_action[0][0], id_user))
                    db.commit()
                    return 1

                else:
                    return 0
                
            except (ValueError, TypeError) as err:
                return -1
        else :
            ## Ajout de l'opération
            cursor.execute("""INSERT INTO OPERATIONS(DATE, PRICE, QUANTITY, ID_ACTION, ID_USER)
                    VALUES ('%s','%s','%s','%s','%s')""" % (date, price, quantity * buy, id_action[0][0], id_user))
            db.commit()





