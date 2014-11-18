from zlib import compress as zlibcompress
from zlib import decompress as zlibuncompress

# This module handles the data compression of the objects stored in the blockchain.
# Currently we just delegate to zlib, but have wrapped with these methods as we may
# wish to change the compression backend, or add some metrics / instrumentation / config here

def compress(data):
    return zlibcompress(data)


def decompress(data):
    return zlibuncompress(data)