import pandas as pd
import numpy as np
import decimal
# TO Generate Missing data set
import missingNess as MN
# to generate data_scaled file
import minMaxScaling
# to calculate Mean Squared Error
import MSE as mse


def meanImputation(data,fileName,headerList):

    rows = data.shape[0]
    cols = data.shape[1]
    dataTobeProceessed = data.copy()
    # transpose data 
    transposedData = dataTobeProceessed.transpose()
    finalSumList = []
    countlst =[]
    # finding data without NAN Value
    for i in range (len(transposedData)):
        total= 0
        count = 0
        for j in range (len(transposedData[0])):
            if np.isnan(transposedData[i][j])==False:
                total= total+ transposedData[i][j]
                count = count + 1
        finalSumList.append(float(total))
        countlst.append(float(count))    
    meanVal = [i / j for i, j in zip(finalSumList, countlst)] 
    
    # Find indexes where NAN present
    inds = np.where(np.isnan(data)) 
    final_data = data.copy()
    final_data[inds] = np.take(meanVal, inds[1]) 
    
    data_toPrint = pd.DataFrame(final_data, columns=headerList)
    data_toPrint.to_csv(fileName,index=False)



# Input and Output file list
InputfileList = ['data.csv','data_scaled.csv']
missingValueFile = ['data-MissingVal.csv','data_scaled-MissingVal.csv']
OutputfileList = ['data-mean.csv','data_scaled-mean.csv']
dataTOwriteinFile =['data-mean-MSE.csv','data_scaled-mean-MSE.csv']

# Reading Headers of CSV File
headerList = pd.read_csv('data.csv', header=None)
headerList = headerList.values[0]
valueOfK = 5

for i in range (len(InputfileList)):
    # creating Missing Data set
    MN.createMissingDataOfFile(InputfileList[i],missingValueFile[i])
    # Read File
    dataframe = pd.read_csv(missingValueFile[i], header=[0],na_values='?')   
    data = dataframe.values 
    # mean Impuattion 
    outputforData = meanImputation(data,OutputfileList[i],headerList)
    
        # find value where NAN is avialable 
    nan_indexes = np.argwhere(np.isnan(data))
    # Mean Squared Error
    mse.meanSquaredError(nan_indexes,InputfileList[i],OutputfileList[i],dataTOwriteinFile[i],headerList)
