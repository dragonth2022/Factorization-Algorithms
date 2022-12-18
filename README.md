# Factorization-Algorithms
This project aims to implement the 3 best integer factorization algorithms currently known. They are (in the order to be implemented):

1. Lenstra Elliptic Curve Factorization
2a. Rational Sieve
2. Quadratic Sieve
3. General Number Field Sieve

At time of writing, I could not find any implementation of the abovementioned algorithms together with an accessible explanation that walks the reader through the code. This project aims to change that.

Integer factorization is an important problem. The hardness of this problem is the mathematical foundation that RSA-encryption rests on. As such, these 3 algorithms are considered to be "enemies of RSA". In particular, security standards for RSA are currently determined by how fast Generic Number Field Sieve runs on the latest hardware.
