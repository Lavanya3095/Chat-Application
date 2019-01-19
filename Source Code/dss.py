from Crypto.PublicKey import DSA
from Crypto.Signature import DSS
from Crypto.Hash import SHA256
hash_obj = ""
publickey = ""


def DSS_sign(message):
    key = DSA.generate(2048)
    publickey = key.publickey()
    hash_obj = SHA256.new(message)
    signer = DSS.new(key, 'fips-186-3')
    signature = signer.sign(hash_obj)
    print(hash_obj.hexdigest())


def DSS_verify(signature, message, h):
    hash_obj = SHA256.new(message)
    pkey = DSS.new(publickey, 'fips-186-3')
    if h == hash_obj.hexdigest():
        try:
            pkey.verify(hash_obj, signature)
            valid = True
        except ValueError:
            valid = False
        return valid
