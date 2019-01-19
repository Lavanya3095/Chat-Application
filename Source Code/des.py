import sys
import chilkat
import random
from diffie_hellman import rand
crypt = chilkat.CkCrypt2()

success = crypt.UnlockComponent("Anything for 30-day trial")

rand(1, 128, 24)


def des_enc(msg, keyHex):

    #  Specify 3DES for the encryption algorithm:
    crypt.put_CryptAlgorithm("3des")

    #  CipherMode may be "ecb" or "cbc"
    crypt.put_CipherMode("cbc")

    #  KeyLength must be 192.  3DES is technically 168-bits;
    #  the most-significant bit of each key byte is a parity bit,
    #  so we must indicate a KeyLength of 192, which includes
    #  the parity bits.
    #crypt.put_KeyLength(192)

    #  The padding scheme determines the contents of the bytes
    #  that are added to pad the result to a multiple of the
    #  encryption algorithm's block size.  3DES has a block
    #  size of 8 bytes, so encrypted output is always
    #  a multiple of 8.
    crypt.put_PaddingScheme(0)

    #  EncodingMode specifies the encoding of the output for
    #  encryption, and the input for decryption.
    #  It may be "hex", "url", "base64", or "quoted-printable".
    crypt.put_EncodingMode("hex")

    #  An initialization vector is required if using CBC or CFB modes.
    #  ECB mode does not use an IV.
    #  The length of the IV is equal to the algorithm's block size.
    #  It is NOT equal to the length of the key.
    ivHex = "0001020304050607"
    crypt.SetEncodedIV(ivHex, "hex")
    crypt.SetEncodedKey(keyHex, "hex")
    encStr = crypt.encryptStringENC(msg)
    return encStr


def des_dec(msg,keyHex):
    #  Now decrypt:
    crypt.put_CryptAlgorithm("3des")
    crypt.put_CipherMode("cbc")
    crypt.put_PaddingScheme(0)
    crypt.put_EncodingMode("hex")
    ivHex = "0001020304050607"
    crypt.SetEncodedIV(ivHex, "hex")
    crypt.SetEncodedKey(keyHex, "hex")
    decStr = crypt.decryptStringENC(msg)
    return decStr
