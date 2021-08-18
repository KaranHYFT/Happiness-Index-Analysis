import pandas as pd
import numpy as np

def meanSquaredError(nan_indexes,originalFile,predictedFile,fileToWrite,headerList):

    # Read original file for MSE Calcuation
    originDataframe = pd.read_csv(originalFile, header=[0],na_values='?')
    originData = originDataframe.values
    
    # Read Predicted file for MSE Calcuation
    predictedDataframe = pd.read_csv(predictedFile, header=[0],na_values='?')
    predictedData = predictedDataframe.values
    
    lst = []
    countData = [] 
    finalData = []
    for i in range(len(headerList)):
        lst.append(0)
        countData.append(0)
    # calculating MSE from 2 files for same  cells of Excel
    for index in nan_indexes:
        row = index[0]
        col = index[1]
        lst[col] = lst[col] + pow((originData[row,col] - predictedData[row,col]),2)
        countData[col] = countData[col] + 1
    # Dividing data  with Number of data
    MSE = [i / j for i, j in zip(lst, countData)]
    finalMSE =[]
    finalMSE.append(MSE)
    
    # Wriring MSE value for each column in respective csv file
    dataToWrite = pd.DataFrame(np.array(finalMSE), columns=headerList)
    dataToWrite.to_csv(fileToWrite,index=False)