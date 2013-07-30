from crypto.entropy.prn_rijndael import PRN_Rijndael
from binascii import b2a_hex

""" Not much of a test yet .... """

if __name__ == "__main__":
    r = PRN_Rijndael()
    for i in range(20):
        print b2a_hex(r.getSomeBytes())
    for i in range (20):
        r.getBytes(i)
    for i in range(40):
        c=r.getBytes(i)
        print b2a_hex(r.getBytes(i))
        r.reseed(c)







