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
            record = parseUserInput(answer)
            #record is a list of search query lists e.g [[subj:gas][body:whale]]
            if outputFull==False:
                #start by getting first item as 'results'                
                results = intersect(record)
                #for i in list:
                    #i = str(i.decode("utf-8"))
                
                print(results)
            if outputFull==True:
                pass
    
    
def intersect(record):
    #start by getting first item as 'results'                
    results = getRecordsBrief(record[0][0],record[0][1])
    for i in range(1, len(record)):
        #now get second-last items from record as 'r'
        r = getRecordsBrief(record[i][0],record[i][1])
        #new results are the results that are in both 'results and 'r'
        results = set(results).intersection(r)
        # do this for all search query to find something that matches all   
    return results
    
        
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
        rowID = rangeSearch('s-'+data,'s-'+data,te,cte)
        subjList=[]
        for rID in rowID:
            record = re.get(rID.encode("utf-8"))
            subject = getText(record.decode("utf-8"),'subj')
            subjList.append(subject)
        results = rowID + subjList

        
        
        return results

    elif key == 'body:':
        results = rangeSearch('b-'+data,None,cte)
        return results
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

def getText(line,tag):
    # Gets the text obtained between the given tag <tag></tag>
    sTag = '<' + tag +'>'
    eTag = '</' + tag +'>'
    startIndex = line.find(sTag) + len(sTag)
    endIndex = line.find(eTag)  
    text = line[startIndex:endIndex]
    return text
    
    
        
def getSubject(subject):
    filetext = 'rtest.txt'.readall()
    pattern = "<subj>" + subject
    subjects = re.findall(pattern, filetext)
    return subjects

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
    
    groupsAll = subject + body + fromEmail + toEmail + dateEq + dateGr + dateLs + dateGrEq + dateLsEq + bcc + cc
    if line != '':
        remainingSearch = line.split(' ')
        for i in range(len(remainingSearch)):
            if remainingSearch[i] != '':
                remainingSearch[i] = 'general:' + remainingSearch[i]
        groupsAll = groupsAll + remainingSearch
    groupsAll = list(filter(lambda a: a != '', groupsAll))
    returnGroup = []
    for group in groupsAll:
        if ':' in group:
            splitGroup = group.split(":")
            splitGroup[0] = splitGroup[0].strip() + ":"
            splitGroup[1] = splitGroup[1].strip()
        if '>' in group:
            splitGroup = group.split(">")
            splitGroup[0] = splitGroup[0].strip() + ">"
            splitGroup[1] = splitGroup[1].strip()    
        if '<' in group:
            splitGroup = group.split("<")
            splitGroup[0] = splitGroup[0].strip() + "<"
            splitGroup[1] = splitGroup[1].strip()
        if '<=' in group:
            splitGroup = group.split("<=")
            splitGroup[0] = splitGroup[0].strip() + "<="
            splitGroup[1] = splitGroup[1].strip()
        if '>=' in group:
            splitGroup = group.split(">=")
            splitGroup[0] = splitGroup[0].strip() + ">="
            splitGroup[1] = splitGroup[1].strip()            
        returnGroup.append(splitGroup)
    return returnGroup

def rangeSearch(start,end,database,curs):
    while(True):
        returnsList=[]
        Starting_Name = start
        Ending_Name = end
        
        #get the record that has the smallest key greater than or equal to the Starting Name:
        result = curs.set_range(Starting_Name.encode("utf-8")) 
       
        if(result != None):
            while(result != None):
                #Checking the end condition: If the results comes after(or equal to) Ending_Name
                if(str(result[0].decode("utf-8")[0:len(Ending_Name)])>Ending_Name): 
                    break
                #x=str(result[0].decode("utf-8"))
                record = database.get(result[0])
                #x=str(record.decode("utf-8"))
                returnsList.append(record.decode("utf-8"))
                result = curs.next() 
            return returnsList
        else:
            return returnsList
        
    
if __name__ == '__main__':
    main()
