from bsddb3 import db
import subprocess

def main():
    '''
    DB_File = "data.db"
    database = db.DB()
    database.set_flags(db.DB_DUP) #declare duplicates allowed before you create the database
    database.open(DB_File,None, db.DB_HASH, db.DB_CREATE)
    curs = database.cursor()

    def recsIndex():
        pass
    
    def termsIndex():
        pass
    
    def emailsIndex():
        pass
    
    def datesIndex():
        pass
    
    curs.close()
    database.close()
    '''
    sortFiles()
    parseFiles()

def sortFiles():
    subprocess.call(['sort', '-u', '-o', 'terms.txt', 'terms.txt'])  
    subprocess.call(['sort', '-u', '-o', 'recs.txt', 'recs.txt'])  
    subprocess.call(['sort', '-u', '-o', 'emails.txt', 'emails.txt'])  
    subprocess.call(['sort', '-u', '-o', 'dates.txt', 'dates.txt'])  

def parseFiles():
    termsDataList, termsKeyList = parseFile('terms.txt')
    emailsDataList, emailsKeyList = parseFile('emails.txt')
    datesDataList, datesKeyList = parseFile('dates.txt')
    recsKeyList, recsDataList = parseFile('recs.txt') #recs is reversed key,data

def parseFile(file):
    f = open(file,'r')
    dataList = []
    keyList = []
    lines = f.read().splitlines()
    for line in lines:
        data,key = line.split(':', 1) #split at first occurance of semicolon only, applicable for recs
        key = key.replace('\\','') #remove backslash
        data = data.replace('\\','')
        dataList.append(data)
        keyList.append(keys)
    f.close()
    return dataList, keyList

def loadDB(file):
    pass
    #subprocess.call(['db_load', '-c', 'duplicates', '-t', 'Btree', '-f']) 

if __name__ == '__main__':
    main()