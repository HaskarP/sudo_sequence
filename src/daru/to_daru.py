import pysam
import os
from daru import *
from more_itertools import peekable
from functools import reduce
import operator
import numpy

def records_in_patch(i, patch_start, patch_size, read_iterator):
    records = []
    while True:
        try:
            read = read_iterator.peek()

            pos_left = read.reference_start
            pos_right = pos_left + read.query_length

            if (pos_right < patch_start or read.reference_start == 0):
                read_iterator.next()
                continue
            if (pos_left > patch_start + patch_size):
                break

            read_iterator.next()
            rec = Record(i, read.query_name, read.flag, read.query_name, 
                read.reference_start, read.mapping_quality, 
                read.cigarstring, read.query_sequence, ''.join(list(map(lambda x: chr(x), read.query_qualities))))
            records.append(rec)
        except StopIteration:
            break
    return records

def find_score(records):
    counts = {}
    for r in records:
        if r.day in counts:
            counts.update({r.day: counts.get(r.day) + 1})
        else:
            counts.update({r.day: 1})

    count_values = list(counts.values())

    variance = numpy.var(count_values)

    return int(variance)

def to_daru(bam_files, daru_filename, index_filename, patch_size):
    read_iterators = list(map(lambda x: peekable(pysam.AlignmentFile(x, "rb").fetch()), bam_files))

    patches = []
    patch_base = int(min(map(lambda x: x.peek().reference_start, read_iterators)) / patch_size) * patch_size

    while True:
        records = []
        for (i, read_iterator) in zip(range(0, len(read_iterators)), read_iterators):
            records.extend(records_in_patch(i, patch_base, patch_size, read_iterator))
       
        print(patch_base, len(records))
        if len(records) != 0:
            score = find_score(records)
            patch = Patch(score, records)
            patches.append(patch)

        try: 
            patch_base = int(min(map(lambda x: x.peek().reference_start, read_iterators)) / patch_size) * patch_size
        except ValueError:
            break

    daru = Daru(patch_size, len(bam_files), patches)
    daru.write(daru_filename, index_filename)

# to_daru(["./data/M229_Control.bam", "./data/M229_Day3.bam", "./data/M229_Day21.bam", "./data/M229_Day90.bam"], "daru.daru", "daru.idaru", 250)
