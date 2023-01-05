#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 19:25:32 2023

@author: baderzakaria
"""

import glassdor_scrapper as gs
import pandas as pd

path = "./chromedriver"

df = gs.get_jobs('java', 15, False, path, 10)

print(df)