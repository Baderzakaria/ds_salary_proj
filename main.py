#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 19:25:32 2023

@author: baderzakaria
"""

import glassdor_scrapper as gs
import pandas as pd

path = "./chromedriver"

df = gs.get_jobs('Data Entry', 100, False, path, 5)

df.to_csv("glassdor_jobs2.csv",',')


