This program generates the perameters necessary to do RSA encryption and decryption.
It was created as a solution to a university assignment.

Usage:
	python3 generator.py n1 n2
		where: 
			n1 = p bit length
			n2 = q bit length

The parameters created include two primes (p and q) of any given length >= 32 bits, a Euler's totient
value, an N value (to use for encryption/decryption) along with the encryption (E) and decryption (D) keys.
They would be used like so: (^ denotes exponent)

	Encryption:
		C = M^E mod N
			where: 
				C -> ciphertext
				M -> plaintext message
				E -> encryption key
				N -> N value generated

	Decryption:
		M = C^D mod N
			where:
				M -> plaintext message
				C -> ciphertext
				D -> decryption key
				N -> N value generated

Important notes:
1 - This does actually work. It has been tested and it CAN encrypt and decrypt messages. However, the ability to do
so, has not been added into the program (since it wasn't worth any marks) and since the generation of primes has not 
been optimized (see below); this program can only practically generate keys that are well below the minimum 2048 bits 
of RSA. This means that this program should never be used for any real security purpose.
2 - The method used to test primality in this program is wildly inefficient and was chosen solely because 
it's optimization was not worth any marks. I may at some point do a similar project to this one where I use
a Miller-Rabin primality test instead as well as add the option to encrypt and decrypt files from within the
program.
