

def read_FASTA_strings(filename):
    with open(filename) as f:
        return f.read().split('>')[1:]



