# -*- coding: utf-8 -*-
"""
Created on Mon Jan  2 12:07:32 2023

@author: Zhao Yufan
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 16:35:13 2022

@author: Zhao Yufan
"""
"""

MOTIVATION:

Problem:
    "Given a composite number n, compute a prime factor of n."

The fastest known general purpose factoring algorithm for factoring a number n
is the General Number Field Sieve (GNFS) that runs in sub-exponential time.

It does not rely on the existence special properties/internal structures of n.
However, there are other algorithms that do (with massive speed ups, if the 
special properties are satisfied) :
    
    1. Naive Trial Division (Favours small primes)
        -Try dividing by small primes 2,3,5,7,....
        -If n has small prime factors, Naive Trial Division will find it
         much much faster than any other algorithms here.
        
    2. Fermat Factorization Method (Favours primes close to sqrt(n) )
        -Try adding small squares 1,4,9,16,25.... (stop when desired) to n
         (i.e. calculate n+1, n+4, n+9, n+16, n+25, ..., n+x**2 = a**2,...)
        
        -If any of these numbers is a perfect square a**2, then we can rearrange
         the equation to n = a**2 - x**2, which gives a factorization
         n = (a+x)(a-x)
        
    3. Special Number Field Sieve 
        -Favours s of the form n = r**e +- s, for small r and s   
        -Works well for Mersenne Numbers and finding Mersenne Primes
        -Mersenne Numbers are numbers of the form 2**k - 1 for some integer k
    
    4. Lenstra's Elliptic Curve Factorization Algorithm
        -Favours medium sized primes of up to 60 digits (180-210 bits)
        -We are implementing this algorithm right now.
"""

#########    HELPER FUNCTIONS ##############

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
In the second step, we need a function to solve the following problem:
    
    'Given two numbers a and m, find the multiplicative inverse of a modulo m'

We implement this function now, but we need to take extra care. This step is 
needed to work with division in finite fields.

A crucial step of The Lenstra Elliptic Curve Factorization relies on the 
FAILURE to find an inversion modulo n. In Python, this will raise a 
'ValueError'.

Later on we must catch this error. Along with this, we want to keep track
of some data that caused this error. This piece of data will eventually
help us factor n.

SPECIFICATIONS:

Given two integers a and m, return an integer x such that a*x = 1 (mod m)

If such an inverse does not exist, raise ValueError.

"""

###Python 3.8 and later. Use Built in pow function:
    
def mod_inverse(a , m):
    output = pow(a, -1, m)
    return output

### Python 3.7 and earlier. Use extended euclidean elgorithm:
### 'egcd' stands for 'extended greatest common divisor'
### 'greatest common divisor' is found using the standard euclidean algorithm
### we are extending it to find something else (modular inverse), hence the name
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def mod_inverse2(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise ValueError('base is not invertible for the given modulus')
    else:
        return x % m


"""
The third step will implement an "addition of points on elliptic curves"
into a function.

-Elliptic Curves, a construction from Algebraic Geometry, is the central object
of interest in the Lenstra Elliptic Curve Factorization algorithm.

-Roughly speaking they are "graphs" of equations of the form y**2 + x**3 + a*x + b.
Points on this graph have a nice "addition structure".

-We will assume the reader is familiar with how this is defined.

-If not, refer to:
    https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication


This is not the elliptic curve point addition algorithm
in its purest and most general sense. We have modified it for our 
integer factorization task. Note the following assumptions:
    
    1. We are not working over a genuine field. 
    
    2. Instead we are working over:
    Z/nZ ~= Z/pqZ
    which is a ring, where not all elements are invertible.
    
    3. The chinese remainder theorem says that:
        Z/nZ ~= Z/pZ x Z/qZ
        
    4. Our curve is "y**2 + x**3 + a*x + b" over the ring "Z/mZ"
    
    5. Function parameters are labelled as in point 4.
    
SPECIFICATIONS:

Given two points p, q on an elliptic curve y^2 = x^2 + ax + b over a ring Z/mZ,
return the point p+q.

    1. p and q are 2-tuples (x1,y1) and (x2,y2) of integer type
    2. a , b , m are genuine integers of integer type
    3. compute (x3,y3), the result of elliptic curve point addition p+q,
       if the operation is possible
    4. If computing (x3,y3) failed, compute the value that we tried to 
       invert that caused this failure.
    5.  return 3 pieces of information: success_of_addition, failure_value, (x3,y3)

