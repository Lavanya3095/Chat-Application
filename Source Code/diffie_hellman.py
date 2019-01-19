from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import dh
from binascii import hexlify
from dss import DSS_sign
from Crypto.PublicKey import DSA
from Crypto.Signature import DSS
from Crypto.Hash import SHA256
import random


a_private_key = ""
b_private_key = ""
a_peer_public_key = ""
b_peer_public_key = ""
perm = []


def rand(start, end, num):
    for j in range(num):
        perm.append(random.randint(start, end))


def DSS_sign(c):
    key = DSA.generate(2048)
    global public_key
    public_key = key.publickey()
    if c == "a":
        hash_obj = SHA256.new(a_peer_public_key)
    else:
        hash_obj = SHA256.new(b_peer_public_key)
    signer = DSS.new(key, 'fips-186-3')
    signature = signer.sign(hash_obj)
    global s
    s = signer.sign(hash_obj)
    return hash_obj.hexdigest(), signature


def DSS_verify(c, h, signature):
    if c == "a":
        hash_obj = SHA256.new(a_peer_public_key)
    else:
        hash_obj = SHA256.new(b_peer_public_key)
    pkey = DSS.new(public_key, 'fips-186-3')
    signature = s
    if h == hash_obj.hexdigest():
        try:
            pkey.verify(hash_obj, signature)
            valid = True
        except ValueError:
            valid = False
        return valid


def diffie_alice_public():
    parameters = dh.generate_parameters(generator=2, key_size=512, backend=default_backend())
    global a_private_key
    a_private_key = parameters.generate_private_key()
    global ap
    ap = a_private_key
    a_peer_public_key = a_private_key.public_key()
    global a
    a = a_peer_public_key
    hash_value, alice_sign = DSS_sign("a")
    return hash_value, alice_sign


def shared_key():
    a_shared_key = ap.exchange(b)
    key = hexlify(a_shared_key).decode()
    final_key = ""
    for i in perm:
        final_key += key[i]
    return final_key


def diffie_bob_public():
    parameters = dh.generate_parameters(generator=2, key_size=512, backend=default_backend())
    global b_private_key
    b_private_key = parameters.generate_private_key()
    global bp
    bp = b_private_key
    b_peer_public_key = b_private_key.public_key()
    global b
    b = b_peer_public_key
    hash_value, bob_sign = DSS_sign("b")
    return hash_value, bob_sign
