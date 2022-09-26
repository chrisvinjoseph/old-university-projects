import hashlib
import random
import socket

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

# Note: I have included very little validation outside of assignment requirements
# i.e. The program assumes that all input from the client will be correct
# I did this because I felt that extra validation wasn't necessary to demonstrate the functionality of the assignment
# and it's necessity was not mentioned in the assignment spec

# Turn on for Debugging messages
debug = False

IP = '127.0.0.1'
PORT = 9999
ssk = ''

def main():
    NB = ''
    NA = str(hex(random.getrandbits(128)))
    username, password = open('passfile', 'r').read().split(", ") # Only supports 1 user (Bob) at this point since more users are not required
    password = password[0:-1] # Strip newline character from string

    host = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host.bind((IP, PORT))

    pk = open('public.pem').read()

    # First message from Bob
    while True:
        print(f"[*] Listening on port {PORT}...")
        message, address = host.recvfrom(1024)
        if debug: print(f"[*] Message: {message}") # DEBUGGING STATEMENT
        initial_arguments = message.decode().split(", ") # Assuming that no validation is necessary that arguments are correct
        if initial_arguments[0] == username:
            NB = initial_arguments[1]

            # First message to Bob
            return_msg = f"Alice, {pk}, {NA}"
            host.sendto(bytes(return_msg, 'utf-8'), address)

            # Last message from Bob
            message, address = host.recvfrom(1024)
            if debug: print(f"[*] Message: {message}") # DEBUGGING STATEMENT
            ciphertext = message

            # Decrypt ciphertext
            private_key = RSA.import_key(open("private.pem").read())
            cipher_rsa = PKCS1_OAEP.new(private_key)
            decrypted_message = cipher_rsa.decrypt(ciphertext)

            # Authenticate Bob
            if debug: print(f"[*] Decrypted Message: {decrypted_message.decode('utf-8')}") # DEBUGGING STATEMENT
            PW, K = decrypted_message.decode('utf-8').split(", ")
            encoded_PW = PW.encode()
            if debug: print(f"[*] Recieved Password: {PW}") # DEBUGGING STATEMENT
            hex_PW = hashlib.sha1(encoded_PW).hexdigest()
            status = ''
            if str(hex_PW) == password:
                status = "Okay"
                print(f"[*] Connection accepted from {address[0]}:{address[1]}")
            else:
                status = "Failed"
                print(f"[*] Connection refused from {address[0]}:{address[1]}")

            return_msg = f'Connection {status}'
            if debug: print(f"[*] Return message: {return_msg}\n")

            # Last message to Bob
            host.sendto(bytes(return_msg, 'utf-8'), address)

            if return_msg == 'Connection Okay':
                if debug: print(f"\n[*] K: {str(K)}")
                if debug: print(f"[*] NA: {str(NA)}")
                if debug: print(f"[*] NB: {str(NB)}\n")
                ssk = hashlib.sha1((f"{K},{NB},{NA}").encode()).hexdigest()

                if debug: print(f"SSK: {ssk}")
                break
        else:
            host.sendto(b'Connection Failed', address)
            print(f"[*] Connection refused from {address[0]}:{address[1]}")

if __name__ == '__main__':
    main()
