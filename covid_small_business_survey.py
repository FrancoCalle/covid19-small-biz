import os, sys
import pandas as pd
import numpy as np
import socket
import seaborn as sns

#if statement to identify where's the dropbox with data:
countryTag = 'us'
dataTag = 'raw/survey_responses'
version = '2020-biz-survey-us_March 30, 2020_10.24.csv'

if socket.gethostname() == 'Littlebeast'
    dataPath = "C:/Users/ffalcon/Dropbox/small-biz-2020/data"
else
    dataPath = "C:/Users/ffalcon/Dropbox/small-biz-2020/data"


print("IMPORT DATA ...")
surveyData = pd.read_csv(os.path.join(dataPath,countryTag,dataTag,version))
surveyData = surveyData.loc[3:surveyData.shape[0],:]

#Transform yesno questions:

print("SOME DATA CLEANING ...")
yesnoList= ['Q3.1', 'Q4.1','Q5.1','Q7.1','Q7.2_1','Q7.2_2','Q7.2_3','Q7.2_4','Q8.1']

for var in yesnoList:
    surveyData[var] = surveyData[var].str.lower()
    surveyData['p'+var] = list(map(lambda x: 1 if x == 'yes' else (0 if x == 'no' else np.nan), surveyData[var]))

qCode =  ['Q2.1_1','Q2.1_2',
         'Q3.2_1', 'Q3.2_2',
         'Q4.2_1','Q4.2_2',
         'Q5.2',
         'Q6.1_2']

for var in qCode:
    surveyData['p'+var] = surveyData[var].astype(float)

surveyData = surveyData.dropna(subset=['pQ2.1_1'])
surveyData['totEmp'] = surveyData['pQ2.1_1'] + surveyData['pQ2.1_2']
surveyData['noemp'] = (surveyData['totEmp'] == 0) | (surveyData['totEmp'] > 300)
surveyData  = surveyData.loc[surveyData['noemp'] != True,:] #Eliminate all bussineses without employeess
surveyData['noLayOffFirm'] = (surveyData['pQ3.1'] == 0) & (surveyData['pQ4.1'] == 0)
surveyData['noLayOffFirm'].sum()/surveyData['noLayOffFirm'].shape[0]


print("PLOT FIRST FIGURES ...")

print('Figure 1: Number of Full time employees')
sns.distplot(surveyData['pQ2.1_1'])
ax.set(xlabel='Number of full time employees', ylabel='Density')

print('Figure 2: Number of Part time employees')
sns.distplot(surveyData['pQ2.1_2'])
ax.set(xlabel='Number of part time employees', ylabel='Density')

print('Figure 3: Number of total employees') 
sns.countplot(x = surveyData['totEmp'].astype(int))
ax.set(xlabel='Total Employees', ylabel='Number of Firms')

print('Figure 3: Number of total employees') # MEMO
#ax = sns.countplot(surveyData['totEmp'].astype(int), color='salmon')
ax = sns.distplot(surveyData['totEmp'].astype(int), kde=False, bins=35, color='salmon')
ax.set(xlabel='Total Employees', ylabel='Number of Businesses')

print('Figure: Number of total employees, binned') # MEMO
surveyData['totEmpByGroup'] = list(map(lambda x: '1 employee' if  x == 1 else
                                                ('2 to 5' if 1 < x <= 5 else
                                                ('6 to 10' if 5 < x <= 10 else
                                                ('11 to 30' if 10 < x <= 30 else
                                                ('31 to 50' if 30 < x <= 50 else 'More than 50')))), 
                                                surveyData['totEmp']))

firmSizeCategories= ['1 employee','2 to 5','6 to 10','11 to 30','31 to 50', 'More than 50']
ax = sns.countplot(x = surveyData['totEmpByGroup'], order=firmSizeCategories,color='salmon')
ax.set(xlabel='Size of business', ylabel='Number of businesses')


print('Figure 4: Number of full time employees laid off')
surveyData['pQ3.2_1'] = surveyData['pQ3.2_1'].fillna(0)
# sns.countplot(x = surveyData['pQ3.2_1'])

print('Figure 5: Number of part time employees laid off')
surveyData['pQ3.2_2'] = surveyData['pQ3.2_2'].fillna(0)
# sns.countplot(x = surveyData['pQ3.2_2'])

print('Figure 6: Number of employees laid off')
surveyData['totUnemp'] = surveyData['pQ3.2_1'] + surveyData['pQ3.2_2']
ax = sns.countplot(x =surveyData['totUnemp'].astype(int), color='salmon')
ax.set(xlabel='Total number of people laid off', ylabel='Number of firms')

print('Figue: Number of employees laid off, binned') # MEMO
surveyData['totUnemp'] = surveyData['pQ3.2_1'] + surveyData['pQ3.2_2']
surveyData['totUnempByGroup'] = list(map(lambda x: 'No layoffs' if x == 0 else
                                                ('1 to 5' if 1 <= x <= 5 else
                                                ('6 to 10' if 5 < x <= 10 else
                                                ('11 to 30' if 10 < x <= 30 else
                                                ('31 to 50' if 30 < x <= 50 else 'More than 50')))), 
                                                surveyData['totUnemp']))
ax = sns.countplot(x = surveyData['totUnempByGroup'], 
                   order=['No layoffs', '1 to 5','6 to 10','11 to 30','31 to 50', 'More than 50'],color='salmon')
ax.set(xlabel='Number of people laid off', ylabel='Number of businesses')


print('Figure 7: Unemployment Rate by Business Size')
surveyDataByGroup = surveyData[['totUnemp','totEmp','totEmpByGroup']].groupby(['totEmpByGroup']).sum()
surveyDataByGroup['unemploymentRate'] = surveyDataByGroup['totUnemp']/ surveyDataByGroup['totEmp']

