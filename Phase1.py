import time
import string

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

    #Starts the timer
    start =time.time()
    strings = file.read().splitlines()
    file.close()

    # Main for loop that gets the text information and writes to files
    for line in strings:
        if line.startswith("<mail>"):
            rowID = getText(line,'row')
            subj = getText(line,'subj')
            body = getText(line,'body')
            from1= getText(line,'from')
            to = getText(line,'to')
            cc = getText(line,'cc')
            bcc = getText(line,'bcc')
            date = getText(line,'date')
            
            termsTxt("s", subj, rowID)
            termsTxt("b", body, rowID)
            emailsTxt("from", from1, rowID)
            emailsTxt("to", to, rowID)
            dateTxt(date,rowID)
            recsTxt(rowID,line)
    
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
    for letter in line:
        if letter.lower() not in alphanumeric:
            line = line.replace(letter, ' ')
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
def termsTxt(tag,line,rowID):
    line = replaceSpecial(line)
    terms = open("terms.txt",'a')
    line = line.split(" ")
    for word in line:
        if len(word) != 0 and len(word)>2:
            terms.write(tag + "-"+  word.lower() + ":" + rowID + "\n")
    terms.close()


def emailsTxt(fld,email,rowID):
    emails = open("emails.txt",'a')
    email = email.split(",")
    for e in email:
        if len(e) != 0:
            emails.write(fld + "-"+  e.lower() + ":" + rowID + "\n")
    emails.close()


def dateTxt(date,rowID):
    dates = open("dates.txt",'a')
    if len(date) != 0:
        dates.write(date + ":" + rowID +"\n")
    dates.close()

def recsTxt(rowID,rec):
    recs = open("recs.txt",'a')
    if len(rec) != 0:
        recs.write(rowID + ":" + rec +"\n")
    recs.close()    

    
if __name__ == '__main__':
    main()