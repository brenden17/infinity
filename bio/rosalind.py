from collections import defaultdict

def counting_DNA_Nucleotide():
    dataset = 'AGCTTTTCATTCTGACTGCAACGGGCAATATGTCTCTGTGTGGATTAAAAAAAGAGTGTCTGATAGCAGC'
    d = defaultdict(int)
    for c in dataset:
        d[c] += 1

    print d

def counting_point_mutation(s, t):
    """http://rosalind.info/problems/hamm/"""
    assert(len(s) == len(t))
    l = len(s)
    count = 0
    for i in xrange(l):
        if s[i] != t[i]:
            count += 1
    print count

if __name__ == '__main__':
#    counting_DNA_Nucleotide()
    counting_point_mutation('GAGCCTACTAACGGGAT', 'CATCGTAATGACGGCCT')
