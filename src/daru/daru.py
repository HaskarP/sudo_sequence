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
        patch_file.write(self.flags.to_bytes(4, byteorder='big'))
        patch_file.write(bytes(self.rname, 'utf-8'))
        patch_file.write(self.pos.to_bytes(4, byteorder='big'))
        patch_file.write(self.mapq.to_bytes(4, byteorder='big'))
        patch_file.write(bytes(self.cigar, 'utf-8'))
        patch_file.write(bytes(self.seq, 'utf-8'))
        patch_file.write(bytes(self.qual, 'utf-8'))

class Patch:
    def __init__(self, metric, records):
        self.metric = metric
        self.records = records

    def write(self, patch_file, index_file):
        index = patch_file.tell()

        index_file.write(self.metric.to_bytes(4, byteorder='big'))
        index_file.write(index.to_bytes(4, byteorder='big'))

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