"""

def elliptic_add(p , q , a , b , m):
    success = -1
    value = -1
    point = ('x' , 'x')
    
    if p == 'Point At Infinity':
        success = 1
        value = -1
        point = q
        return success , value , point
    
    elif q == 'Point At Infinity':
        success = 1
        value = -1
        point = p
        return success , value , point
    
    else:
        
    
        x1 , y1 = p[0] , p[1]
        x2 , y2 = q[0] , q[1]
        
        assert (y1**2)%m == ((x1**3)%m + (a*x1)%m + b)%m , '1st point is not on curve'
        assert (y2**2)%m == ((x2**3)%m + (a*x2)%m + b)%m , '2nd point is not on curve'
        
        if x1 != x2:
            
            try:
                #calculating the gradient
                lamb = (((y2 - y1)%m) * mod_inverse((x2-x1)%m , m))%m
                
            except ValueError:
                #if we get this error, it means gradient calculation failed
                #We want to know what caused this failure
                #This cause will help us factorize n
                success = -1
                value = (x2-x1)%m
                point = ('x','x')
                return success , value , point

        elif (x1 == x2) and y1%m == (m - y2)%m:
            success = 1
            value = -1
            point  = 'Point At Infinity'
            return success , value , point
        
        elif (x1 == x2) and y1 != 0:
            try:
                lamb = ((((3*((x1)**2)%m)%m + a))%m * mod_inverse((2*y1)%m , m))%m
            except ValueError:
                #if we get this error, it means 2*y1 was not invertible mod m
                #this means gcd(2*y1,m) is not 1
                #this helps us factorize n
                success = -1
                value = (2*y1)%m
                point = ('x','x')
                return success , value , point 

        
        else:  
            #if this gets  executed, we are adding two points both with order 2
            success = 1
            value = -1
            point = 'Point At Infinity'
            return success , value , point
        
        #if we reach here, it means the addition was successful
        success = 1
        value = -1
        x3 = ((lamb**2)%m - x1 - x2)%m
        y3 = ((((x1-x3)%m)*lamb)%m - y1)%m
        point = (x3,y3)
        
        return success , value , point

"""
The fourth step is to implement a "multiplication of points on elliptic curves"
into a function.



SPECIFICATIONS:

Given a point p on the elliptic curve y**2 + x**3 + a*x + b over a ring Z/mZ,
and an integer k, return three pieces of information:
    success , cause_of_failure, (xkp,ykp)

    1. Again, remember that we are working over Z/mZ, not a genuine field.
    2. p is a 2-tuple (x0,y0) of integer types
    3. a , b , m , k are genuine integers of integer type
    4. returns success , cause_of_failure, (xkp,ykp) result of elliptic curve 
       point multiplication.
"""

def elliptic_multiply(p , k , a , b , m):
    
    result = 'Point At Infinity'
    
    while k > 0:
        
        if k % 2 == 1:
            #attempt to update result
            success , value , result = elliptic_add(p , result , a , b , m)
            
            if success == -1:
                #If this is executed, means update failed. Return value now.
                return success , value , result
            
        
        k = k // 2
        #attempt to update point p
        success , value , point = elliptic_add(p , p , a , b , m)

        if success == 1:
            #update point p if addition was successful
            p = point
        else:
            #if this is executed, means addition failed. Return value now.
            return success , value , point
        

    return success , value , result
    


"""
The fifth and final step is to implement the Lenstra Elliptic Curve Algorithm
in full, using the helper functions above.

The theory behind the algorithm is as follows:
    
    1. Work over the ring Z/nZ. Suppose that n is the product of two primes p,q.
    
    2. The chinese remainder theorem says that Z/nZ is isomorphic to Z/pZ x Z/qZ.
    
    3. Pick an elliptic curve E: y**2 = x**3 + a*x + b and a point (x0,y0)
       on the curve.
       
    4. Both Z/pZ and Z/qZ are fields. Consider the elliptic curve E over them.
       Write them as E(Fp) and E(Fq).
    
    5. The algorithm relies on Lagrange's Theorem and the fact that E(Fp), E(Fq)
       are finite groups, with varying sizes as E changes.
       5a. For a fixed curve E, let the sizes of E(Fp) and E(Fq) be N and M 
           respectively.
       5b. Let g be any point on E(Fp). Lagrange's theorem says that
           Ng = 'Point At Infinity' in E(Fp)
       5c. Also, Kg = 'Point At Infinity' in E(Fp) whenever K is a multiple of 
           the order of g, which must divide N by Lagrange's Theorem.
       5d. If we are lucky in picking K, E and g, we will recover a factor of n.
       5e. While we do not know the exact probability, heuristics tells us that
           luck is on our side.
       5f. This is the fastest known factoring algorithm if the smallest factor
           of n is around 10**50 to 10**60 or less.
    

    6. N is the number of points on E(Fp). Hasse theorem on elliptic curves says:
        |N-(p+1)| <= 2*sqrt(p)
       The same holds for q.
       
    7. Let K denote some integer. We attempt to calculate points KP via
       elliptic curve point multiplication. Doing this involves performing 
       multiplication inverses modulo n.
       
        6a.Picking good values for K is the main limiting reason that might cause
           this algorithm to fail to find a factor of n.
           
    8. If the inverse cannot be found, it means we are at the 'point of infinity'
       on either Z/pZ or Z/qZ.
       
    9. Say the un-invertible element was t. Taking gcd(t,n) will (hopefully)
       yield a non-trivial proper factor of n (either p or q).
       
       
       
