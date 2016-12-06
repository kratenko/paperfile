"""
Created on Dec 5, 2016

@author: kratenko@garstig.org
"""

import hashlib
import random
import struct
import math

with open('gpl-3.0.txt', 'rb') as f:
    data = f.read()

data = data[:4096]


class Dumper(object):
    VERSION = 1
    BUNCH_SIZE = 250

    def __init__(self, data):
        self.random_id = random.randint(0, 0xffff)
        self.data = data
        self.data_len = len(data)
        self.data_hash = hashlib.sha1(self.data).digest()
        self.bunch_size = self.BUNCH_SIZE
        self.bunch_count = int(math.ceil(self.data_len / self.bunch_size))

    def header(self, bunch_number):
        return struct.pack(">ccBHB", b'p', b'f', self.VERSION, self.random_id, bunch_number)

    def gen_bunches(self):
        b0 = self.header(0)
        b0 += struct.pack(">HB", self.data_len, self.bunch_count)
        b0 += self.data_hash
        bunches = [b0]
        for n in range(self.bunch_count):
            bunch = self.header(n + 1)
            bunch += self.data[n * self.bunch_size:(n + 1) * self.bunch_size]
            bunches.append(bunch)
        return bunches


class Loader(object):

    def __init__(self, bunches):
        pass


def load(parts):
    sorted_parts = {}
    for part in parts:
        n = part[5]
        assert n not in sorted_parts
        sorted_parts[n] = part
    assert 0 in sorted_parts
    p0 = sorted_parts[0]
    h1 = p0[9:50]
    part_counts = p0[8]
    data = b''
    for n in range(1, part_counts + 1):
        part = sorted_parts[n]
        data += part[6:]
    h2 = hashlib.sha1(data).digest()
    print(len(data), h1, h2)
    return data
#h = hashlib.sha1(data)
#print(len(data), len(data) / 250)

pf = Dumper(data)
bunches = pf.gen_bunches()
for b in bunches:
    print(b)
out = load(bunches)
print(data == out)

import qrcode

img = qrcode.make(bunches[1], border=0, box_size=4)

img.show()
