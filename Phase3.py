from bsddb3 import db
import subprocess
import re
import time

def main():
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
            userQuery = parseUserInput(answer)
            #START HERE!!!
            results = intersect(userQuery) #first, call intersect on the user's query that was parsed (now go to intersect function)
            
            
            if outputFull==False:
                #for every result(ID), search for the data in re file and print brief
                for id in row ids:
                    get id, re.idx
                    
                for i in results:
                    print(i[0]+', '+i[1])
                print()
            if outputFull==True:
                #for every result(ID), search for the data in re file and print full
                pass
    cem.close()
    cte.close()
    cda.close()
    cre.close()
    re.close()
    da.close()
    te.close()
    em.close()    

def intersect(userQuery): 
    #this function will get rowIDs found that matches all user's search queries
    #(dont change anything here)
    #go to getRecordIDs (renamed)
    #userQuery is [[search sub,search term][sub,term]]
    
    
    #start by getting first item as 'results'                
    results = getRecordIDs(userQuery[0][0],userQuery[0][1])
    for i in range(1, len(userQuery)):
        #now get second-last items from record as 'r'
        r = getRecordIDs(userQuery[i][0],userQuery[i][1])
        #new results are the results that are in both 'results and 'r'
        results = set(results).intersection(r)
        # do this for all search query to find something that matches all   
    return results
    
        
def getRecordIDs(key,data): #
    # NEED TO WORK ON THIS PART
#Accesses the database and returns the record


    #each of these will return rowIDs found for this user's search query, very simple oen line
    if key == 'subj:':
        rowID = rangeSearch('s-'+data,'s-'+data,te,cte)

        return rowID

    elif key == 'body:':
        rowID = rangeSearch('b-'+data,'b-'+data,te,cte)
        bodyList=[]
        results=[]
        for rID in rowID:
            record = re.get(rID.encode("utf-8"))
            body = getText(record.decode("utf-8"),'subj')
            results.append([rID,body])
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
            return set(returnsList)
        else:
            return set(returnsList)
        
    
if __name__ == '__main__':
    main()
