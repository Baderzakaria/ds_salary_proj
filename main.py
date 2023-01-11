#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 19:25:32 2023

@author: baderzakaria
"""

import glassdor_scrapper as gs
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

path = "./chromedriver"

df = gs.get_jobs('Data Entry', 500, False, path, 5)

df.to_csv("glassdor_jobs2.csv",',')


