import os, sys
import pandas as pd
import numpy as np
import seaborn as sns
from small_biz.data_getter import get_surv_data

#1. Import data
print("IMPORT DATA ...")

countrySample = 'latam'
lang = 'spanish'
surveyData = get_surv_data(countrySample)

#%%
print("SOME DATA CLEANING ...")
yesnoList= ['q3.1', 'q4.1','q5.1','q7.1','q7.2_1','q7.2_2','q7.2_3','q7.2_4','q8.1']

for var in yesnoList:
    surveyData[var] = surveyData[var].str.lower()
    surveyData['p'+var] = list(map(lambda x: 1 if (x == 'yes' or x == 'si') else (0 if x == 'no' else np.nan), surveyData[var]))

qCode =  ['q2.1_1','q2.1_2',
         'q3.2_1', 'q3.2_2',
         'q4.2_1','q4.2_2',
         'q5.2',
         'q6.1_2']

for var in qCode:
    surveyData['p'+var] = surveyData[var].astype(float)

surveyData = surveyData.dropna(subset=['pq2.1_1'])
surveyData['totEmp'] = surveyData['pq2.1_1'] + surveyData['pq2.1_2']

# Don't drop them for now 
# surveyData['noemp'] = (surveyData['totEmp'] == 0) | (surveyData['totEmp'] > 300)
# surveyData  = surveyData.loc[surveyData['noemp'] != True,:] #Eliminate all bussineses without employeess

surveyData['noLayOffFirm'] = (surveyData['pq3.1'] == 0) & (surveyData['pq4.1'] == 0)
surveyData['noLayOffFirm'].sum()/surveyData['noLayOffFirm'].shape[0]

#%%
print("PLOT MEMO FIGURES ...")

#%% Number of employees

print('Figure 3: Number of total employees') # MEMO

if lang == 'english':
    ax = sns.distplot(surveyData['totEmp'].astype(int), 
                      kde=False, bins=35, color='salmon')
    ax.set(xlabel='Total Employees', ylabel='Number of Businesses')
elif lang == 'spanish':
    ax = sns.distplot(surveyData['totEmp'].astype(int), 
                      kde=False, bins=35, color='salmon')
    ax.set(xlabel='Empleados', ylabel='Numero de empresas')


print('Figure: Number of total employees, binned') # MEMO

if lang == 'english':
    surveyData['totEmpByGroup'] = list(map(lambda x: '0 employees' if  x == 0 else
                                                ('1 to 5' if 1 <= x <= 5 else
                                                ('6 to 10' if 5 < x <= 10 else
                                                ('11 to 30' if 10 < x <= 30 else
                                                ('31 to 50' if 30 < x <= 50 else 'More than 50')))),
                                                surveyData['totEmp']))
    firmSizeCategories= ['0 employees','1 to 5','6 to 10','11 to 30','31 to 50', 'More than 50']
    ax = sns.countplot(x = surveyData['totEmpByGroup'], order=firmSizeCategories,color='salmon')
    ax.set(xlabel='Size of business', ylabel='Number of businesses')
    
elif lang == 'spanish':
    surveyData['totEmpByGroup'] = list(map(lambda x: '0 empleados' if  x == 0 else
                                                ('1 a 5' if 1 <= x <= 5 else
                                                ('6 a 10' if 5 < x <= 10 else
                                                ('11 a 30' if 10 < x <= 30 else
                                                ('31 a 50' if 30 < x <= 50 else 'Más de 50')))),
                                                surveyData['totEmp']))
    firmSizeCategories= ['0 empleados','1 a 5','6 a 10','11 a 30','31 a 50', 'Más de 50']
    ax = sns.countplot(x = surveyData['totEmpByGroup'], order=firmSizeCategories,color='salmon')
    ax.set(xlabel='Tamaño de empresa', ylabel='Número de empresas')
    
    
    
    
#%% Lay offs 

print('Figure: Number of full time employees laid off, by size of business') # MEMO

if lang == 'english':
    ax = sns.barplot(x = surveyData['totEmpByGroup'],
                 y = surveyData['pq3.2_1'], order=firmSizeCategories, color='salmon')
    ax.set(xlabel='Size of business', ylabel='Number of full-time employees laid off')

elif lang == 'spanish':
    ax = sns.barplot(x = surveyData['totEmpByGroup'],
                 y = surveyData['pq3.2_1'], order=firmSizeCategories, color='salmon')
    ax.set(xlabel='Tamaño de empresa', ylabel='Número de despidos de empleados a tiempo completo')



print('Figure: Number of part time employees laid off, by size of business') # MEMO

if lang == 'english':
    ax = sns.barplot(x = surveyData['totEmpByGroup'],
                 y = surveyData['pq3.2_2'], order=firmSizeCategories, color='salmon')
    ax.set(xlabel='Size of business', ylabel='Number of part-time employees laid off')

