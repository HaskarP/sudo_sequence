import pysam
import os
import numpy
from daru import *


def reads_in_patch(patch_start, patch_size, file_list):
	records = []
	for (i, file) in zip(range(0, len(file_list)), file_list):
		for read in file.fetch():
			pos_left = read.reference_start
			pos_right = pos_left + read.query_length
			if (pos_right < patch_start or read.reference_start == 0):
				continue
			if (pos_left > patch_start + patch_size):
				break
			rec = Record(i, read.query_name, read.flag, read.query_name, 
				read.reference_start, read.mapping_quality, 
				read.cigar, read.query_sequence, read.query_qualities)
			records.append(rec)
	return records


def find_score(records):
	
	return 76



PATCH_SIZE = 250

all_reads = []

folder = "./bam/"

list_of_files_per_person = os.listdir(folder)
list_of_files_per_person =  list(filter(lambda x : x.endswith(".bam"), list_of_files_per_person))

file_prefix = list(set(map(lambda x : x[:4],list_of_files_per_person)))[0]



filename_list = list(filter(lambda x : x.startswith(file_prefix),list_of_files_per_person))

file_list = [pysam.AlignmentFile(folder+name_of_file, "rb") for name_of_file in filename_list]

print(file_prefix, filename_list)
print()	

# file_lengths = [sum(file.lengths) for file in file_list]
# max_file_length = max(file_lengths)

patches = []

i = 0
while True : 
	#print(i*PATCH_SIZE, max_file_length)
	record = reads_in_patch(i * PATCH_SIZE, PATCH_SIZE, file_list)
	if len(record) == 0:
		continue
	score = find_score(record)
	patch = Patch(score, record)
	patches.append(patch)

	i += PATCH_SIZE

daru = Daru(PATCH_SIZE, len(file_list), patches)

daru.write("daru.daru", "index.idaru")