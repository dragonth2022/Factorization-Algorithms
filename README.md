# Factorization-Algorithms
Integer factorization is an important problem. The hardness of this problem is the mathematical foundation that RSA-encryption rests on. As such, these 3 algorithms are considered to be "enemies of RSA". In particular, security standards for RSA are currently determined by how fast Generic Number Field Sieve runs on the latest hardware.

In this project, I aim to implement the 3 (4?) best integer factorization algorithms currently known, as I learn them. They are (in the order to be implemented):

1. Lenstra Elliptic Curve Factorization (main prototype done, optimizations, extensions, and simplifications not yet done)
2. Quadratic Sieve
3. General Number Field Sieve
4. (?) Rational Sieve

At time of writing, I could not find any implementation of the abovementioned algorithms together with an accessible explanation that walks the reader through the code. This project aims to change that.

The Lenstra Elliptic Curve Factorization algorithm makes use of constructions from Algebraic Geometry (elliptic curves) to factor integers in sub-exponential time. This is a probabilistic algorithm that best works for numbers with prime factors less than 10^60. It is based on the earlier 'Pollard's p-1 Algorithm' that uses the cyclic group (Z/nZ)*. Lenstra extends it by replacing it with elliptic curve groups. There is a further stage-2 extension after Lenstra. The base version of Lenstra is already done. I aim to implement both 'Pollard's p-1' and 'stage-2' sometime in future, together with some other optimizations.

Rational, Quadratic, and General Number Field Sieves are in the same family of factoring algorithms that uses Algebraic Number Theory. Each is a generalization/extension of the previous, with Rational Sieve being the easiest to understand (but the slowest) and General Number Field Sieve being the hardest (and also the fastest), involving a vast amount of graduate level mathematics.

Quadratic Sieve lies somewhere in the middle. Due to differences in the amount of set-up required, it is the fastest algorithm for numbers with prime factors between 10^60 and 10^100, despite having a slightly higher complexity than the General Number Field Sieve.

To compare performance, I have also added a naive factorization algorithm, which simply tries to divide n by all primes less than sqrt(n).

Try factorizing n = 100100310010033003009 to see the difference:

lenstra(100100310010033003009 , 2000000 , 5)

naive_factorize(100100310010033003009)
