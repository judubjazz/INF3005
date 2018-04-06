# # https://stackoverflow.com/questions/3310584/insert-binary-file-in-sqlite-database-with-python
#
# import sqlite3
# from database import Database
#
# # let's just make an arbitrary binary file...
# with open('/tmp/abin', 'wb') as f:
#   f.write(''.join(chr(i) for i in range(55)))
# # ...and read it back into a blob
# with open('/tmp/abin', 'rb') as f:
#   ablob = f.read()
#
# # OK, now for the DB part: we make it...:
# db = sqlite3.connect('/tmp/thedb')
# db.execute('CREATE TABLE t (thebin BLOB)')
# db.execute('INSERT INTO t VALUES(?)', [buffer(ablob)])
# db.commit()
# db.close()
#
# # ...and read it back:
# db = sqlite3.connect('/tmp/thedb')
# row = db.execute('SELECT * FROM t').fetchone()
# print (repr(str(row[0])))
#
#
# # https://stackoverflow.com/questions/3309957/pysqlite-how-to-save-images
# #write
# connection = sqlite3.connect('/home/ju/JetBrainsProjects/PycharmProjects/webII_tp2/db/database.db')
# cursor = connection.cursor()
# cursor.execute('insert into Animal (id, name, type, race, age, date_creation, description, photo_url, owner_id) values (?,?,?)', (id, name, sqlite3.Binary(file.read())))
#
# #read
# file = cursor.execute('select photo_url from Animal where id=?', (id,)).fetchone()
#
# #toapp
# # return cStringIO.StringIO(file['bin'])


# http://snipplr.com/view/10127/sqlite-3-insert-binary-image-data-with-python/
import sqlite3
import datetime
import base64



con = sqlite3.connect('/home/ju/JetBrainsProjects/PycharmProjects/webII_tp2/db/database.db')
cur = con.cursor()
now = datetime.datetime.now()

# with open('/home/ju/JetBrainsProjects/PycharmProjects/webII_tp2/static/img/rhino.jpeg', "rb") as input_file:
#     imagedata = input_file.read()
name = 'bearette'
type = 'bear'
race = 'bearus'
age = 5
date = now.isoformat()
description = 'beautiful rhinoceros'
img_url = "../static/img/bear.jpeg"
# img_data = base64.b64encode(imagedata)
# img_data = [memoryview(imagedata)]
cur.execute('INSERT INTO Animal'
            '(id, name, type, race, age, date_creation, description, img_url, owner_id)'
            ' VALUES (?,?,?,?,?,?,?,?,?)', (1,name,type,race,age,date,description,img_url,1))
con.commit()

# with open('/home/ju/JetBrainsProjects/PycharmProjects/webII_tp2/db/img/squirel.jpeg', "rb") as input_file:
#     imagedata = input_file.read()
name = 'squirette'
type = 'rat'
race = 'squirus'
age = 5
date = now.isoformat()
description = 'beautiful squirel'
img_url = "../static/img/squirel.jpeg"
# img_data = base64.b64encode(imagedata)
# img_data = sqlite3.Binary(imagedata)
cur.execute('INSERT INTO Animal'
            '(id, name, type, race, age, date_creation, description, img_url, owner_id)'
            ' VALUES (?,?,?,?,?,?,?,?,?)', (2,name,type,race,age,date,description,img_url,2))
con.commit()

# with open('/home/ju/JetBrainsProjects/PycharmProjects/webII_tp2/db/img/panda.jpeg', "rb") as input_file:
#     imagedata = input_file.read()
name = 'pandette'
type = 'panda'
race = 'pandus'
age = 5
date = now.isoformat()
description = 'beautiful panda'
img_url = "../static/img/panda.jpeg"
# img_data = base64.b64encode(imagedata)
# img_data = sqlite3.Binary(imagedata)
cur.execute('INSERT INTO Animal'
            '(id, name, type, race, age, date_creation, description, img_url, owner_id)'
            ' VALUES (?,?,?,?,?,?,?,?,?)', (3,name,type,race,age,date,description,img_url,3))
con.commit()

# with open('/home/ju/JetBrainsProjects/PycharmProjects/webII_tp2/db/img/zebra.jpeg', "rb") as input_file:
#     imagedata = input_file.read()
name = 'zebrette'
type = 'horse'
race = 'zebrus'
age = 5
date = now.isoformat()
description = 'beautiful zebra'
img_url = "../static/img/zebra.jpeg"
# img_data = base64.b64encode(imagedata)
# img_data = sqlite3.Binary(imagedata)
cur.execute('INSERT INTO Animal'
            '(id, name, type, race, age, date_creation, description, img_url, owner_id)'
            ' VALUES (?,?,?,?,?,?,?,?,?)', (4,name,type,race,age,date,description,img_url,4))
con.commit()


# with open('/home/ju/JetBrainsProjects/PycharmProjects/webII_tp2/db/img/elephant.jpeg', "rb") as input_file:
#     imagedata = input_file.read()
name = 'elephette'
type = 'elephant'
race = 'elephus'
age = 5
date = now.isoformat()
description = 'beautiful elephant'
img_url = "../static/img/elephant.jpeg"
# img_data = base64.b64encode(imagedata)
# img_data = sqlite3.Binary(imagedata)
cur.execute('INSERT INTO Animal'
            '(id, name, type, race, age, date_creation, description, img_url, owner_id)'
            ' VALUES (?,?,?,?,?,?,?,?,?)', (5,name,type,race,age,date,description,img_url,5))
con.commit()


con.close()