from crypto.cipher.aes  import AES
from crypto.cipher.cbc  import CBC
from crypto.cipher.base import BlockCipher, padWithPadLen, noPadding

class AES_CBC(CBC):
    """ AES encryption in CBC feedback mode """
    def __init__(self, key=None, padding=padWithPadLen(), keySize=16):
        CBC.__init__( self, AES(key, noPadding(), keySize), padding)
        self.name       = 'AES_CBC'

