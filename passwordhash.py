import sys
import hashlib
import mysql.connector
from mysql.connector import Error

user = False
admin = False

username = input("Input Username\n")#Ask user for their username
password = input("Input a password\n")#Ask user for their password

sha256 = hashlib.sha256()#initialize hash

sha256.update(password.encode('utf-8'))#We hash the string because the password stored in the db is hashed for security reasons
string_hash = sha256.hexdigest()#Turn hashed password into a string

usernameTuple = (username,)#Puts username into a tuple to compare to the admin table later
userTuple = (username,string_hash,)#Puts username and the password hash into a tuple for users table comparison

print(userTuple)

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
        query = 'SELECT username,passwordhash FROM users'#Query to get relevant user data from the users table
        cursor.execute(query)
        result = cursor.fetchall()#Putting the results from the query into a list of tuples

        for r in result:#loop through list
            if(r == userTuple):#compare result to the tuple of username and hash
                print("User Verified")
                adminQue = 'SELECT username FROM admins'#Admins table exists for access control
                cursor.execute(adminQue)
                record = cursor.fetchall()
                for a in record:#Loop through admin table results
                    if(a == usernameTuple):
                        print("User is Admin")
                        admin = True
                        break
                user = True
                break
        if user is True and admin is not True:
            que = 'SELECT gender,age,weight,height,health_history FROM project'
            cursor.execute(que)
            res = cursor.fetchall()
            for r in res:
                print(r)
                print('\n')
        elif admin is True:
            que = 'SELECT * FROM project'
            cursor.execute(que)
            res = cursor.fetchall()
            print(res)
            for r in res:
                print(r)
                print('\n')
except Error as e:
    print("Error while connecting to MySQL", e)
finally:#Closes connection
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")