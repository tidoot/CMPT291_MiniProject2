from bsddb3 import db
import subprocess
import re

def main():
    quit = False
    outputFull = False
    
    d1,d2,d3,d4 = db.DB()
       
    d4.open('da.idx', None, db.DB_BTREE, db.DB_CREATE)
    d3.open('em.idx', None, db.DB_BTREE, db.DB_CREATE)
    d2.open('te.idx', None, db.DB_BTREE, db.DB_CREATE)
    d1.open('re.idx', None, db.DB_HASH, db.DB_CREATE)
    
    c1 = d1.cursor()
    c2 = d2.cursor()
    c3 = d3.cursor()
    c4 = d4.cursor()
    
    while not quit:
        answer = input('Type "output=full" to view the full record. \nType "output=brief" to return to default view. \nType "q" to quit. \nPlease enter your queries: ')
        answer = answer.lower()
        if answer == 'output=full':
            outputFull = True
            print('-------------\nOutput has been changed to full view.\n')
        elif answer == 'output=brief':
            outputFull = False
            print('-------------\nOutput has been changed to briew view.\n')
        elif answer == 'q':
            quit=True
        else:
            record = processQuery(answer)
            print(record)
    
    
    def processQuery(answer):
        # NEED TO WORK ON THIS PART
    #Processes string to pass to getRecords
        getRecords(idx,answer)
       
        
    def getRecords(idx,answer):
        # NEED TO WORK ON THIS PART
    #Accesses the database and retursn the record
        database = db.DB()
        curs = database.cursor()
        database.open(idx)        
        curs.close()
        database.close() 
        
        # NEED TO WORK ON THIS PART
        if outputFull == False:
            #Prints record in brief view
            return record
        elif outputFull == True:
            #Prints full record
            return record  
        
def getSubject():
    filetext = 'rtest.txt'.readall()
    subject = input("Enter Subject")
    pattern = "<subj>" + subject
    re.findall(pattern, filetext)

def getKey(idxLst):
    for idx in idxLst:
        db3.get(idx)

if __name__ == '__main__':
    main()
