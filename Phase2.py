from bsddb3 import db
DB_File = "data.db"
database = db.DB()
database.set_flags(db.DB_DUP) #declare duplicates allowed before you create the database
database.open(DB_File,None, db.DB_HASH, db.DB_CREATE)
curs = database.cursor()

#Insert key-values including duplicates …
database.put(b'key1', "value1")
database.put(b'key1', "value2")
database.put(b'key2', "value1")
database.put(b'key2', "value2")





curs.close()
database.close()
