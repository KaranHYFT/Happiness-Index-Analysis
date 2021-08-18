import random 
import pandas as pd
#to create missingnesss of data and store it to another file of 50 % data

# fromFile : to read data from , toStoreinFile : File name in which missing data will be stored
def createMissingDataOfFile(fromFile,toStoreinFile):
    
    dataframe = pd.read_csv(fromFile, header=[0])
    data = dataframe.values
    #Read Header
    headerList = pd.read_csv(fromFile, header=None)
    headerList = headerList.values[0]

    # NO of rows to be selected, 50% of total tows
    lengthOfData = int (len(data)/2)
    start = 0
    end = len(data)
    #  selecting random Rows between 1 to No of rows, without repetation
    randomRows =[]
    randomRows = giveRandomList(start,end-1,lengthOfData)
    
    # generating random No list for columns, selecting 50 % of selected 50 % data
    columns = len(data[0])   
    columnsnRandomList =[] 
    for i in range (columns):
        columnsnRandomList.append(randomNoFromList(randomRows,int(lengthOfData/2)))
        #columnsnRandomList.append(giveRandomList(start,int(end/2),int(lengthOfData/2)))
    data = data.tolist()
    # filling ? to  data of Excel sheet, from above result of randomcols and randomRows result
    for col in range (columns):
        for row in range (int(len(data)/4)):
            data[columnsnRandomList[col][row]][col] =  "?"


    # write data to Excel with Missing values
    data_scaled = pd.DataFrame(data, columns=headerList)
    data_scaled.to_csv(toStoreinFile,index=False)

# Generating random list
def giveRandomList(start,end,randNoLength):  
    count = 0
    randomList = []
    while(count!=randNoLength): 
        randomNo = random.randint(start, end)
        if randomNo not in randomList:
            randomList.append(randomNo) 
            count = count + 1
    return randomList

# It gives random list from Given dataset eithout repetation
def randomNoFromList(datset,totalNo):
    count = 0
    randomList = []
    while(count!=totalNo): 
        randomNo  = random.choice(datset) 
        if randomNo not in randomList:
            randomList.append(randomNo) 
            count = count + 1
    return randomList
print("Called MissingNess")
#createMissingDataOfFile("data.csv","dummyData.csv")