#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

import scipy.stats as stats
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.multicomp import pairwise_tukeyhsd

pd.options.mode.chained_assignment = None


# In[6]:


reg_time = pd.read_csv("C:\\Users\\nightsone\\problem1-reg_data.csv", sep=';')
aut_data = pd.read_csv("C:\\Users\\nightsone\\problem1-auth_data.csv", sep=';')

havenan_reg = reg_time.isnull().any()
havenan_auth = aut_data.isnull().any()


print('Есть ли Nan', '\n')

print(havenan_reg)
print(havenan_auth, '\n')

print('Уникальные значения', '\n')

uniq_reg = reg_time.nunique()
uniq_auth = aut_data.nunique()
print(uniq_reg)
print(uniq_auth)

# sec to date 

reg_time["reg_ts"] = pd.to_datetime(reg_time["reg_ts"], unit='s')
aut_data["auth_ts"] = pd.to_datetime(aut_data["auth_ts"], unit='s')


# In[7]:


merge_all = reg_time.merge(aut_data, how='outer')
merge_all['days_per_user'] = (merge_all['auth_ts'] - merge_all['reg_ts']).dt.days + 1

merge_all['reg_ts'] = pd.to_datetime(merge_all['reg_ts'],format='%m/%Y/%d').dt.to_period('d')
merge_all['auth_ts'] = pd.to_datetime(merge_all['auth_ts'],format='%m/%Y/%d').dt.to_period('d')

list(merge_all.columns.values)
final_df = merge_all[['uid', 'reg_ts', 'auth_ts', 'days_per_user']]

q = final_df.head(1000000)


# In[10]:


group = q.groupby(['reg_ts', 'days_per_user'])
cohort_data = group['uid'].size()
cohort_data = cohort_data.reset_index()


# In[11]:


# create cohort and set base cohort

cohort_counts = cohort_data.pivot(index='reg_ts', columns='days_per_user', values='uid')
base = cohort_counts[1]

# calculate retention rate

retention = cohort_counts.divide(base, axis=0).round(2)
retention.fillna(0).tail(50)


# In[10]:


# function of retention rate


def retention_rate (cohort_data, cohort_counts):
    try:
        cohort_counts = cohort_data.pivot(index='reg_ts', columns='days_per_user', values='uid')
        base = cohort_counts[1]
        retention = cohort_counts.divide(base, axis=0).round(3)

        return retention.fillna(0)
    except ZeroDivisionError:
        return 0
    
print(retention_rate(cohort_data, cohort_counts))

