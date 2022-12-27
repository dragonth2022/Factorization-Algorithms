# -*- coding: utf-8 -*-
"""
Created on Sun Feb 17 22:29:50 2019

@author: zhao yufan
"""
import secrets
import math

def MillerRabin(n):
    
    reallyrandomint = secrets.SystemRandom()
    m = n-1
    
    if n < 1:
        verdict = 'Error message: Please enter a POSITIVE integer.'
    
    elif n == 1:
        verdict = False
        
    elif n == 2:
        verdict = True
        
    elif n%2 == 0:
        verdict = False
        
    else:
        def extract2(m):
            a = m-1
            b = ~a
            c = m&b
            return c

        k = extract2(m)
        e = int(math.log(k,2))
        failcount= 0
        
        for r in range(10):
            
            x = reallyrandomint.randint(2,n-1)
            m = n-1
            
            for s in range(e):                            
                
                if pow(x , m , n) == 1:            
                    m = m//2                        
                                
                elif pow(x , m , n) == n-1:
                    break                   
                
                else:
                    failcount = failcount + 1
        
        if failcount != 0:
            verdict = False
        else:
            verdict = True
    return verdict
