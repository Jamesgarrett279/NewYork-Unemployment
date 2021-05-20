#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Author: James Carter Garrett

# Necessary libraries
import json
from urllib.request import urlopen
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display

# Displays the most up-to-date unemploynment rate for New York
def ny_current_status():
    # API for New York's Unemployment Information from bls.gov
    nyRequest = urlopen("https://api.bls.gov/publicAPI/v1/timeseries/data/LASST360000000000003")
    nyObject = json.loads(nyRequest.read())
    
    # Checks to see if the request is denied
    if nyObject['status'] == "REQUEST_NOT_PROCESSED":
        print(nyObject['message'])
        return

    # This is the data from the api
    nyData = nyObject['Results']['series'][0]['data']
    
    print("API INFO FROM: api.bls.gov")
    print("Series ID:", nyObject['Results']['series'][0]['seriesID'])
    print("------------------------------")
    print("New York's Current Unemployment Rate:", nyData[0]['value'], " | Update from", nyData[0]['periodName'],
         nyData[0]['year'])
    print("------------------------------")
    print()

    return

def ny_unemployment_showcase():
    # Checks to make sure the file is found
    try:
        overallDataframe = pd.read_csv("NY1976-2020.csv")
    except Exception as ex:
        print(ex)
        return
    
    # Checks to make sure the second file is found
    try:
        twoYearDF = pd.read_csv("NY2019-2020.csv")
    except Exception as ex:
        print(ex)
        return
    
    # Sets the index to the year and replaces "NaN" with 0
    overallDataframe.set_index('Year', inplace = True)
    twoYearDF.set_index('Year', inplace = True)
    
    overallDataframe.fillna(0, inplace = True)
    twoYearDF.fillna(0, inplace = True)
    
    # Checks input to see if they want to see the monthly UI rate
    keepRunning = True
    while keepRunning == True:
        userInput = input("Would you like to see the monthly UI rate pandas for 1976-2020? (yes/no): ")
        
        if userInput.lower() == 'yes':
            display(overallDataframe)
            keepRunning = False
        
        elif userInput.lower() == 'no':
            keepRunning = False
        
        else:
            print("Invalid input, try again.")
    
    # Get the average unemployment for each year and create a pandas from it
    meanDict = {}
    
    for year, months in overallDataframe.iterrows():
        monthSum = 0
        for value in months:
            monthSum += value
        
        # If the year is 2020, we divide by 10 since we only have data up to October
        if year == 2020:
            average = monthSum / 10
            meanDict[year] = round(average, 1)
        
        else:
            average = monthSum / 12
            meanDict[year] = round(average, 1)
    
    overallAverageDF = pd.DataFrame.from_dict(meanDict, orient='index', columns=['Percentage'])
    
    # Checks input to see if they want to see the yearly average UI rate pandas
    keepRunning = True
    while keepRunning == True:
        userInput = input("Would you like to see the yearly average UI rate pandas for 1976-2020? (yes/no): ")
        
        if userInput.lower() == 'yes':
            display(overallAverageDF)
            keepRunning = False
        
        elif userInput.lower() == 'no':
            keepRunning = False
        
        else:
            print("Invalid input, try again.")    
    
    # Chart for 1976-2020
    overallChart = plt.figure(figsize=(15,6), dpi = 200)
    overallAxes = overallChart.add_axes([0.1, 0.2, 0.8, 0.9])
    overallAxes.set_xlabel("Years from 1976 to 2020")
    overallAxes.set_ylabel("Unemployment Rate (yearly average, in percent)")
    overallAxes.set_title("New York's Unemployment Rate from 1976 to 2020")
    
    # Add the years to the plot
    for year, percent in overallAverageDF.iterrows():      
        valueBar = overallAxes.bar(year, percent[0], width = 0.5)
        
        # This adds the percentage above the bar
        concatText = str(str(percent[0]) + "%")
        overallAxes.text(year, percent + 0.2, concatText, horizontalalignment = 'center')
    
    # Chart for 2019-2020
    twoYearChart = plt.figure(figsize=(12,6), dpi = 100)
    twoYearAxes = twoYearChart.add_axes([0.1, 0.2, 0.8, 0.9])
    monthTicks = ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    monthLabels = (['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    
    twoYearAxes.set_xticks(monthTicks)
    twoYearAxes.set_xticklabels(monthLabels)
    twoYearAxes.set_xlabel("Months in a Year")
    twoYearAxes.set_ylabel("Unemployment Rate (in percent)")
    twoYearAxes.set_title("New York's Unemployment Rate: 2019 v.s. 2020")
    
    # Change the dataframe to descending order
    twoYearDF = twoYearDF.sort_values('Year', ascending = False)
    
    # Checks input to see if they want to see 2019-2020 UI pandas
    keepRunning = True
    while keepRunning == True:
        userInput = input("Would you like to see the 2019-2020 UI rate pandas? (yes/no): ")
        
        if userInput.lower() == 'yes':
            display(twoYearDF)
            keepRunning = False
        
        elif userInput.lower() == 'no':
            keepRunning = False
        
        else:
            print("Invalid input, try again.")  
    
    # A list to hold 2020's percentages to add to the label over the bar
    percentList = []
    
    # Adding each year to the chart
    for year, months in twoYearDF.iterrows():
        if year == 2019:
            for month in range(len(months)):
                # Sets a label for the legend to the final month
                if month == 11:
                    valueBar = twoYearAxes.bar(month, months[month], color = 'blue', label = '2019')
                else:
                    valueBar = twoYearAxes.bar(month, months[month], color = 'blue')
                
                # Adds the percents over the bar, seperated by a line: |
                percent2019 = str("2019: " + str(months[month]) + "%")
                percent2020 = str("2020: " + str(percentList[month]) + "%")
                percentLabel = str(percent2019 + " | " + percent2020)
                
                twoYearAxes.text(month, months[month] + 0.4, percentLabel, horizontalalignment = 'center', 
                                rotation=90)                
        else:
            for month in range(len(months)):
                # Sets a label for the legend to the final month
                if month == 11:
                    valueBar = twoYearAxes.bar(month, months[month], color = 'red', label = '2020')
                else:
                    valueBar = twoYearAxes.bar(month, months[month], color = 'red')
                    
                percentList.append(months[month])
    
    # Add legend to the chart
    twoYearAxes.legend()

# ------Call this function------
def ny_main():
    ny_current_status()
    ny_unemployment_showcase()

ny_main()

