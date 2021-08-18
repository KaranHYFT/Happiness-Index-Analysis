#from pandas import read_csv
import pandas as pd
import xlsxwriter
import numpy as np
# TO Generate Missing data set
import missingNess as MN
# to generate data_scaled file
import minMaxScaling
# to calculate Mean Squared Error
import MSE as mse


zeroMargin=0.000001

# calculate distance 
def calculate_distance(x,y):
    col = len(x)
    dist = 0
    # Columns
    presentCols =  len(x)
     # Total points
    totalPoints =  len(x)
    for i in range(col):
        # if  one of the value is NAN then skip
        if(np.isnan(x[i]) or np.isnan(y[i])):
            presentCols = presentCols-1
            continue
        dist = dist + (x[i]-y[i])**2
    # Distance formula
    dist = dist*totalPoints/presentCols
    return dist**0.5

#Genrerate weights
def make_weights(k,neighbors,distances):
  ans = 0
  for i in range(k):
      # If value is 0 take value as 0.000001
    if(distances[i]==0):
            distances[i]=zeroMargin 
    ans = ans + ((1-distances[i])*neighbors[i])
    
  ans = ans / k
  return ans

# KNN Imputation with k = 5
def knnImputation(data,kValue,fileName,headerList):
    count = 0
    # find the index where value is NaN
    nan_indexes = np.argwhere(np.isnan(data))
    # column nad rows of Excel data
    rows = data.shape[0]
    cols = data.shape[1]
    final_data = data.copy()
    # serach for data with NAN
    for index in nan_indexes:
        count = count + 1
        distances = []
        row = index[0]
        col = index[1]
        x = data[row]
        for i in range(rows):
            # for same row: not calculate the distance 
            isNaN = np.all(np.isnan(data[i]).any())
            if i==row  or isNaN:
                continue
            # calculate distance
            dist = calculate_distance(x,data[i])
            distances.append([dist, data[i][col]])
        # sorting data on basis of distance 
        distances.sort(key=lambda x: x[0])
        distances = np.array(distances)
        # k closest points
        
        neighbors = []
        respectiveDistance =[]
        for i in range(len(distances)):
            # if NAN take next nearest point into consideration
            if(np.isnan(distances[i,1])):
                continue
            neighbors.append(distances[i,1])
            respectiveDistance.append(distances[i,0])
            if(len(neighbors)==kValue):
                break

        # Generate Weights
        missing_value = make_weights(kValue,neighbors,respectiveDistance)
        final_data[row][col] = missing_value

    # Writing final data to Excel sheet
    data_scaled = pd.DataFrame(final_data, columns=headerList)
    data_scaled.to_csv(fileName,index=False)

    return(final_data)
    

# Input and Output file list
InputfileList = ['data.csv','data_scaled.csv']
missingValueFile = ['data-MissingVal.csv','data_scaled-MissingVal.csv']
OutputfileList = ['data-KNN-3-Weighted.csv','data_scaled-KNN-3-Weighted.csv']
dataTOwriteinFile =['data-KNN-3-Weighted-MSE.csv','data_scaled-KNN-3-Weighted-MSE.csv']

# Reading Headers of CSV File
headerList = pd.read_csv('data.csv', header=None)
headerList = headerList.values[0]
# can channge value of k
valueOfK = 3

for i in range (len(InputfileList)):
    # creating Missing Data set
    MN.createMissingDataOfFile(InputfileList[i],missingValueFile[i])
    # Read File
    dataframe = pd.read_csv(missingValueFile[i], header=[0],na_values='?')   
    data = dataframe.values 
    # KNN Impuattion 
    outputforData = knnImputation(data,valueOfK,OutputfileList[i],headerList)

    # find value where NAN is avialable 
    nan_indexes = np.argwhere(np.isnan(data))
    # Mean Squared Error
    mse.meanSquaredError(nan_indexes,InputfileList[i],OutputfileList[i],dataTOwriteinFile[i],headerList) 
