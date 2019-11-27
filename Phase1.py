import time
import string
import re

def main():
    valid = False
    while not valid:
        try:
            dataFile = input("Please enter a data file: ") ##Type records.xml
            file = open(dataFile,'r')
        except IOError:
            print('Invalid file name. Try again.\n')
        else:
            valid = True
    
    terms = open("terms.txt",'a')
    emails = open("emails.txt",'a')
    dates = open("dates.txt",'a')
    records = open("recs.txt",'a')
    
    
    #Starts the timer
    start =time.time()
    line = file.readline()
    while line:
        if line.startswith("<mail>"):
            rowID = getText(line,'row')
            subj = getText(line,'subj')
            body = getText(line,'body')
            from1= getText(line,'from')
            to = getText(line,'to')
            cc = getText(line,'cc')
            bcc = getText(line,'bcc')
            date = getText(line,'date')
            
            termsTxt("s", subj, rowID,terms)
            termsTxt("b", body, rowID,terms)
            emailsTxt("from", from1, rowID,emails)
            emailsTxt("to", to, rowID,emails)
            emailsTxt("cc", cc, rowID,emails)
            emailsTxt("bcc", bcc, rowID,emails)
            dateTxt(date,rowID,dates)
            recsTxt(rowID,line,records)
        line = file.readline()
        
    file.close()
    terms.close()
    emails.close()
    dates.close()
    records.close()
    
    #Stops the timer and prints time
    end=time.time()
    time_interval = end-start
    print("Time Completed: " + str(time_interval))

def replaceSpecial(line):
    # Replaces any special characters used in termsTxt
    line = line.replace('&lt;', '<')
    line = line.replace('&gt;', '>')
    line = line.replace('&amp;', '&')
    line = line.replace('&apos;', "'")
    line = line.replace('&quot;', '"')
    line = line.replace('&#10;', '')
    
    alphanumeric = string.ascii_lowercase + '0123456789' + '-' + ' ' + '_' 
    line = re.sub(r'[^\w\s]',' ',line)
    line = re.sub(r'\b\w{1,2}\b','',line)
    return line
    
def getText(line,tag):
    # Gets the text obtained between the given tag <tag></tag>
    sTag = '<' + tag +'>'
    eTag = '</' + tag +'>'
    startIndex = line.find(sTag) + len(sTag)
    endIndex = line.find(eTag)  
    text = line[startIndex:endIndex]
    return text

#Creates the text files   
def termsTxt(tag,line,rowID,terms):
    line = replaceSpecial(line)
    line = line.split(" ")
    for word in line:
        if len(word) != 0 and len(word)>2:
            terms.write(tag + "-"+  word.lower() + ":" + rowID + "\n")

def emailsTxt(fld,em,rowID,emails):
    em = em.split(",")
    for e in em:
        if len(e) != 0:
            emails.write(fld + "-"+  e.lower() + ":" + rowID + "\n")

def dateTxt(da,rowID,dates):
    if len(da) != 0:
        dates.write(da + ":" + rowID +"\n")


def recsTxt(rowID,rec,records):
    if len(rec) != 0:
        records.write(rowID + ":" + rec +"\n")
    
if __name__ == '__main__':
    main()
