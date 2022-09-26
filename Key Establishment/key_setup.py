import os
import hashlib

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

def main():
    setUpRSA()

def setUpRSA():
    RSAkey = RSA.generate(2048)
    private_key = RSAkey.export_key()
    public_key = RSAkey.public_key().export_key()

    fout = open("Alice/private.pem", "wb")
    fout.write(private_key)
    fout.close()

    fout = open("Alice/public.pem", "wb")
    fout_bob = open("Bob/fingerprint", "w")
    fout.write(public_key)
    fout_bob.write(hashlib.sha1(public_key).hexdigest())
    fout_bob.close()
    fout.close()

def checkPrevRSA():
    path = os.getcwd()
    skfile = path + "Alice/private.pem"
    pkfile = path + "Alice/public.pem"

    return (os.path.isfile(skfile) and os.path.isfile(pkfile))

if __name__ == '__main__':
    main()