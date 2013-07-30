from crypto.cipher.aes  import AES
from crypto.cipher.base import padWithPadLen
from binascii           import a2b_hex, b2a_hex, hexlify, unhexlify

key = '%016x' % 0x1234
kSize = len(key)

data = 'Data goes here! Is that a surprize?'

alg = AES(key, keySize=kSize, padding=padWithPadLen())

enc_data=alg.encrypt(data)
dec_data=alg.decrypt(enc_data)
