import hmac
import sys
import hashlib
import mysql.connector
from mysql.connector import Error

SymmetricKey = "OvercomeAdversity"

try:#Try to connect to mysql
    connection = mysql.connector.connect(user='root', password='Pokemon42',#My Personal user password
                                         host='localhost',#The host
                                         database='dspproject',#The database with the tables
                                         port='3307')#My mysql is on port 3307 so I have to specify the port, the default port is 3306
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor(buffered=True)
        cursor = connection.cursor() 
        que = 'SELECT * FROM project'
        cursor.execute(que)
        res = cursor.fetchall()

        mes = ''
        for r in res:
            mes = str(r)
            hashmac = hmac.new(SymmetricKey.encode(),mes.encode(), hashlib.sha256)
            print(r)
            print('\n')
            print(r[0])
            print('\n')
            print(r[1])
            print('\n')
            print(hashmac.hexdigest())
            print('\n')
            insert = "UPDATE project SET hashMAC = '" + hashmac.hexdigest() + "' " + "WHERE first_name = '" + r[0] + "' AND last_name = '" + r[1] + "';"
            print(insert)
            cursor.execute(insert)
            connection.commit()
except Error as e:
    print("Error while connecting to MySQL", e)
finally:#Closes connection
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")