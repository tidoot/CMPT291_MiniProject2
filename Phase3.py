from bsddb3 import db
import datetime
from datetime import *
import subprocess
import re
import time

da = db.DB()
em = db.DB()
te = db.DB()
rec = db.DB()

da.set_flags(db.DB_DUP)
em.set_flags(db.DB_DUP)
te.set_flags(db.DB_DUP)
rec.set_flags(db.DB_DUP)
   
da.open('da.idx', None, db.DB_BTREE, db.DB_CREATE)
em.open('em.idx', None, db.DB_BTREE, db.DB_CREATE)
te.open('te.idx', None, db.DB_BTREE, db.DB_CREATE)
rec.open('re.idx', None, db.DB_HASH, db.DB_CREATE)

cda = da.cursor()
cem = em.cursor()
cte = te.cursor()
cre = rec.cursor()
    
def main():   
    quit = False
    outputFull = False

    #Main interface
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
        elif len(answer)==0:
            print()
        else:
            userQuery = parseUserInput(answer.lower())
            rowIdList = intersect(userQuery) #first, call intersect on the user's query that was parsed (now go to intersect function)
            results=[]
            for rowId in rowIdList:
                record = rec.get(rowId.encode('utf-8'))
                if outputFull==False:
                    body = getText(record.decode('utf-8'), 'subj')
                elif outputFull:
                    body = record.decode('utf-8')
                results.append([rowId,body])    
            if len(results)==0:
                print('No results found. Please try again')
            else:
                for i in results:
                    print(i[0]+', '+i[1])
            print()

    cem.close()
    cte.close()
    cda.close()
    cre.close()
    rec.close()
    da.close()
    te.close()
    em.close()    

def intersect(userQuery): 
    #this function will get rowIDs found that matches all user's search queries
    #go to getRecordIDs   
    #start by getting first item as 'results'                
    results = getRecordIDs(userQuery[0][0],userQuery[0][1])
    for i in range(1, len(userQuery)):
        #now get second-last items from record as 'r'
        r = getRecordIDs(userQuery[i][0],userQuery[i][1])
        #new results are the results that are in both 'results and 'r'
        results = set(results).intersection(r)
        # do this for all search query to find something that matches all   
    return results 
        
def getRecordIDs(key,data): 
    #Accesses the database and returns the record
    #each of these will return rowIDs found for this user's search query
    if key == 'subj:':
        if '%' in data:
            rowID = rangeSearch('s-'+data,'s-'+data,te,cte, True)
            return rowID
        else:
            rowID = rangeSearch('s-'+data,'s-'+data,te,cte)
            return rowID
    elif key == 'body:':
        if '%' in data:
            rowID = rangeSearch('b-'+data,'b-'+data,te,cte, True)
            return rowID
        else:
            rowID = rangeSearch('b-'+data,'b-'+data,te,cte)
            return rowID
    elif key == 'general:':
        if '%' in data:
            rowID = rangeSearch('b-'+data,'b-'+data,te,cte, True)
            rowID2 = rangeSearch('s-'+data,'s-'+data,te,cte, True)
        else:
            rowID = rangeSearch('b-'+data,'b-'+data,te,cte)
            rowID2 = rangeSearch('s-'+data,'s-'+data,te,cte)                    
        rowID = rowID.union(rowID2)
        return rowID
    elif key == 'from:':
        rowID = rangeSearch('from-'+data,'from-'+data,em,cem)
        return rowID
    elif key == 'to:':
        rowID = rangeSearch('to-'+data,'to-'+data,em,cem)
        return rowID
    elif key == 'date:':
        rowID = rangeSearch(data,data,da,cda)
        return rowID
    elif key == 'date>':
        data = datetime.strptime(data, '%Y/%m/%d')
        date = str(datetime.date(data) + timedelta(days=1)).replace('-','/')
        rowID = rangeSearch(date,'9999/12/31',da,cda, True)
        return rowID
    elif key == 'date<':
        data = datetime.strptime(data, '%Y/%m/%d')
        date = str(datetime.date(data) - timedelta(days=1)).replace('-','/')
        rowID = rangeSearch('0000/00/00',date,da,cda, True)
        return rowID  
    elif key == 'date>=':
        rowID = rangeSearch(data,'9999/12/31',da,cda, True)
        return rowID
    elif key == 'date<=':
        rowID = rangeSearch('0000/00/00',data,da,cda, True)
        return rowID 
    elif key == 'bcc:':
        rowID = rangeSearch('bcc-'+data,'bcc-'+data,em,cem)
        return rowID
    elif key== 'cc:':
        rowID = rangeSearch('cc-'+data,'cc-'+data,em,cem)
        return rowID
    else:
        return 'Could not process query please try again'

def changeDate(date):
        datetime.strptime(str(date), '%Y-%m-%d')


def getText(line,tag):
    # Gets the text obtained between the given tag <tag></tag>
    sTag = '<' + tag +'>'
    eTag = '</' + tag +'>'
    startIndex = line.find(sTag) + len(sTag)
    endIndex = line.find(eTag)  
    text = line[startIndex:endIndex]
    return text  
        

        
def parseUserInput(line):
    #Removes and strips any whitespaces before and after ":"
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

def rangeSearch(start,end,database,curs, partial = False):
    #Gets the rowID from parsed user input
    while(True):
        returnsList=[]
        Starting_Name = str(start).replace('%','')
        Ending_Name = str(end).replace('%','')
        
        #get the record that has the smallest key greater than or equal to the Starting Name:
        result=curs.set_range(Starting_Name.encode("utf-8"))
            
        if(result != None):
            while(result != None):
                #Checking the end condition: If the results comes after sEnding_Name
                if(str(result[0].decode("utf-8")[0:len(Ending_Name)])>Ending_Name): 
                    break
                if partial:
                    returnsList.append(result[1].decode("utf-8"))
                elif partial == False:
                    if re.match(Starting_Name + '$',result[0].decode("utf-8")):
                        returnsList.append(result[1].decode("utf-8"))
                result = curs.next()
                
            return set(returnsList)
        else:
            return set(returnsList)


if __name__ == '__main__':
    main()