ax = sns.barplot(x = surveyDataByGroup.index, y = surveyDataByGroup['unemploymentRate'], order=firmSizeCategories)
ax.set(xlabel='Firm Size', ylabel='Rate of unemployed')


ax = sns.barplot(x = surveyDataByGroup.index, y = surveyDataByGroup['totUnemp'], order=firmSizeCategories)
ax.set(xlabel='Firm Size', ylabel='Number of unemployed')


print('Figure: Share of employees laid off') # MEMO
surveyData['firm_layoffShare'] = surveyData['totUnemp']/surveyData['totEmp']
ax = sns.distplot(surveyData['firm_layoffShare'], bins=10, kde=False,color='salmon')
ax.set(xlabel='Share of laid off employees', ylabel='Numer of businesses')
# np.median(surveyData['firm_layoffShare']) 
# Median firm in our survey has laid off 2/3 of their employees
# np.mean(surveyData['pQ3,1'])
# 62% of firms in our survey have laid off at least 1 employee


print('Figure: Share of employees laid off, by size of firm') # maybe in memo



print('Figure 8: Share of firms that will not lay off workers')
ax = sns.barplot(x = surveyData['totEmpByGroup'], y = surveyData['noLayOffFirm'], order=firmSizeCategories)
ax.set(xlabel='Firm Size', ylabel='Share of firms that will not lay off workers')


print('Figure: prob of recovery in next two years by size of firm')
surveyData['counter'] = 1
surveyDataByGroup = surveyData[['pQ5.1','counter','totEmpByGroup']].groupby(['totEmpByGroup']).sum()
surveyDataByGroup['optimistRate'] = surveyDataByGroup['pQ5.1']/ surveyDataByGroup['counter']
ax = sns.barplot(x = surveyDataByGroup.index, y = surveyDataByGroup['optimistRate'], 
                 order=firmSizeCategories, color='salmon')
ax.set(xlabel='Firm Size', ylabel='Percentage thinks will recover within 2 years')
# np.mean(surveyData['pQ5.1'])  68.7% think YES recovery in < 2 years


print('Figure: time for recovery (in months)') # Dashboard
#surveyData['Q5.2'] = surveyData['Q5.2'].fillna(0)
#ax = sns.countplot(surveyData['Q5.2'].astype(int), color='salmon')
timeRecovery = surveyData['Q5.2'].copy()
timeRecovery.dropna(inplace=True)
ax = sns.countplot(timeRecovery.astype(int), color='salmon')
ax.set(xlabel='Number of months', ylabel='Number of businesses')

print('Figure: avg time for recovery, by size of firm') # MEMO
ax = sns.barplot(x = surveyData['totEmpByGroup'], 
                 y = surveyData['pQ5.2'], order=firmSizeCategories, color='salmon')
ax.set(xlabel='Size of business', ylabel='Estimated time for recovery (in months)')



print('Figure 9: Probability to file bankruptcy dist') # memo
surveyData['probBankruptcy'] = surveyData['pQ6.1_2']
surveyData['nMonthsCrisis'] = surveyData['pQ5.2']
ax = sns.distplot(surveyData.loc[surveyData['noLayOffFirm']==1,'probBankruptcy'],norm_hist=True, kde=False, label="No Lay Off")
ax = sns.distplot(surveyData.loc[surveyData['noLayOffFirm']==0,'probBankruptcy'],norm_hist=True, kde=False, label="Lay Off")
ax.legend()
ax.set(xlabel='Probability of filing bankruptcy in the next 6 months', ylabel='Density')



print('Figure 10: Average probability to file bankruptcy by firm size')
ax = sns.barplot(x = 'totEmpByGroup', 
                 y = 'probBankruptcy', data = surveyData, 
                 order = firmSizeCategories, color='salmon')
ax.set(xlabel='Size of business', ylabel='Average probability of bankruptcy')



print('Figure: Awareness of government aid')
ax = sns.countplot(surveyData['Q7.1'], color='salmon')
ax = sns.countplot(surveyData['pQ7.1'], color='salmon')
# 67% are aware of some kind of aid 

print('Figure: Awareness Rate by Business Size') # memo 
surveyData['counter'] = 1
surveyDataByGroup = surveyData[['pQ7.1','counter','totEmpByGroup']].groupby(['totEmpByGroup']).sum()
surveyDataByGroup['awarenessRate'] = surveyDataByGroup['pQ7.1']/ surveyDataByGroup['counter']

ax = sns.barplot(x = surveyDataByGroup.index, y = surveyDataByGroup['awarenessRate'], 
                 order=firmSizeCategories, color='salmon')
ax.set(xlabel='Size of business', ylabel='Percentage aware of govt. relief measures')

# Loan, Cover wages, Cover rent, Defer payments (rent, utilities)

np.mean(surveyData['pQ7.2_1']) # 87% know policies for loans
np.mean(surveyData['pQ7.2_2']) # 66% know policies covering wages
np.mean(surveyData['pQ7.2_3']) # 34% know policies covering rent
np.mean(surveyData['pQ7.2_4']) # 45% know about policies to defer payments 



print('Figure: % who know about policy X, conditional on declaring they know something')
data = surveyData[surveyData['pQ7.1']==1].copy()
toplot = data[['pQ7.2_1','pQ7.2_2','pQ7.2_3','pQ7.2_4']].sum()/data['pQ7.1'].sum()

ax = sns.barplot(x = ['Loans','Cover wages','Cover rent','Defer payments'],y = toplot, color='salmon')

