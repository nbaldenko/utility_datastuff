import pandas as pd
import numpy as np

# visualization
import seaborn as sns
import matplotlib.pyplot as plt

# machine learning
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB

raw_data_df = pd.read_csv('/Users/nicolasbaldenko/Documents/Portfolio/Data Science/Utility/Data/fercform1electricutilitydata19942014.csv')

#strip whitespace and parenthesis from column names
raw_data_df.columns = [x.strip().replace(' ', '') for x in raw_data_df.columns]
raw_data_df.columns = [x.strip().replace('(', '') for x in raw_data_df.columns]
raw_data_df.columns = [x.strip().replace(')', '') for x in raw_data_df.columns]

'''
Plan to clean and complete this data

1. Clean the data by checking for anomolies
    A common error would be values reported in kW or kWh sometimes and MW or MWh in other years
    to fix those, we can find the median value of every energy or power column !!!FOR A GIVEN UTILITY!!!
    then compare all the values to that median
    any values >100*median are most likely in Mega instead of Kilo and should be /1000
    any values <100*median are most likely in Kilo instead of Mega and should be *1000
    
    Any other possible errors?
    
2. Complete missing data

    Some companies might have no data for certain fields. Those probably can't be filled
    and I guess we could simply not use those companies if we want to use those fields?
    Or just not use those fields for anything?

'''

#raw_data_df.info()

total_demand_year = raw_data_df.groupby(by=['ReportingYear'])['PeakDemandMW'].sum()

#plot raw data with missing values (total demand by year)
#Determing rolling statistics
rolmean = pd.rolling_mean(total_demand_year, window=5)
rolstd = pd.rolling_std(total_demand_year, window=5)
#Plot rolling statistics:
orig = plt.plot(total_demand_year, color='blue',label='Original')
mean = plt.plot(rolmean, color='red', label='Rolling Mean')
std = plt.plot(rolstd, color='black', label = 'Rolling Std')
plt.legend(loc='best')
plt.title('Rolling Mean & Standard Deviation')
plt.show(block=False)

#this for loop goes through each utility name 
#every Peak Demand field that is empty is filled in with the mean Peak Demand for that company
#If the company has no mean Peak Demand, then it is filled in with the mean for all companies 
#second part is totaly BS not good for model, but it's something. 
#probably better to just not use those companies with no peak demand data.
for i in raw_data_df['UtilityName'].unique():
    
    if np.isnan(raw_data_df.loc[raw_data_df.UtilityName==i,'PeakDemandMW'].mean()):
        raw_data_df.loc[ (raw_data_df.PeakDemandMW.isnull()) & (raw_data_df.UtilityName==i), 'PeakDemandMW' ] = raw_data_df['PeakDemandMW'].mean()
    #else:
    #    raw_data_df.loc[ (raw_data_df.PeakDemandMW.isnull()) & (raw_data_df.UtilityName==i), 'PeakDemandMW' ] = raw_data_df.loc[raw_data_df.UtilityName==i,'PeakDemandMW'].mean()
 
#raw_data_df.plot(x='UtilityName',y='Peak_Demand_MW')


#plot peak demand by year with missing values filled
total_demand_year = raw_data_df.groupby(by=['ReportingYear'])['PeakDemandMW'].sum()
plt.figure()
#Determing rolling statistics
rolmean = pd.rolling_mean(total_demand_year, window=5)
rolstd = pd.rolling_std(total_demand_year, window=5)
#Plot rolling statistics:
orig = plt.plot(total_demand_year, color='blue',label='Original')
mean = plt.plot(rolmean, color='red', label='Rolling Mean')
std = plt.plot(rolstd, color='black', label = 'Rolling Std')
plt.legend(loc='best')
plt.title('Rolling Mean & Standard Deviation')
plt.show(block=False)
  