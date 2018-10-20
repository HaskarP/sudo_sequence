import os

class Record:
    def __init__(self, day, qname, flags, rname, mapq, cigar, seq, qual):
        self.day = day
        self.qname = qname
        self.flags = flags
        self.rname = rname
        self.mapq = mapq
        self.cigar = cigar
        self.seq = seq
        self.qual = qual
    
    def write(self, patch_file):
        patch_file.write(int(self.timestamp))
        patch_file.write(str(self.qname))
        patch_file.write(int(self.flags))
        patch_file.write(str(self.rname))
        patch_file.write(int(self.mapq))
        patch_file.write(str(self.cigar))
        patch_file.write(str(self.seq))
        patch_file.write(str(self.qual))

class Patch:
    def __init__(self, metric, records):
        self.metric = metric
        self.records = records

    def write(self, patch_file, index_file):
        index = os.fstat(path_file.fileno()).st_size 

        index_file.write(int(self.metric))
        index_file.write(int(index))

        for record in self.records:
            record.write(patch_file)

class Daru:
    def __init__(self, patchsize, days, patches):
        self.patchsize = patchsize
        self.days = days
        self.patches = patches

    def write(self, patch_filename, index_filename):
        patch_file = open(patch_filename, "wb")
        index_file = open(index_filename, "wb")
        
        patch_file.write(int(patchsize))
        patch_file.write(int(days))
        for patch in self.patches:
            patch.write(patch_file, index_file)
