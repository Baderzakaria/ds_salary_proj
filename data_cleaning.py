#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  7 12:24:04 2023

@author: baderzakaria
"""

import pandas as pd

df=pd.read_csv("glassdor_jobs.csv")

#>>>>>>>>salary parsing


#remove empties

#hourly from per year

df['hourly'] = df['Salary Estimate'].apply(lambda x : 1 if 'per hour' in x.lower() else 0)

#remove employer provided from salary
 
df['employer _provided'] = df['Salary Estimate'].apply(lambda x : 1  if 'employer provided salary:' in x.lower() else 0)


df=df[df['Salary Estimate']!='-1']

#split before ()
salary = df['Salary Estimate'].apply(lambda x : x.split('(')[0] )

#remove the K $ and per hour and employer...

minus_kd = salary.apply(lambda x: x.replace('K','').replace('$',''))


minus_hr = minus_kd.apply(lambda x: x.lower().replace('per hour','').replace('employer provided salary:',''))

#get the min hour after removing the splitter 

df['min_salary'] = minus_hr.apply(lambda x: int(x.split('-')[0]))

#setting the data type of this new column to d type integer
df['min_salary'].dtype

df['max_salary'] = minus_hr.apply(lambda x: int(x.split('-')[1]))
df['max_salary'].dtype
#calculating the average

df['avg_sal']= (df['min_salary']+df['max_salary'])/2


#compnay name text only
# we will apply this when u had to use in lambda another column since it cant be linked to x
df['company_txt']=df.apply(lambda x: x['Company Name'] if x['Rating'] <= 0 else x['Company Name'][:-3],axis =1)

#state field 

df['job_state']= df.apply(lambda x: x['Location'].split(',')[0],axis= 1)

df.job_state.value_counts()

#if the job location is in the same headquarter

df['same_city']=df.apply(lambda x : 1 if x.Location== x.Headquarters else 0,axis = 1)

# age of the company 

df['age'] = df.Founded.apply(lambda x: x if x<1 else 2022 - x )

#>>>>>parsing of job description 

#find python 

df['python_yn']=df['Job Description'].apply(lambda x : 1 if 'python' in x.lower() else 0)
df.python_yn.value_counts()

df['rstudio_yn']=df['Job Description'].apply(lambda x : 1 if 'r studio' in x.lower() or 'r-studio' in x.lower() else 0)
