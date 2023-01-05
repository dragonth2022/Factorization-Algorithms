# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 11:52:05 2022

@author: Zhao Yufan
"""

"""
Problem:
    "Given a composite number n, compute a prime factor of n."

The fastest known general purpose factoring algorithm for factoring a number n
is the General Number Field Sieve (GNFS) that runs in sub-exponential time.

We will work towards implementing that. To understand its concepts, we first
implement the more basic Quadratic Sieve here. Due to the amount of overhead/setup
required for the GNFS, the Quadratic Sieve is still the fastest algorithm
for n with prime factors of up to around 100 digits (~300 - 350 bits).

The Quadratic Sieve works similarly to the Rational Sieve with just 1 difference:
    - Instead of finding relations by factoring z and z+n, we look for numbers
      x, y and a quadratic polynomial P such that P(x)P(y) is a square modulo n.
      (hence the name 'Quadratic Sieve')

The rest of the algorithm proceeds exactly like the Rational Sieve:
    - Use these squares to find relations, and then express n as a difference 
    of two squares.


"""
"""
Helper functions

We need the following helper functions:
    
    0.1 Floor square root
    0.2 gcd function (math library)
    0.3 modular exponentiation function (built in pow(a,b,c))
    0.4 modular inverse function (built in pow(a,b,c))
    0.5 Miller-Rabin primality test (already done)
    0.6 Generating random numbers with a fixed number of bits
    0.7 Generating random primes with a fixed number of bits (done from 0.6)
    0.8 (TO DO) Function for calculating the Legendre Symbol (Euler's Formula)
    0.9 (TO DO) Function for calculating square roots modulo p (Shanks-Tonelli)
    0.10(TO DO) Function for quick gaussian elimination over GF(2)
    
(All steps 0.1 - 0.7 are already complete in some form or another: either a 
 built in function, in some library, or in another file in this repository)
    
"""
"""
The first step (0.8) is to implement Euler's formula for calculating the Legendre Symbol:
    
inputs: an integer 'a' and a prime 'p'
output: 1 if there exists some integer x such that x**2 is congruent to a mod p
        -1 if such a value for x does not exist
"""
from math import gcd , log

def legendre(a , p):
    assert gcd(a , p) == 1
    check = pow(a , (p-1)//2 ,p)

    if check == 1:
        return 1
    elif check == p-1:
        return -1
    else:
        raise ValueError ( 'is p prime?')

"""
The second step (0.9) is to implement the Shanks-Tonelli algorithm for computing
integer square roots modulo a prime p.

inputs: an integer 'b' and a prime 'p'
output: an integer 'x' such that x**2 = b (mod p), if it exists
"""
def extract2(m): #returns the highest power of 2 that divides m
    return len(bin(m&(~(m-1))))-3

def extract3(m): #returns the highest power of 3 that divides m
    temp = m
    count = 0
    while temp%3 == 0:
        count = count + 1
        temp = temp // 3
    return count

def rep_square_to_1(x , p):
    count = 0
    temp = x
    while temp%p != 1:
        count = count + 1
        temp = (temp**2)%p

    return count

def mod_p_sqrt(n , p):
    
    assert legendre(n , p) == 1 , ('n is not a quadratic residue modulo p')
    
    z = 1
    while legendre(z , p) == 1:
        z = z+1
        
    S = int( log(extract2(p-1) , 2) )
    Q = (p-1)//(extract2(p-1)) 
    M = S
    c = pow(z , Q , p)
    t = pow(n , Q , p)
    R = pow(n , (Q+1)//2 , p)    

    if t == 0:
        return 0
    if t == 1:
        return R
    else:
        while t!=1:
            
            i = rep_square_to_1(t , p)    
            b = pow(c , pow(2 , M-i-1)  , p)   
            M = i
            c = pow(b,2,p)
            t = (  t * c )%p
            R = (R*b)%p
    
            if t%p == 1:
                return R
"""
The third step is to implement a function to do gaussian elimination on a matrix
over GF(2). 

Input: A matrix (not necessarily square) with entries in GF(2).
Output: An element of the null space.

This algorithm is taken from:
    
https://www.cs.umd.edu/~gasarch/TOPICS/factoring/fastgauss.pdf
"""
from copy import deepcopy
def ge_gf2(M): #M is a matrix over GF(2)
    #no. of rows = n
    #no. of columns = m
    temp = deepcopy(M)
    rows = len(temp)
    cols = len(temp[0])
    row_marking = [False]*rows
    assert cols <= rows
    #print(temp)
    for j in range(cols): # for each column:
        #search for A_ij = 1 in column j
        for i in range(rows):
            if temp[i][j] == 1:
                #temp1 = (i,j)
                row_marking[i] = True
                #print(row_marking)
                for k in range(cols):
                    if k == j:
                        continue
                    
                    if temp[i][k] == 1: 
                        #add column j to column k, iterate over rows
                        for count in range(rows):
                            temp[count][k] = (temp[count][j] + temp[count][k])%2
                    
                break
        #print(temp)
            
    solutions = []
    for count in range(rows):
        if row_marking[count] == False:
            free_row = [temp[count],count]
            solutions.append(free_row)
    
    if solutions == []:
        return 'No solution found. Consider the smoothness bound B.'
    
    #print("Found {} potential solutions.".format(len(solutions)))
    return solutions , row_marking , temp , M
                    
                
def solve_row(solutions,temp,row_marking,K=0):
    solution_vec, indices = [],[]
    free_row = solutions[K][0] # may be multiple K
    for i in range(len(free_row)):
        if free_row[i] == 1: 
            indices.append(i)
    
    for r in range(len(temp)): #rows with 1 in the same column will be dependent
        for i in indices:
            if temp[r][i] == 1 and row_marking[r]:
                solution_vec.append(r)
                break
            
  
    solution_vec.append(solutions[K][1])       
    #print("Found linear dependencies at rows "+ str(solution_vec))   
    return solution_vec
"""
We need to improve our factoring algorithm. Naive factorization is not sufficient
here, because we aim to factorize larger numbers with the quadratic sieve 
compared to the rational sieve. To do this, we will use extract2, extract3, and
Lenstra's Elliptic Curve Method implemented earlier. We also use the
Miller Rabin Primality Test.

"""
import math
import LenstraEC
from MillerRabinPrimalityTest import MillerRabin

def prime_factors(number):
    n = number
    prime_factors = {}
    bound= 20000
    curves = 50
    
    temp = extract2(n)
    if temp != 0:
        prime_factors[2] = temp
    n = n//(2**temp)

    temp = extract3(n)
    if temp != 0:
        prime_factors[3] = temp
    n = n//(3**temp)
    
    if n == 1:
        return prime_factors
    
    primality = MillerRabin(n)
    

    while primality is False:
        factor = LenstraEC.lenstra(n , bound , curves)
        if factor != -1:
            try:
                prime_factors[factor] = prime_factors[factor]+1
                n = n//factor
            except KeyError:
                prime_factors[factor] = 1
                n = n//factor
            
            primality = MillerRabin(n)
    
    if (primality is False) and (factor == -1):
        return {-1:0}
    
    elif primality is True:
        try:
            prime_factors[n] = prime_factors[n]+1
        except KeyError:
            prime_factors[n] = 1

    return prime_factors

"""
we now implement the QS algorithm. The basic idea is as follows:
    0. Given a composite number n = pq, we want to find the unknown primes p and q.
    1. Set the parameters:
        (a) We use the simple polynomial Q(x) = x**2
        (b) Calculate M := floor(sqrt(n))
        (c) Determine a bound B for smoothness. Online sources suggest that a 
            good value for the bound B is B=2*e**(sqrt(log(n)log(log(n))/4)
    2. Notice that if x**2 = 0 (mod n), then also x**2 - n = 0 (mod n)
        (a) We want |LHS| to be as small as possible so the subsequent steps of 
            the algorithm, which require integer factoring as well, won't be 
            too troublesome (Use Lenstra's elliptic curve method for this)
        (b) To do this, we pick x from the interval [-M , M]. Equivalently,
            we start searching from M onwards, i.e. M+1, M+2, M+3, ...
    3. Notice that if x is in the sieving interval and some prime p divides Q(x),
       Then:
           (x - floor(sqrt(n)))**2 = n (mod p)
       so n is a quadratic residue mod p. We can therefore throw out primes
       that are not (from the list produced by the Sieve of Eratosthenes)
    4. Calculate x**2 - n (mod n) for multiple values x, and factorise the results.
    5. Collect the results. These are our relations
    6. Use linear algebra to find a product of relations that result in a
       congruence of squares.
    7. Use difference of 2 squares to factor n.
           


"""

from math import floor , ceil , sqrt , e

def evaluate2(A , B , C , x):
    return A*x**2 + B*x + C

def pnt(n):
    return ceil(n/log(n))

def bound(n):
    return floor(2*e**(sqrt( log(n)*log(log(n)) / 4 )))

def poly_gen_2():
    return 1 , 0 , 0

def get_factor_base(n, prime_set):
    factor_base = []
    for prime in prime_set:
        if legendre(n , prime) == 1:
            factor_base.append(prime)
    return factor_base

def build_relations(n , B , dimension):
    relations = []
    count = 0
    start_value = floor(sqrt(n))
    #print(start_value)
    while len(relations) < dimension:
        #print(relations)
        count = count + 1

        temp1 = (start_value + count)**2 - n
        #print((temp1, count))
        temp1_factors = prime_factors(temp1)
        if temp1_factors == 'error ECM failed':
            continue
        else:
            append = True
            for item in temp1_factors:
                if item > B:
                    append = False
                    break
            
            if append is True:
               relations.append((start_value + count,temp1_factors))
        
    return relations

def mod_mul(a, b, mod):
 
    res = 0
    a = a % mod
 
    while (b):
     
        if (b & 1):
            res = (res + a) % mod
             
        a = (2 * a) % mod
 
        b >>= 1
    return res
def prime_to_index(factor_base):
    indices = {}
    count = 0
    for prime in factor_base:
        indices[prime] = count
        count = count + 1
    return indices

def build_r_matrix(factor_base , relations):
    
    dimension = len(factor_base)
    count = 0
    prime_index = prime_to_index(factor_base)
    r_matrix = []
    for item in relations:
        temp3 = [0] * dimension
        for prime in item[1]:
            temp3[prime_index[prime]] = temp3[prime_index[prime]] + item[1][prime] % 2
        r_matrix.append(temp3)
        count = count + 1
    
    return r_matrix


def quadratic_sieve(n):
    B = bound(n)
    prime_set = LenstraEC.primes_up_to(B)
    factor_base = get_factor_base(n , prime_set)
    dimension = len(factor_base)
#start squaring at smallest values
    print('check 0')
    relations = build_relations(n , B , dimension)  
    print('check 1')
    #keep track of rows in relation_matrix and start_value+counter
    r_track = {}
    count = 0
    for item in relations:
        r_track[count] = item[0]
        count = count + 1
    
    #building the matrix

    r_matrix = build_r_matrix(factor_base, relations)
    
    solutions , row_marking , temp , M = ge_gf2(r_matrix)
    #take sum of rows in solution vec to get linear relation
    solution_vec = solve_row(solutions , temp , row_marking,K=0)
    print(solution_vec)
    
    LHS = 1
    RHS = 1
    #p_output keeps track of exponent of 
    p_output = [0]*dimension
    prime_index = prime_to_index(factor_base)
    
    for item in solution_vec:
        
        LHS = mod_mul(LHS, relations[item][0], n)
        p_tracker = relations[item][1]
        for prime in p_tracker:
            p_output[prime_index[prime]] = p_output[prime_index[prime]] + p_tracker[prime]
    
    for count in range(len(p_output)):
        p_output[count] = p_output[count]//2
        RHS = mod_mul(RHS , pow(factor_base[count] , p_output[count] , n) , n)
        
    
    return gcd(LHS-RHS, n)



#test_value = 140739635773439 # 65537 * 2147483647


















