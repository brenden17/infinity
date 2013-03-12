from collections import defaultdict

import numpy as np

import pandas as pd

def fetch_file(label='', trace=True):
    def onDecorator(func):
        def onCall(*args, **kwargs):
            result = func(*args, **kwargs)
            if trace:
                format = '%s%s: %.5f'
                values = (label, func.__name__, elapsed)
                print(format % values)
            return result
        return onCall
    return onDecorator

def counting_DNA_Nucleotide(dnastring):
    '''http://rosalind.info/problems/dna/'''
    d = defaultdict(int)
    for c in dnastring:
        d[c] += 1
    print '%d %d %d %d' % (d['A'], d['C'], d['G'], d['T'])
    return d

def transcribing_DNA_into_RNA(dnastring):
    l = []
    for n in dnastring:
        if n == 'T':
            l.append('U')
        else:
            l.append(n)
    print ''.join(l)

def complementing_a_strand_of_DNA(dnastring):
    '''http://rosalind.info/problems/revc/'''
    complement = {'A':'T', 'G':'C', 'C':'G', 'T':'A'}
    print ''.join([complement.get(n, n) for n in dnastring])[::-1]

def rabbits_and_recurrence_relations(n, k):
    '''http://rosalind.info/problems/fib/'''
    ADULT, CHILD = 0, 1
    RATE = k
    d = np.zeros((2, 40))
    d[ADULT, 0], d[CHILD, 0] = 0, 1
    d[ADULT, 1], d[CHILD, 1] = 1, 0

    for i in xrange(2, n):
        d[ADULT, i] = d[ADULT, i-1] + d[CHILD, i-1]
        d[CHILD, i] = d[ADULT, i-1] * RATE

    print d[ADULT, n-1] + d[CHILD, n-1]

def computing_GC_content(dnastring):
    d = counting_DNA_Nucleotide(dnastring)
    ratio = float(d['C'] + d['G']) / float(d['C'] + d['G'] + d['A'] + d['T'])
    print ratio * 100

def counting_point_mutation(s, t):
    '''http://rosalind.info/problems/hamm/'''
    assert(len(s) == len(t))
    print len([1 for i, n in enumerate(s) if t[i]!=n]) 

def protein_translation(dnastring):
    '''http://rosalind.info/problems/prot'''
    CODON = {
                'UUU':'F',
                'UUC':'F',
                'UUA':'L',
                'UUG':'L',
            }
    l = len(dnastring) / 3
    protine = [CODON.get(dnastring[s*3:s*3+3], '') for s in xrange(l)]
    print ''.join(protine)

def finding_a_motif_in_DNA(sd, td):
    '''http://rosalind.info/problems/subs'''
    tdl = len(td)
    print [i+1 for i, n in enumerate(sd) if sd[i:i+tdl] == td]

def consensus_and_profile(dnastrings):
    '''http://rosalind.info/problems/cons'''
    l = [[c for c in s] for s in dnastrings]
    raw = pd.DataFrame(l)

    col = len(dnastrings[0])
    index = ['A', 'C', 'G', 'T']
    profile = pd.DataFrame(np.random.randn(4, col),
                            index=index,
                            columns=range(col))
    for i in xrange(col):
        counter = raw[i].value_counts()
        profile[i]=[counter.get(c, 0) for c in index]

    print ''.join(profile.idxmax(axis=0).values)
    print profile

def mortal_fibonacci_rabbits(n, m):
    '''http://rosalind.info/problems/fibd/'''
    ADULT, CHILD = 0, 1
    d = np.zeros((2, n))
    d[ADULT, 0], d[CHILD, 0] = 0, 1
    d[ADULT, 1], d[CHILD, 1] = 1, 0

    for i in xrange(2, n):
        k = 0 if i-m < 0 else d[CHILD, i-m]
        d[ADULT, i] = d[ADULT, i-1] + d[CHILD, i-1] - k
        d[CHILD, i] = d[ADULT, i-1]

    print d[ADULT, n-1] + d[CHILD, n-1]


if __name__ == '__main__':
    counting_DNA_Nucleotide('AGCTTTTCATTCTGACTGCAACGGGCAATATGTCTCTGTGTGGATTAAAAAAAGAGTGTCTGATAGCAGC')
    counting_point_mutation('GAGCCTACTAACGGGAT', 'CATCGTAATGACGGCCT')
    transcribing_DNA_into_RNA('GATGGAACTTGACTACGTAAATT')
    complementing_a_strand_of_DNA('AAAACCCGGT')
    rabbits_and_recurrence_relations(5, 3)
    computing_GC_content('AGCTATAG')
    protein_translation('UUUUUCUUA')
    finding_a_motif_in_DNA('GATATATGCATATACTT', 'ATAT')
    consensus_and_profile(['ATCCAGCT', 'GGGCAACT', 'ATGGATCT', 'AAGCAACC',
'TTGGAACT', 'ATGCCATT', 'ATGGCACT'])
    mortal_fibonacci_rabbits(6, 3)
