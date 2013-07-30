class ARC4:
    """ ARC4 Stream Cipher Algorithm
    """
    def __init__(self,key=None):
        """ key -> octet string for key """
        self.name        = 'ARC4'
        self.strength    = None # depends on keySize
        self.blockSize   = 1    # blockSize is in bytes

        if key != None:
            self.setKey(key)

    def setKey(self, key):
        """ Set initial state from key. Never use the same key more than once!
        """
        self.keySize     = len(key)
        self.strength    = self.keySize  # this does not include subtracting IV size :-(
        i, j, self.state = 0, 0, range(256)
        for i in range(256):
            j = (j + self.state[i] + ord(key[i % len(key)])) % 256
            self.state[i], self.state[j] = self.state[j], self.state[i]
        self.keyReady = 1 # Ready

    def encrypt(self, plainText, more = None):
        """ Encrypt a string and return a binary string
            multiple sequential calls can be made using more =1,
            this continues the encryption
            New sessions of encrypt can NOT be called twice with the same key!!!!
        """
        if self.keyReady != 1 : raise 'Error, ARC4 key already used once!'
        if more != 1:
            self.keyReady = None
        cipherText = arcfourBlock(self.state, plainText)
        return cipherText


    def decrypt(self, cipherText, more = None):
        """ Decrypt a string and return a string """
        if self.keyReady != 1 :
            raise 'set for decryption required'
        if more != 1:
            self.keyReady = None
        plainText = arcfourBlock(self.state, cipherText)
        return plainText


def arcfourBlock(state, input):
    """ Use state to encrypt input string, returns string """
    i, j, output = 0, 0, []
    for byte in input:
        i = (i + 1) % 256
        j = (j + state[i]) % 256
        state[i], state[j] = state[j], state[i]
        n = (state[i] + state[j]) % 256
        output.append(chr(ord(byte) ^ state[n]))
    output = ''.join(output) # convert to string
    return output
