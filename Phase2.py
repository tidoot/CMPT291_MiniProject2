from bsddb3 import db
import subprocess

def main():
    sortFiles()
    parseFiles()
    
    #Creates the database
    loadDB('recs.txt','re.idx','hash')
    loadDB('terms.txt','te.idx','btree')
    loadDB('emails.txt','em.idx','btree')
    loadDB('dates.txt','da.idx','btree')
    
    #After database is made, it can be converted to txt form to check:
    #check('re.idx','rtest.txt')
    #check('te.idx','ttest.txt')
    #check('em.idx','etest.txt')
    #check('da.idx','dtest.txt')
    

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
    
    #Changed the txt files to lines of alternating key and data pairs
    reformat(termsKeyList,termsDataList,'terms.txt')
    reformat(emailsKeyList,emailsDataList,'emails.txt')
    reformat(datesKeyList,datesDataList,'dates.txt')
    reformat(recsKeyList,recsDataList,'recs.txt')

def parseFile(file):
    f = open(file,'r')
    dataList = []
    keyList = []
    lines = f.read().splitlines()
    for line in lines:
        key,data = line.split(':', 1) #split at first occurance of semicolon only, applicable for recs
        key = key.replace('\\','') #remove backslash
        data = data.replace('\\','')
        dataList.append(data)
        keyList.append(key)
    f.close()
    return dataList, keyList


def reformat(list1,list2,name):
    f = open(name,'w')
    index=0
    for i in range(len(list1)):
        f.write(list1[index]+'\n'+list2[index]+'\n')
        index+=1
    f.close()


#[-c name=value]: allows adding of duplicate key/value pair
#[-T] : allows for txt to db?
#[-t type]: gives db type(hash/btree)
#[-f file]: use file to make db
def loadDB(fileInput,fileOutput,indexType):
    subprocess.call(['db_load', '-c','duplicates=1','-T', '-t', indexType, '-f', fileInput, fileOutput]) 


# Turns .idx file to .txt for checking
def check(fileInput,fileOutput):
    subprocess.call(['db_dump','-p','-f',fileOutput,fileInput]) 


if __name__ == '__main__':
    main()