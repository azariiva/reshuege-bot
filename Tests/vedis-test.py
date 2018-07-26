from vedis import Vedis


db = Vedis('mydb.vdb')
line = db[1]
print(db[2].decode())
db[2] = 'Русский'
