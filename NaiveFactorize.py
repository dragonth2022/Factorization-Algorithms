# -*- coding: utf-8 -*-
"""
Created on Sun Dec 18 22:47:40 2022

@author: Zhao Yufan
"""
import math


#naive factorization. simply checks all integers less than sqrt(n)
def naive_factorize(n):
    maxfactor = math.floor(math.sqrt(n))+1
    for number in range(2,maxfactor+1):
        if n%number == 0:
            return number
        else:
            continue
    
    return 'input was prime'
    
    
    
