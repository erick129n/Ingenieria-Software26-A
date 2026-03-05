import mysql.connector

connection = mysql.connector.connect(host='localhost', username='root', password='', database='taller_mecanico', port=3308)

cursor = connection.cursor()
query1 = 'select * from usuarios'
cursor.execute(query1)
table = cursor.fetchall()
for row in table:
    print(row)

print('Table description:')
query2 = 'DESC usuarios'
cursor.execute(query2)
table2 = cursor.fetchall()
for row in table2:
    print(row)

cursor.close()
connection.close()