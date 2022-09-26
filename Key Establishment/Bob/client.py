import hashlib
import random
import socket
import sys

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

# Turn on for Debugging messages
debug = False

IP = '127.0.0.1'
PORT = 9999

# Bob's password is hardcoded. This was done to save time as password setting functionality
# is not worth any marks.
bob_pass = "abcd"

def main():
    NB = str(hex(random.getrandbits(128)))
    K = str(hex(random.getrandbits(128)))
    NA = ''
    hostname = ''

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # User setup
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    
    # First message to Alice
    if debug: print(f"[*] NB: {NB}") # DEBUGGING STATEMENT
    init_message = f"{username}, {NB}"
    client.sendto(bytes(init_message, "utf-8"), (IP, PORT))

    # First message from Alice
    message, address = client.recvfrom(4096)
    if message == b'Connection Failed': # Close if 'Connection Failed recieved'
        print("[*] Connection attempt failed. Exiting...")
        client.close()
        sys.exit(1)
    if debug: print(f"[*] Message: {message}") # DEBUGGING STATEMENT
    message_contents = message.decode().split(", ")
    hostname = message_contents[0] # This doesnt really matter but I might as well set the hostname since I have it
    
    # Verify Alice's public key with stored fingerprint
    if hashlib.sha1(message_contents[1].encode()).hexdigest() != (open("fingerprint", "r").read()):
        print("\nFingerprint does not match. Connection failed.")
        client.close()
        sys.exit(1)

    public_key = RSA.import_key(message_contents[1])
    NA = message_contents[2]

    # Last message to Alice
    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrytiontext = password + ", " + K
    C1 = cipher_rsa.encrypt(bytes(encrytiontext, "utf-8"))
    client.sendto(C1, (IP, PORT))

    # Last message from Alice
    message, address = client.recvfrom(4096)
    if message == b'Connection Failed': # Close if 'Connection Failed recieved'
        if debug: print("[*] Log: Connection attempt failed. Exiting...")
        client.close()
        sys.exit(1)
    if debug: print(f"[*] Message: {message}") # DEBUGGING STATEMENT

    if message == b'Connection Failed':
        if debug: print("[*] Log: Connection attempt failed. Exiting...")
        client.close()
        sys.exit(1)
    else:
        print("[*] Connection attempt successful")
        if debug: print(f"\n[*] K: {str(K)}")
        if debug: print(f"[*] NA: {str(NA)}")
        if debug: print(f"[*] NB: {str(NB)}\n")
        ssk = hashlib.sha1((f"{K},{NB},{NA}").encode()).hexdigest()

        if debug: print(f"SSK: {ssk}")

    client.close()

if __name__ == '__main__':
    main()
