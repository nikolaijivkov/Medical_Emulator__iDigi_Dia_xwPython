def xorS(a,b):
    """ XOR two strings """
    assert len(a)==len(b)
    x = []
    for i in range(len(a)):
            x.append( chr(ord(a[i])^ord(b[i])))
    return ''.join(x)
      
def xor(a,b):
    """ XOR two strings """
    x = []
    for i in range(min(len(a),len(b))):
            x.append( chr(ord(a[i])^ord(b[i])))
    return ''.join(x)
