from bsddb3 import db
import subprocess
import re
import time

def main():
    quit = False
    outputFull = False
    
    
    while not quit:
        answer = input('Type "output=full" to view the full record. \nType "output=brief" to return to default view. \nType "q" to quit. \nPlease enter your queries: ')
        answer = answer.lower()
        if answer == 'output=full':
            outputFull = True
            print('-------------\nOutput has been changed to full view.\n')
        elif answer == 'output=brief':
            outputFull = False
            print('-------------\nOutput has been changed to brief view.\n')
        elif answer == 'q':
            quit=True
        else:
            record = processQuery(answer)
            print(record)
    
    
def processQuery(answer,outputFull):
    # NEED TO WORK ON THIS PART
#Processes string to pass to getRecords
    if outputFull == False:
        getRecordsBrief(key,data)
        return record
    else:
        getRecordsFull(key,data)
        return record
    
        
def getRecordsBrief(key,data):
    # NEED TO WORK ON THIS PART
#Accesses the database and returns the record
    da = db.DB()
    em = db.DB()
    te = db.DB()
    re = db.DB()
    
    da.set_flags(db.DB_DUP)
    em.set_flags(db.DB_DUP)
    te.set_flags(db.DB_DUP)
    re.set_flags(db.DB_DUP)
       
    da.open('da.idx', None, db.DB_BTREE, db.DB_CREATE)
    em.open('em.idx', None, db.DB_BTREE, db.DB_CREATE)
    te.open('te.idx', None, db.DB_BTREE, db.DB_CREATE)
    re.open('re.idx', None, db.DB_HASH, db.DB_CREATE)
    
    cda = da.cursor()
    cem = em.cursor()
    cte = te.cursor()
    cre = re.cursor()
    

    if key == 'subj:':
        result = te.get('s-'+data)
        
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

#if __name__ == '__main__':
    #main()