elif lang == 'spanish':
    ax = sns.barplot(x = surveyData['totEmpByGroup'],
                 y = surveyData['pq3.2_2'], order=firmSizeCategories, color='salmon')
    ax.set(xlabel='Tamaño de empresa', ylabel='Número de despidos de empleados a tiempo parcial')


# Firms without employees?
surveyData[surveyData['totEmp']==0] 
# & surveyData['q1.3'] == 'República Dominicana'] 
# 243  


#%%
surveyData['noemp'] = (surveyData['totEmp'] == 0) 
surveyData  = surveyData.loc[surveyData['noemp'] != True,:] #Eliminate all bussineses without employeess


print('Figure: Number of employees laid off, binned') # MEMO

surveyData['pq3.2_1'] = surveyData['pq3.2_1'].fillna(0)
surveyData['pq3.2_2'] = surveyData['pq3.2_2'].fillna(0)
surveyData['totUnemp'] = surveyData['pq3.2_1'] + surveyData['pq3.2_2']

if lang == 'english':
    surveyData['totUnempByGroup'] = list(map(lambda x: 'No layoffs' if x == 0 else
                                                ('1 to 5' if 1 <= x <= 5 else
                                                ('6 to 10' if 5 < x <= 10 else
                                                ('11 to 30' if 10 < x <= 30 else
                                                ('31 to 50' if 30 < x <= 50 else 'More than 50')))),
                                                surveyData['totUnemp']))
    ax = sns.countplot(x = surveyData['totUnempByGroup'],
                   order=['No layoffs', '1 to 5','6 to 10','11 to 30','31 to 50', 'More than 50'],color='salmon')
    ax.set(xlabel='Number of people laid off', ylabel='Number of businesses')

elif lang == 'spanish': # skipping for now for latam
    surveyData['totUnempByGroup'] = list(map(lambda x: 'Ningún despido' if x == 0 else
                                                ('1 a 5' if 1 <= x <= 5 else
                                                ('6 a 10' if 5 < x <= 10 else
                                                ('11 a 30' if 10 < x <= 30 else
                                                ('31 a 50' if 30 < x <= 50 else 'Más de 50')))),
                                                surveyData['totUnemp']))
    ax = sns.countplot(x = surveyData['totUnempByGroup'],
                   order=['Ningún despido', '1 a 5','6 a 10','11 a 30','31 a 50', 'Más de 50'],color='salmon')
    ax.set(xlabel='Número de despidos', ylabel='Número de empresas')
    

print('Figure: Share of employees laid off') # MEMO

if lang == 'english':
    surveyData['firm_layoffShare'] = surveyData['totUnemp']/surveyData['totEmp']
    ax = sns.distplot(surveyData['firm_layoffShare'], bins=10, kde=False,color='salmon')
    ax.set(xlabel='Share of laid off employees', ylabel='Numer of businesses')

elif lang == 'spanish':
    surveyData['firm_layoffShare'] = surveyData['totUnemp']/surveyData['totEmp']
    ax = sns.distplot(surveyData['firm_layoffShare'], bins=10, kde=False,color='salmon')
    ax.set(xlabel='Fracción de empleados despedidos', ylabel='Número de empresas')

# np.median(surveyData['firm_layoffShare'])
# Median firm in our survey has laid off 2/3 of their employees
# np.mean(surveyData['pq3,1'])
# 62% of firms in our survey have laid off at least 1 employee

#%%

print('Figure: Number of employees laid off, by size of business') # MEMO

if lang == 'english':
    ax = sns.barplot(x = surveyData['totEmpByGroup'],
                 y = surveyData['totUnemp'], order=firmSizeCategories, color='salmon')
    ax.set(xlabel='Size of business', ylabel='Total employees laid off')

elif lang == 'spanish':
    ax = sns.barplot(x = surveyData['totEmpByGroup'],
                 y = surveyData['totUnemp'], order=firmSizeCategories, color='salmon')
    ax.set(xlabel='Tamaño de empresa', ylabel='Total despidos (tiempo completo + tiempo parcial)')


print('Figure: Number of prospective layoffs, by size of business') # MEMO

surveyData['pq4.2_1'] = surveyData['pq4.2_1'].fillna(0)
surveyData['pq4.2_2'] = surveyData['pq4.2_2'].fillna(0)
    
if lang == 'english':
    surveyData['totMoreLayoffs'] = surveyData['pq4.2_1'] + surveyData['pq4.2_2']
    ax = sns.barplot(x = surveyData['totEmpByGroup'],
                 y = surveyData['totMoreLayoffs'], order=firmSizeCategories, color='salmon')
    ax.set(xlabel='Size of business', ylabel='Estimated additional layoffs')
    
