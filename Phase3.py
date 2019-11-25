from bsddb3 import db
import subprocess
import re
import time

def main():
    quit = False
    outputFull = False
    line = 'subj : kenneth.shulklapper@enron.com  to:keith.holst@enron.com subj:jennifer.medcalf@enron.com confidential shares date>2001/03/10'
    print(parseUserInput(line))
    
    
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
        
def parseUserInput(line):
    subject = re.findall('subj[ ]*:[ ]*[^ ]*', line)
    for match in subject:
        line = line.replace(match,'')
    body = re.findall('body[ ]*:[ ]*[^ ]*', line)
    for match in body:
        line = line.replace(match,'')    
    fromEmail = re.findall('from[ ]*:[ ]*[^ ]*', line)
    for match in fromEmail:
        line = line.replace(match,'')    
    toEmail = re.findall('to[ ]*:[ ]*[^ ]*', line)
    for match in toEmail:
        line = line.replace(match,'')    
    dateEq = re.findall('date[ ]*:[ ]*[^ ]*', line)
    for match in dateEq:
        line = line.replace(match,'')    
    dateGr = re.findall('date[ ]*>[ ]*[^ ]*', line)
    for match in dateGr:
        line = line.replace(match,'')    
    dateLs = re.findall('date[ ]*<[ ]*[^ ]*', line)
    for match in dateLs:
        line = line.replace(match,'')    
    dateGrEq = re.findall('date[ ]*>=[ ]*[^ ]*', line)
    for match in dateGrEq:
        line = line.replace(match,'')    
    dateLsEq = re.findall('date[ ]*<=[ ]*[^ ]*', line)
    for match in dateLsEq:
        line = line.replace(match,'')    
    bcc = re.findall('bcc[ ]*:[ ]*[^ ]*', line)
    for match in bcc:
        line = line.replace(match,'')    
    cc = re.findall('cc[ ]*:[ ]*[^ ]*', line)
    for match in cc:
        line = line.replace(match,'')
    line = line.strip()
    remainingSearch = line.split(' ')
    for i in range(len(remainingSearch)):
        if remainingSearch[i].isalpha():
            remainingSearch[i] = 'general:' + remainingSearch[i]
    groupsAll = subject + body + fromEmail + toEmail + dateEq + dateGr + dateLs + dateGrEq + dateLsEq + bcc + cc + remainingSearch
    
    returnGroup = []
    for group in groupsAll:
        splitGroup = re.split(':|>|<|>=|<=',group)
        splitGroup[0] = splitGroup[0].strip()
        splitGroup[1] = splitGroup[1].strip()
        returnGroup.append(splitGroup)
    return returnGroup
        
    
#if __name__ == '__main__':
    #main()
