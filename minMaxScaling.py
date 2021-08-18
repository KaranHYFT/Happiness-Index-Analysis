#from pandas import read_csv
import pandas as pd
import numpy as np
import xlsxwriter

#change value of newMax and newMin for scaling,  it will scale data between 0 to 1
newMin = 0
newMax = 1

def find_minMax(dataset):
	minmaxList = list()
	for i in range(len(dataset[0])):
		col_values = [row[i] for row in dataset]
        #finding min and max and appending to list
		minVal = min(col_values)
		maxVal = max(col_values)
		minmaxList.append([minVal, maxVal])
	return minmaxList
 
#noramlizing data set
def normalization(dataset, minmax):
	for row in dataset:
		for i in range(len(row)):
            # by chaging value of newMin and newMin, we can scale data in particular range
			row[i] = round((row[i] - minmax[i][0]) / (minmax[i][1] - minmax[i][0]) * (newMax - newMin) + newMin,6)

#load file and read data, except first row (header)
fileName = 'data.csv'
dataframe = pd.read_csv(fileName, header=[0])
data = dataframe.values
#Read Header
headerList = pd.read_csv(fileName, header=None)
headerList = headerList.values[0]

#No of colunmns and rows
col = data.shape[1]
row = data.shape[0]
# Calculate min and max for each column
minmax = find_minMax(data)
#scaling data
normalization(data, minmax)

data_scaled = pd.DataFrame(data, columns=headerList)
data_scaled.to_csv('data_scaled.csv',index=False)

print("called minmax")