Having discussed the theory, we now describe the steps of the algorithm in
detail (Following the code)
    0. Inputs: (i)   The integer n to be factorized
               (ii)  A bound, the maximum value of k we shall examine
                     In practice, it is sufficient to only examine primes
               (iii) The number of curves we wish to examine
               (note that increasing 'bound' and 'curves' essentially
                specifies the amount of computation resources we wish to spend
                on factoring n)
    
    1. Check that n%2 != 0 and n%3 != 0. 
        1a. The primes 2 and 3 cause problems when working with Elliptic Curves. 
            Extra non-trivial math is needed to deal with these 2 special cases 
            if we do not exclude them now. But in the computation realm, 
            excluding them is just a matter of 2 trivial 'assert' statements.
            
    2. Pick a random elliptic curve and a point p = (x0,y0) on the curve.
        2a. Keep count of the number of curves tried.
        
    3. Calculate the discriminant of the curve, then check gcd(discriminant,n).
       If this is not 1 or n, return it immediately. If it is n, pick another curve.
       3a. This is another special case and we got lucky.
       3b. If we do not check for this, and it happens that 
           gcd(discriminant,n) != 0, the curve is 'Singular' over either Fp or Fq. 
       3c. Proceeding with the rest of the algorithm will cause problems,
           because the mathematical theory does not hold in this case.
    
    4. At point p = (x0,y0), calculate its 'tangent slope'.
        (This is a step in multiplying p by 2. We pre-check this for optimization purposes)
       4a. If this raises 'ValueError', it means we got lucky, and p is a point
           of order 2, and we have also found a non-invertible element t of Z/nZ.
       4b. Calculate gcd(t,n). If this is neither 1 nor n, return it.
       
    5. For K in 2,3,4,5,6,7,..., bound , calculate KP:
        5a. If any of them fail, elliptic_multiply(*) will tell us the
            non-invertible element t in Z/nZ that caused this failure.
        5b. Calculate gcd(t,n). If this is neither 1 nor n, return it.
        (5c. An alternative way for choosing K is to choose small powers of 
            primes generated using primes_up_to(n) implemented on line 54.)
    
    6. If step 5 passes and curve_count < curves, try another curve.
        Else: return 'Failed to find factor with given bound and curves'.
       
       
"""
from random import randint
from math import gcd
from MillerRabinPrimalityTest import MillerRabin

def lenstra(n , bound , curves):
    assert n%2 != 0 , 'please first factor out the prime 2'
    assert n%3 != 0 , 'please first factor out the prime 3'
    discriminant = 0
    curves_tried = 0
    
    guess = n
    if guess == 1:
        return -1
    while guess == n and discriminant == 0:
        #initialize with a random point (x,y)
        #find a curve y**2 + x**3 + a*x + b that (x,y) lies on
        
        for _ in range(curves):
            
            curves_tried = curves_tried + 1
            x0 , y0 = randint(0,n-1) , randint(0,n-1)
            p = (x0 , y0)
            
            #randomize coefficient a, compute b to ensure p is on curve
            a = randint(0, n - 1)
            b = ((y0**2)%n - (x0**3)%n - (a*x0)%n)%n
            #curve is now y**2 + x**3 + a*x + b
            
            
            #Try getting lucky with discriminant of curve
            #Check discriminant of curve when interpreted over rational numbers Q
            #If discriminant has non-trivial, proper common factor with n,
            #This means we got lucky and we found one prime factor of n
            #The subsequent operations will also not work, because curve is 
            #singular over either Fq or Fp, might as well return answer now.
            
            
            
            d = 4 * (a**3) + 27 * (b**2)
            guess = gcd(d , n)
            if guess != 1 and guess != n:
                output = gcd(guess,n)
                if MillerRabin(output) is True:
                    return output
                else:
                    return lenstra(output , bound , curves)
            
            #Try getting lucky with starting point p
            xp , yp = p[0] , p[1]
            try:
                slope_at_p = (((3*((xp**2)%n))%n + a)%n) * mod_inverse( (2*yp)%n , n)
            except ValueError:
                output = gcd((2*yp)%n , n)
                
                if MillerRabin(output) is True:
                    return output
                else:
                    return lenstra(output , bound , curves)
                
            except TypeError:
                continue
            
            
            #If we reach here, we are not lucky
            #prime_list = primes_up_to(bound)
            
            #for item in prime_list:
            primes_to_check = primes_up_to(bound)
            for count in range(10):
                for item in primes_to_check:
                    
                    #before proceeding, check if current point produces factor
                    try:
                        slope_at_p = (((3*((xp**2)%n))%n + a)%n) * mod_inverse( (2*yp)%n , n)
                    except ValueError:
                        output = gcd((2*yp)%n , n)
                        
                        if MillerRabin(output) is True:
                            return output
                        else:
                            return lenstra(output , bound , curves)
                        
                    except TypeError:
                        break
    
                    
                    #if it does not, update point
                    success , value , new_point = elliptic_multiply(p , item , a , b , n)
                    if success == -1:
                        output = gcd(value,n)
                        
                        if MillerRabin(output) is True:
                            return output
                        else:
                            return lenstra(output , bound , curves)
                        
                        
                    p = new_point
                    xp , yp = p[0] , p[1]
                
                
        #If we reach here, we failed to find a factor with specified bounds and curves
        #return 'Failed to find factor with specified smoothness bound and max curves tried'
        return -1

                





















