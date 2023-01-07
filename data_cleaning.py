#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  7 12:24:04 2023

@author: baderzakaria
"""

import pandas as pd

df=pd.read_csv("glassdor_jobs.csv")

# salary parsing

#remove null estimates
df=df[df['Salary Estimate']!='-1']


#compnay name text only

#state field 

# age of the company 

#parsing of job description

