from bsddb3 import db
import subprocess
import re

def main():
    quit = False
    outputFull = False
    
    
    while not quit:
        answer = input('Type "output=full" to view the full record. \nType "output=brief" to return to default view. \nType "q" to quit. \nPlease enter your queries: ')
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
    
    
def processQuery(answer,outputFull):
    # NEED TO WORK ON THIS PART
#Processes string to pass to getRecords
    getRecords(key,data,outputFull)
       
        
def getRecords(key,data,outputFull):
    # NEED TO WORK ON THIS PART
#Accesses the database and retursn the record
    d1,d2,d3,d4 = db.DB()
    d1.set_flags(db.DB_DUP)
    d2.set_flags(db.DB_DUP)
    d3.set_flags(db.DB_DUP)
    d4.set_flags(db.DB_DUP)
       
    d4.open('da.idx', None, db.DB_BTREE, db.DB_CREATE)
    d3.open('em.idx', None, db.DB_BTREE, db.DB_CREATE)
    d2.open('te.idx', None, db.DB_BTREE, db.DB_CREATE)
    d1.open('re.idx', None, db.DB_HASH, db.DB_CREATE)
    
    c1 = d1.cursor()
    c2 = d2.cursor()
    c3 = d3.cursor()
    c4 = d4.cursor()
    

    if key == 'subj:':
        pass
    elif key == 'body:':
        pass
    elif key == 'from:':
        pass
    elif key == 'to:':
        pass
    elif key == 'date:':
        pass
    elif key == 'date>':
        pass
    elif key == 'date<':
        pass    
    elif key == 'date>=':
        pass
    elif key == 'date<=':
        pass    
    elif key == 'bcc:':
        pass
    elif key== 'cc:':
        pass
    elif '%' in data:
        pass
    else:
        return 'Could not process query please try again'
    

    
    c1.close()
    c2.close()
    c3.close()
    c4.close()
    d1.close()
    d2.close()
    d3.close()
    d4.close()    
    
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
