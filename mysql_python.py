import os
import pymysql
from flask import Flask

username = os.getenv('C9_USER')

connection = pymysql.connect(host='localhost',
                            user=username,
                            password='',
                            db='RecipeBook')
                            
try:
    with connection.cursor() as cursor:
        sql = "SELECT * FROM USER;"
        cursor.execute(sql)
        result=cursor.fetchall()
        print(result)

finally:
    connection.close()
    