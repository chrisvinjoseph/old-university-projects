from random import getrandbits
from random import randint
from math import sqrt
import sys

def main():
    if len(sys.argv) != 3:
        print("Needs 2 arguments")
        usage()
        exit(1)
    
    p_size = int(sys.argv[1])
    q_size = int(sys.argv[2])

    p = 0
    q = 0

    if p_size > 31 and q_size > 31:
        # getrandbits(n) generates integer representation of n bit long binary
        # Return of getrandbits(n) may not have matching number of digits for the same inputs
        # since significant bits could be randomized to 0
        found_p = False
        found_q = False
        p = getrandbits(p_size)
        while(not found_p):
            if isPrime(p):
                found_p = True
            else:
                p = getrandbits(p_size)
                
        q = getrandbits(q_size)
        while(not found_q):
            if isPrime(q):
                found_q = True
            else:
                q = getrandbits(q_size)
    else:
        print("Bit lengths must be >= 32")
        usage()
        exit(1)

    fout = open("out.txt", "w")
    fout.write("p = " + str(p) + "\n")
    fout.write("q = " + str(q) + "\n")
    N = p*q
    fout.write("N = " + str(N) + "\n")
    m = (p - 1)*(q - 1) # Euler's totient calculation
    e = createEVal(m)
    fout.write("e = " + str(e) + "\n")
    d = extendedGCD(m, e)
    fout.write("d = " + str(d) + "\n")

def usage():
    print("Usage:\n\tt3.py n1 n2\n\tWhere n1 = p bit length and n2 = q bit length")

def isPrime(val):
    # Deterministic since relatively small values.
    # May take time for very large values.
    prime = True
    for i in range(2, int(sqrt(val))):
        if (val % i) == 0:
            prime = False

    return prime

def gcd(n1, n2):
   while n2 != 0:
       n1, n2 = (n2), (n1 % n2)
  
   return n1

def createEVal(m):
    e = randint(1, m-1)
    while gcd(e, m) != 1:
        e = randint(1, m-1)
    
    return e

def extendedGCD(n1, n2):
    # Inverse of n2 mod n1
    done = False
    a1 = 1
    b1 = 0
    a2 = 0
    b2 = 1
    while not done:
        q = int(n1 / n2)
        r = n1 % n2
        if r == 0:
            done = True
        else:
            n1 = n2
            n2 = r
            t = a2
            a2 = a1 - (q * a2)
            a1 = t
            t = b2
            b2 = b1 - (q * b2)
            b1 = t
    
    b = b2
    print(b)

    return b 

if __name__ == '__main__':
    main()