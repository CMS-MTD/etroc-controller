def add_binary(a, b, shift=8):
    return a<<shift | b

def get_binary_string(a, nBits=8):
    return "{0:{fill}{nBits}b}".format(a, nBits=nBits, fill='0')

def set_bit(num, idx, value):
    if value == 1:
        return num | (  1 << idx)
    else:
        return num & (~(1 << idx))

def get_bit(num, idx):
    return int(num & (1 << idx) != 0)