elif lang == 'spanish':
    surveyData['totMoreLayoffs'] = surveyData['pq4.2_1'] + surveyData['pq4.2_2']
    ax = sns.barplot(x = surveyData['totEmpByGroup'],
                 y = surveyData['totMoreLayoffs'], order=firmSizeCategories, color='salmon')
    ax.set(xlabel='Tamaño de empresa', ylabel='Despidos adicionles estimados')
    

#%% Expectations: Recovery, Bankruptcy

print('Figure: time for recovery (in months)') # MEMO and Dashboard
#surveyData['q5.2'] = surveyData['q5.2'].fillna(0)
#ax = sns.countplot(surveyData['q5.2'].astype(int), color='salmon')

if lang == 'english':
    timeRecovery = surveyData['q5.2'].copy()
    timeRecovery.dropna(inplace=True)
    ax = sns.countplot(timeRecovery.astype(int), color='salmon')
    ax.set(xlabel='Estimated time for recovery (in months)', ylabel='Number of businesses')

elif lang == 'spanish':
    timeRecovery = surveyData['q5.2'].copy()
    timeRecovery.dropna(inplace=True)
    ax = sns.countplot(timeRecovery.astype(int), color='salmon')
    ax.set(xlabel='Tiempo estimado de recuperación (meses)', ylabel='Número de empresas')
    


print('Figure: avg time for recovery, by size of firm') # MEMO

if lang == 'english':
    ax = sns.barplot(x = surveyData['totEmpByGroup'],
                 y = surveyData['pq5.2'], order=firmSizeCategories, color='salmon')
    ax.set(xlabel='Size of business', ylabel='Estimated time for recovery (in months)')

elif lang == 'spanish':
    ax = sns.barplot(x = surveyData['totEmpByGroup'],
                 y = surveyData['pq5.2'], order=firmSizeCategories, color='salmon')
    ax.set(xlabel='Tamaño de empresa', ylabel='Tiempo estimado de recuperación (meses)')



print('Figure 9: Probability to file bankruptcy dist') # memo
surveyData['probBankruptcy'] = surveyData['pq6.1_2']
surveyData['nMonthsCrisis'] = surveyData['pq5.2']
ax = sns.distplot(surveyData.loc[surveyData['noLayOffFirm']==1,'probBankruptcy'],norm_hist=True, kde=False, label="No Lay Off")
ax = sns.distplot(surveyData.loc[surveyData['noLayOffFirm']==0,'probBankruptcy'],norm_hist=True, kde=False, label="Lay Off")
ax.legend()
ax.set(xlabel='Probability of filing bankruptcy in the next 6 months', ylabel='Density')


print('Figure: Probability of bankruptcy')

if lang == 'english':
    ax = sns.distplot(surveyData['pq6.1_2'], kde=False, color='salmon')
    ax.set(xlabel='Probability of filing for bankruptcy in the next 6 months', ylabel='Number of businesses')
elif lang == 'spanish':
    ax = sns.distplot(surveyData['pq6.1_2'], kde=False, color='salmon')
    ax.set(xlabel='Probabilidad de quebrar en los próximos 6 meses', ylabel='Número de empresas')


#%% Awareness of different programs

print('Figure: Awareness Rate by Business Size') # memo

surveyData['counter'] = 1
surveyDataByGroup = surveyData[['pq7.1','counter','totEmpByGroup']].groupby(['totEmpByGroup']).sum()
surveyDataByGroup['awarenessRate'] = surveyDataByGroup['pq7.1']/ surveyDataByGroup['counter']

if lang == 'english':
    ax = sns.barplot(x = surveyDataByGroup.index, y = surveyDataByGroup['awarenessRate'],
                 order=firmSizeCategories, color='salmon')
    ax.set(xlabel='Size of business', ylabel='Percentage aware of any govt. relief measures')
    #sns.savefig('D:/Dropbox (Personal)/small-biz-2020/writeup/Figures/US_Awareness_bySize.eps', format='eps')

elif lang == 'spanish':
    ax = sns.barplot(x = surveyDataByGroup.index, y = surveyDataByGroup['awarenessRate'],
                 order=firmSizeCategories, color='salmon')
    ax.set(xlabel='Tamaño de empresa', ylabel='Porcentaje que conoce medidas del gobierno')



print('Figure: % who know about policy X, conditional on declaring they know something')
data = surveyData[surveyData['pq7.1']==1].copy()
toplot = data[['pq7.2_1','pq7.2_2','pq7.2_3','pq7.2_4']].sum()/data['pq7.1'].sum()
ax = sns.barplot(x = ['Loans','Cover wages','Cover rent','Defer payments'],y = toplot, color='salmon')
ax.set(ylabel='Share of owners who know the policy')


#%% Get some quotes
toexport = surveyData[['q12.1','q12.2']].copy()

toexport.to_csv('long_responses.csv')




