from bsddb3 import db
import subprocess

def main():

    DB_File = "data.db"
    database = db.DB()
    database.set_flags(db.DB_DUP) #declare duplicates allowed before you create the database
    database.open(DB_File,None, db.DB_HASH, db.DB_CREATE)
    curs = database.cursor()

    
    curs.close()
    database.close()


if __name__ == '__main__':
    main()