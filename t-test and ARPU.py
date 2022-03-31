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


# In[3]:


ab = pd.read_csv("C:\\Users\\nightsone\\problem2.csv", sep=';')

control_g = ab.query("testgroup == 'a'")
test_g = ab.query("testgroup =='b'")

arpu_control = control_g['revenue'].sum() / control_g['user_id'].nunique()
arpu_test = test_g['revenue'].sum() / control_g['user_id'].nunique()
print('arpu_control =', arpu_control)
print('arpu_test =', arpu_test)
stats.ttest_ind(control_g.revenue, test_g.revenue)


# In[ ]:




