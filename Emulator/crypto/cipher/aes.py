from crypto.cipher.rijndael import Rijndael
from crypto.cipher.base     import BlockCipher, padWithPadLen, noPadding
from crypto.errors          import BadKeySizeError

class AES(Rijndael):
    """ The AES algorithm is the Rijndael block cipher restricted to block
        sizes of 128 bits and key sizes of 128, 192 or 256 bits
    """
    def __init__(self, key = None, padding = padWithPadLen(), keySize=16):
        """ Initialize AES, keySize is in bytes """
        if  not (keySize == 16 or keySize == 24 or keySize == 32) :
            raise BadKeySizeError, 'Illegal AES key size, must be 16, 24, or 32 bytes'

        Rijndael.__init__( self, key, padding=padding, keySize=keySize, blockSize=16 )

        self.name       = 'AES'




