from bsddb3 import db
import subprocess

def main():
    quit = False
    outputFull = False
    getSubject()
    
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
        
def rangeSearch(start, end):
    idxLst = []
    result = curs.set_range(start.encode("utf-8"))
    while(result != None):
        #Checking the end condition: If the student's name comes after(or equal to) Ending_Name
        if(str(result[0].decode("utf-8")[0:len(Ending_Name)])>=Ending_Name): 
            break
            
        print("Name: " + str(result[0].decode("utf-8")) + ", Mark: " + str(result[1].decode("utf-8")))
        idxList.append(result[0])
        result = curs.next()
        
def getSubject():
    database = db.DB()
    curs = database.cursor()
    database.open(idx)         
    subStart = input("Enter Start Subject")
    subEnd = input("Enter End Subject, enter nothing for no end")
    idxLst = rangeSearch(subStart, subEnd)
    print(idxLst)
    #valueLst = fileGet(idxLst)
    curs.close()
    database.close()


if __name__ == '__main__':
    main()
