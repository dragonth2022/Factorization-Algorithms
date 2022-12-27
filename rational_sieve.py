# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 14:04:05 2022

@author: Zhao Yufan
"""
"""
Problem:
    "Given a composite number n, compute a prime factor of n."

The fastest known general purpose factoring algorithm for factoring a number n
is the General Number Field Sieve (GNFS) that runs in sub-exponential time.

We will work towards implementing that. To understand its concepts, we first
implement the more basic Rational Sieve here.


"""
"""
(Warm Up)
The first step implement the Sieve of Eratosthenes algorithm for finding
prime numbers up to a given bound n (specified by input)

This helper function will be useful for generating one of the parameters used in
the algorithm.
"""

def primes_up_to(n):
    primeCheck = [True]*(n+1) #boolean array indicating if index is prime
    primeCheck[0] = False
    primeCheck[1] = False
    primes = []
    p = 2
    
    while p**2 < n:
        
        if (primeCheck[p] is True):
            for i in range(p**2 , n+1 , p):
                primeCheck[i] = False
        
        for j in range(p+1,n+1):
            if primeCheck[j] is True:
                p = j
                break
    
    for k in range(n+1):
        if primeCheck[k] is True:
            primes.append(k)
    
    return primes

"""
The second step is to know how to check if a number is 'B-smooth'. 
A number z is called B-smooth if all its prime factors are less than B.

For this, we need 2 helper functions:
    1. A function that breaks down a number into its prime factorization (as a list);
    2. A function to check if all prime factors in that list is less than B.
    
for 1, we will use naive_factorzation. Even though this is one of the worst
factorization algorithms for large n, it is suitable for our purpose here because
it has the least setup/overhead for small n. Since Rational Sieve itself is not intended
for large n, naive_factorization works here.
"""

import math


def prime_factors(number):
    prime_factors = {}
    t = number
    i = 2
    while i < math.isqrt(t) + 1:
        if t % i == 0:
            prime_factors[i] = 0
            while t % i == 0:
                prime_factors[i] = prime_factors[i] + 1
                t = t // i
        i = i+1
    if t > 1:
        prime_factors[t] = 1
    return prime_factors
                

#B-smooth check
def is_B_smooth(prime_factors , B):
    return max(prime_factors) in primes_up_to(B)

"""
The third step is to generate some relations.

We now fix a bound B, and an integer z, such that both z and z+n are B-smooth.
For Rational Sieve to run smoothly, B cannot be too large.
The Sieve of Eratosthenes will help us here.

We will then compute the prime factors of z and z+n to generate the relations
we seek.

This step involves factoring z+n, so it somewhat turns into a recursive problem.
However, since we generally only expect n to be difficult to factorize and we
have the freedom to choose z, factoring z+n should be an easier task than
factoring n.

Moreover, we can use other algorithms (Lenstra Elliptic Curves, Naive Factorize),
so we are not making a circular argument.

However, for the case of the rational sieve, we will simply use naive_factorization.
Rational sieve is only suitable for small small integers, z+n and z should be small too.
naive_factorization in this case would be the fastest since it involves the least
amount of setup (compared to say, Pollard's or Lenstra's)

"""
def build_relations(n , B):
    relations = []
    for i in range(2,n):
        z_factors = prime_factors(i)
        if is_B_smooth(z_factors , B):
            zn_factors = prime_factors(n+i)
            if is_B_smooth(zn_factors , B):
                relations.append({"z": z_factors, "zn": zn_factors})
    
    return relations
"""
In the fourth step, we make use of the fact that Rational Sieve attempts to
obtain squares that are congruent mod n.

To do this on paper, we rewrite the factors of z and z+n into prime**exponent
form, and then reduce the exponents mod 2. We could also multiply out different relations to check if the exponents are even.

We write out a function to check this condition.
"""


def is_even(factor_dict):
    for factor in factor_dict:
        if factor_dict[factor] %2 != 0:
            return False 
    return True

"""
In the fifth step, we need a way to multiply two numbers together in prime factors form.

To achieve this, we will write a "prime_multiply" function.

Input:
    two integers: 
        n = {n_primes* : n_exponents*}
        m = {m_primes* : m_exponents*}
Output:
    one integer:
        nm = {nm_primes* : nm_exponents*}
"""

def prime_multiply(n_factors , m_factors):
    #merge keys together first:
    nm_factors = n_factors | m_factors
        
    for key in nm_factors:
        
        try:
            nm_factors[key] = n_factors[key] + m_factors[key]
        
        except KeyError:
            #'key' is not a prime factor of either n or m
            #either way, | already produced correct value for nm_factors
            continue
        
    return nm_factors

"""
The final step is to put all these together into the Rational Sieve algorithm.
"""
import itertools
#import math #already imported above


def rational_sieve(n , B):
    relations = build_relations(n , B)
    for L in range(1 , len(relations)+1):
        for subset in itertools.combinations(relations , L):
            if L == 1:
                current_relation = [subset[0]['z'] , subset[0]['zn']]
                
            else:
                current_relation = [subset[0]['z'] , subset[0]['zn']]
                subset_length = len(subset)
                for J in range(1 , subset_length):
                    current_relation[0] = prime_multiply(current_relation[0] , subset[J]['z']  )
                    current_relation[1] = prime_multiply(current_relation[1] , subset[J]['zn'] )
            if is_even(current_relation[0]) and is_even(current_relation[1]):
                x = 1
                y = 1
                for prime in current_relation[0]:
                    x = x * (prime**(current_relation[0][prime]//2))
                for prime in current_relation[1]:
                    y = y * (prime**(current_relation[1][prime]//2))
                
                    
                p = math.gcd(x-y , n)
                if p != 1 and p != n:
                    return p
                
                p = math.gcd(x+y , n)
                if p != 1 and p != n:
                    return p

"""
as with any good algorithm implementation, we must craft some test cases:
"""
test_1 = 2993 # 41*73
bound_1 = 20
print(rational_sieve(test_1,bound_1))

import time

st = time.time()
test_2 = 72781  # 73*997
bound_2 = 500

st = time.time()
print(rational_sieve(test_2,bound_2))
et = time.time()

print(et-st)
    




























