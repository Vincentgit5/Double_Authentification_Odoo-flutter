import math
from random import random, randrange, getrandbits, randint

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

from sympy import mod_inverse


# function that generates public and private keys
def generate_key_pair():
    p = randint(9999999999, 99999999999999999)
    q = randint(378945699, 9999999999999)
    return generate_keypair(p, q)


# parameters of the function that generates keys
def generate_keypair(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    e = randint(588888899, 11111118555)
    while math.gcd(e, phi) != 1:
        e = randrange(1, phi)
    d = mod_inverse(e, phi)
    return ((e, n), (d, n))


# function that generates an automatic number for each user

def generate_number():
    number = randint(0, 99999)
    return number


# function that randomly generates a series of 5 digits and checks whether the number already exists

def generer_numero(liste_numeros):
    numero = ""
    for i in range(5):
        numero += str(random.randint(0, 99999))
    if numero in liste_numeros:
        return generer_numero(liste_numeros)
    else:
        return numero


def encrypt(public_key_str, plaintext):
    public_key_bytes = bytes.fromhex(public_key_str)
    public_key = serialization.load_der_public_key(public_key_bytes, backend=default_backend())
    ciphertext = public_key.encrypt(plaintext.encode(), padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None))

    return ciphertext.hex()
