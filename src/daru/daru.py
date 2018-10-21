import struct
import os

class Record:
    def __init__(self, day, qname, flags, rname, pos, mapq, cigar, seq, qual):
        self.day = day
        self.qname = qname
        self.flags = flags
        self.rname = rname
        self.pos = pos
        self.mapq = mapq
        self.cigar = cigar
        self.seq = seq
        self.qual = qual
    
    def write(self, patch_file):
        patch_file.write(self.day.to_bytes(4, byteorder='big'))

        patch_file.write(bytes(self.qname, 'utf-8'))
        patch_file.write((0).to_bytes(1, byteorder='big'))

        patch_file.write(self.flags.to_bytes(4, byteorder='big'))

        patch_file.write(bytes(self.rname, 'utf-8'))
        patch_file.write((0).to_bytes(1, byteorder='big'))

        patch_file.write(self.pos.to_bytes(4, byteorder='big'))
        patch_file.write(self.mapq.to_bytes(4, byteorder='big'))

        patch_file.write(bytes(self.cigar, 'utf-8'))
        patch_file.write((0).to_bytes(1, byteorder='big'))

        patch_file.write(bytes(self.seq, 'utf-8'))
        patch_file.write((0).to_bytes(1, byteorder='big'))

        patch_file.write(bytes(self.qual, 'utf-8'))
        patch_file.write((0).to_bytes(1, byteorder='big'))

class Patch:
    def __init__(self, metric, records):
        self.metric = metric
        self.records = records

    def write(self, patch_file, index_file):
        index = patch_file.tell()

        index_file.write(self.metric.to_bytes(4, byteorder='big'))
        index_file.write(index.to_bytes(4, byteorder='big'))
        patch_file.write(len(self.records).to_bytes(4, byteorder='big'))

        for record in self.records:
            record.write(patch_file)

class Daru:
    def __init__(self, patch_size, days, patches):
        self.patch_size = patch_size
        self.days = days
        self.patches = patches

    def write(self, patch_filename, index_filename):
        patch_file = open(patch_filename, "wb")
        index_file = open(index_filename, "wb")
        
        patch_file.write(bytes([self.patch_size]))
        patch_file.write(bytes([self.days]))
        for patch in self.patches:
            patch.write(patch_file, index_file)

def read_string(patch_file):
    chars = []
    current = int.from_bytes(patch_file.read(1), byteorder='big')
    while current != 0:
        chars.append(chr(current))
        current = int.from_bytes(patch_file.read(1), byteorder='big')
    return "".join(chars)

def read_record(patch_file):
    day = int.from_bytes(patch_file.read(4), byteorder='big')
    qname = read_string(patch_file) 
    flags = int.from_bytes(patch_file.read(4), byteorder='big')
    rname = read_string(patch_file) 
    pos = int.from_bytes(patch_file.read(4), byteorder='big')
    mapq = int.from_bytes(patch_file.read(4), byteorder='big')
    cigar = read_string(patch_file) 
    seq = read_string(patch_file) 
    qual = read_string(patch_file)
    return Record(day, qname, flags, rname, pos, mapq, cigar, seq, qual)


def read_patch(patch_filename, byte_index):
    patch_file = open(patch_filename, "rb")
    patch_file.seek(byte_index)

    patch_size = int.from_bytes(patch_file.read(4), byteorder='big')
    records = []
    for i in range(0, patch_size):
        records.append(read_record(patch_file))

    return records

def read_index(index_filename):
    byte_count = os.path.getsize(index_filename)
    index_file = open(index_filename, "rb")

    indeces = {} 

    for i in range(0, int(byte_count / 8)):
        metric = int.from_bytes(index_file.read(4), byteorder='big')
        index = int.from_bytes(index_file.read(4), byteorder='big')
        indeces[index] = metric

    return indeces
