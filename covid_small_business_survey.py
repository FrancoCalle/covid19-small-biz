import os, sys
import pandas as pd
import numpy as np
import socket
import seaborn as sns

#if statement to identify where's the dropbox with data:
countryTag = 'us'
dataTag = 'raw/survey_responses'

if socket.gethostname() == 'Littlebeast'
    dataPath = "C:/Users/ffalcon/Dropbox/small-biz-2020/data"
else
    dataPath = "C:/Users/ffalcon/Dropbox/small-biz-2020/data"


print("IMPORT DATA ...")
surveyData = pd.read_csv(os.path.join(dataPath,countryTag,dataTag,'2020-biz-survey-us_March 29, 2020_19.36.csv'))
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

surveyData['totEmpByGroup'] = list(map(lambda x: 'Independent' if  x == 1 else
                                                (']2 5]' if 1 < x <= 5 else
                                                (']5 10]' if 5 < x <= 10 else
                                                (']10 30]' if 10 < x <= 30 else
                                                (']30 50]' if 30 < x <= 50 else '> 50')))), surveyData['totEmp']))

firmSizeCategories= ['Independent',']2 5]',']5 10]',']10 30]',']30 50]', '> 50']
ax = sns.countplot(x = surveyData['totEmpByGroup'], order=firmSizeCategories)
ax.set(xlabel='Firm Size', ylabel='Number of firms')


print('Figure 4: Number of full time employees laid off')
surveyData['pQ3.2_1'] = surveyData['pQ3.2_1'].fillna(0)
# sns.countplot(x = surveyData['pQ3.2_1'])

print('Figure 5: Number of part time employees laid off')
surveyData['pQ3.2_2'] = surveyData['pQ3.2_2'].fillna(0)
# sns.countplot(x = surveyData['pQ3.2_2'])

print('Figure 6: Number of employees laid off')
surveyData['totUnemp'] = surveyData['pQ3.2_1'] + surveyData['pQ3.2_2']
sns.countplot(x =surveyData['totUnemp'].astype(int))
ax.set(xlabel='Total number of people laid off', ylabel='Number of firms')

surveyData['totUnempByGroup'] = list(map(lambda x: 'No unemp' if x == 0 else
                                                ('[1 5]' if 1 <= x <= 5 else
                                                (']5 10]' if 5 < x <= 10 else
                                                (']10 30]' if 10 < x <= 30 else
                                                (']30 50]' if 30 < x <= 50 else '> 50')))), surveyData['totUnemp']))

ax = sns.countplot(x = surveyData['totUnempByGroup'], order=['No unemp', '[1 5]',']5 10]',']10 30]',']30 50]', '> 50'])
ax.set(xlabel='Number of people unemployed', ylabel='Number of firms')


print('Figure 7: Unemployment Rate by Business Size')
surveyDataByGroup = surveyData[['totUnemp','totEmp','totEmpByGroup']].groupby(['totEmpByGroup']).sum()
surveyDataByGroup['unemploymentRate'] = surveyDataByGroup['totUnemp']/ surveyDataByGroup['totEmp']

ax = sns.barplot(x = surveyDataByGroup.index, y = surveyDataByGroup['unemploymentRate'], order=firmSizeCategories)
ax.set(xlabel='Firm Size', ylabel='Rate of unemployed')


ax = sns.barplot(x = surveyDataByGroup.index, y = surveyDataByGroup['totUnemp'], order=firmSizeCategories)
ax.set(xlabel='Firm Size', ylabel='Number of unemployed')


print('Figure 8: Share of firms that will not lay off workers')
ax = sns.barplot(x = surveyData['totEmpByGroup'], y = surveyData['noLayOffFirm'], order=firmSizeCategories)
ax.set(xlabel='Firm Size', ylabel='Share of firms that will not lay off workers')


print('Figure 9: Probability to file bankruptcy dist')
surveyData['probBankruptcy'] = surveyData['pQ6.1_2']
surveyData['nMonthsCrisis'] = surveyData['pQ5.2']
ax = sns.distplot(surveyData.loc[surveyData['noLayOffFirm']==1,'probBankruptcy'],norm_hist=True, kde=False, label="No Lay Off")
ax = sns.distplot(surveyData.loc[surveyData['noLayOffFirm']==0,'probBankruptcy'],norm_hist=True, kde=False, label="Lay Off")
ax.legend()
ax.set(xlabel='Probability to file bankruptcy', ylabel='Density')



print('Figure 10: Probability to file bankruptcy by firm size')
ax = sns.barplot(x = 'totUnempByGroup', y = 'probBankruptcy', data = surveyData, order = ['[1 5]',']5 10]',']10 30]',']30 50]', '> 50'])
ax.set(xlabel='Firm Size', ylabel='Average probability of bankruptcy')
