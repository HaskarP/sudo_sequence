class Record:
    def __init__(self, ident, seq, desc=""):
        self.identifier = ident
        self.sequence = seq
        self.description = desc

    def __repr__(self):
        bases = ""
        qualities = ""
        for (base, quality) in self.sequence:
            bases = bases + base
            qualities = qualities + str(chr(quality))
        return ("@" 
                + self.identifier 
                + " " 
                + self.description 
                + "\n" 
                + bases
                + "\n"
                + "+\n"
                + qualities)

class Fastq:
    def __init__(self, records=[]):
        self.records = records

    def __repr__(self):
        return self.records.__repr__()

def read_fastq(filename):
    input_file = open(filename, "r")
    lines = input_file.readlines()

    records = []

    while lines:
        header = lines[0][:-1]
        bases = lines[1][:-1]
        qualities = lines[3][:-1]
        del lines[:4]

        if not header.startswith('@'):
            raise ValueError("'" + header + "' is not a valid sequence header")
        
        processed_header = header[1:].split(' ', 1)
        ident = processed_header[0]
        desc = ""
        if len(processed_header) > 1: 
            desc = processed_header[1]

        if len(bases) != len(qualities):
            raise ValueError("The number of bases should be the same as the number of qualities")

        seq = []
        for (base, quality) in zip(list(bases), (list(qualities))):
            if base.upper() not in ['A', 'C', 'T', 'G']:
                raise ValueError("'" + sequence + "' is not a valid sequence")
            seq.append((base.upper(), ord(quality)))

        record = Record(ident, seq, desc)
        print(record)
        records.append(record)

    return Fastq(records)
