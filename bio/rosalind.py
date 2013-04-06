from collections import defaultdict

import numpy as np

import pandas as pd

from Bio.Seq import Seq
from Bio import SeqIO

def read_file(filename='',fmt=''):
    def decorator(func):
        def call(*args, **kwargs):
            handle = open(filename)
            record_iterator = SeqIO.parse(handle, fmt)
            for record in record_iterator:
                result = func(record, *args, **kwargs)
            return result
        return call
    return decorator

def counting_DNA_Nucleotide(dnastring):
    '''http://rosalind.info/problems/dna/'''
    #method 1
    d = defaultdict(int)
    for c in dnastring:
        d[c] += 1
    print '%d %d %d %d' % (d['A'], d['C'], d['G'], d['T'])
    return d
    #method2 using biopython
    s = Seq(dnastring)
    d = {n: s.count(n) for n in 'ACGT'}
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
    #method1
    d = counting_DNA_Nucleotide(dnastring)
    ratio = (float(d['C'] + d['G']) / float(d['C'] + d['G'] + d['A'] + d['T'])) * 100
    print ratio

    #method2
    from Bio.SeqUtils import GC
    print GC(Seq(dnastring))

def counting_point_mutation(s, t):
    '''http://rosalind.info/problems/hamm/'''
    assert(len(s) == len(t))
    print len([1 for i, n in enumerate(s) if t[i]!=n]) 

def protein_translation(dnastring):
    '''http://rosalind.info/problems/prot'''
    #methon1
    CODON = {
                'UUU':'F',
                'UUC':'F',
                'UUA':'L',
                'UUG':'L',
            }
    l = len(dnastring) / 3
    protine = [CODON.get(dnastring[s*3:s*3+3], '') for s in xrange(l)]
    print ''.join(protine)
    #methond2
    s = Seq(dnastring)
    print s.translate()

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

def a_brief_introduction_to_graph_theory(labels, dnastrings, k):
    '''http://rosalind.info/problems/grph/'''
    l1 = [s[0:k] for s in dnastrings]
    l2 = [s[-k::] for s in dnastrings]
    d = {0:l1, 1:l2}
    p = pd.DataFrame(d, index=labels)
    l = list()
    for i in range(len(labels)):
        ll = [(labels[i], s) for s in p[p[0]==p[1][i]].index.tolist() if
s!=labels[i]]
        if ll:
            l.extend(ll)
    print l

#def finding_a_shared_motif(dnastrings):
#    for i, s1 in enumerate(dnastrings):
#        for s2 in dnastrings[i+1::]
#            pass

def find_pos(seq, sub, start=0, end=2147483647):
    post = list()
    new_start, end = start, end
    while True:
        seq.find(sub, new_start, end)
        if new_start < 0:
            break
        pos.append(new_start)
        new_start += 1

class ExtendSeq(Seq):
    def _find_pos(self, sub, start=0, end=2147483647):
        pos = list()
        new_start = start
        while True:
            new_start = self.find(sub, new_start, end)
            if new_start < 0:
                break
            #    yield
            #pos.append(new_start)
            yield new_start
            new_start += 1
        #return pos or None

    def find_pos(self, sub, start=0, end=2147483647):
        return [pos for pos in self._find_pos(sub, start, end)]

    def get_gccontent(self):
        from Bio.SeqUtils import GC
        return GC(self)

    def remove_intron(self, intron):
        length = len(intron)
        start = self.find(intron)
        if start  < 0:
            return self
        return self[0:start] + self[start+length::]

    def remove_introns(self, introns):
        new_seq = self
        for intron in introns:
            print intron
            new_seq = new_seq.remove_intron(intron)
            print new_seq
        return new_seq

    def __cmp__(self, other):
        return str(self) == str(other)

    def __getitem__(self, index):
        if isinstance(index, int):
            return self._data[index]
        else:
            return ExtendSeq(self._data[index], self.alphabet)

def searching_through_the_haystack(dnastrings):
    '''http://rosalind.info/problems/lcsm'''
    pass

def open_reading_frames(dnastring):
    from Bio.Data import CodonTable
    l = list()
    dna_codon_table = CodonTable.unambiguous_dna_by_name['Standard']
    s = ExtendSeq(dnastring)
    #for start_codon in dna_codon_table.start_codons:
    for start_codon in ('ATG',):
        start_list = s.find_pos(start_codon)
        for start in start_list:
            stop_list = []
            for stop_codon in dna_codon_table.stop_codons:
                if s[start+3:].find(stop_codon) >= 0:
                    stop_list.append(start+s[start+3:].find(stop_codon)+3)
            stop_list.sort()
            print s[start::]
            print stop_list
            print start, stop_list[0]
            print s[start: stop_list[0]].translate()
            l.append(s[start: stop_list[0]])
    print l
    """
    #starts = filter(None, [s.find_pos(sc) for sc in dna_codon_table.start_codons])
    starts = filter(None, [s.find_pos(sc) for sc in ('ATG',)])
    ends = filter(None, [s.find_pos(sc) for sc in dna_codon_table.stop_codons])
    from itertools import product
    raw_pos = product(starts, ends)
    pos = list()
    for (sposlist, eposlist) in raw_pos:
        pos.extend([(spos+3, epos-3) for spos, epos in product(sposlist, eposlist) if spos<epos])
    """

def enumerating_gene_orders(count):
    '''http://rosalind.info/problems/perm'''
    from itertools import permutations
    l = [e for e in permutations(xrange(1, count+1))]
    print len(l)
    print l

def chaining_the_amino_acids(protein):
    '''http://rosalind.info/problems/prtm'''
    mmtable = {
                'A':71.03711,
                'C':103.00919,
                'D':115.02694,
                'E':129.04259,
                'F':147.06841,
                'G':57.02146,
                'H':137.05891,
                'I':113.08406,
                'K':128.09496,
                'L':113.08406,
                'M':131.04049,
                'N':114.04293,
                'P':97.05276,
                'Q':128.05858,
                'R':156.10111,
                'S':87.03203,
                'T':101.04768,
                'V':99.06841,
                'W':186.07931,
                'Y':163.06333,
                }
    print sum([mmtable.get(e, 1) for e in protein])

def the_billion_year_war(dnastring):
    '''http://rosalind.info/problems/revp'''
    s = ExtendSeq(dnastring)
    l = list()
    window_size = xrange(4, 13, 2)
    length = len(s)

    for i in xrange(length-window_size[0]):
        for k in window_size:
            if i+k > length:
                continue
            sub = s[i:i+k]
            if str(sub) == str(sub[::-1].complement()):
                l.append((i+1, k))
    print l

def enumerating_kmers_lexicographically(dnastring, k):
    from itertools import product
    l = [''.join(c) for c in product(dnastring, repeat=k)]
    print l
    return l

def rna_splicing(dnastring, introns):
    '''http://rosalind.info/problems/splc/'''
    s = ExtendSeq(dnastring)
    new_s = s.remove_introns(introns)
    print new_s
    print new_s.translate()

def longest_increasing_subsequence(n, s):
    '''unsolved'''
    '''http://rosallind.info/problems/lgis/'''
    inc_l = list()
    dec_l = list()
    base_max_value,base_min_value = (s[0], s[1]) if s[0]>s[1] else (s[1],s[0])
    print base_max_value,base_min_value

    for i in s:
        if base_max_value > i:
            dec_l.append(i)
            base_max_value = i
        if base_min_value < i:
            inc_l.append(i)
            base_min_value = i

    print inc_l, dec_l

def genome_assembly_as_shortest_superstring(dnastrings):
    table = [(dnastring[0:3], dnastring[4::]) for dnastring in dnastrings]

def kmer_composition(dnastring, k=4):
    '''http://rosalind.info/problems/kmer/'''
    s = ExtendSeq(dnastring)
    length = len(s)
    l = enumerating_kmers_lexicographically('ACGT', k)
    print [len(s.find_pos(e)) for e in l]

def partial_gene_orderings(n, r):
    l = n - r + 1
    from operator import mul
    print range(l, n+1)
    print reduce(mul, range(l, n+1)) % 1000000

def enumerating_oriented_gene_orderings(n):
    x = range(-n, n+1)
    print 'ddd'
    print x
    print x.remove(0)
    from itertools import permutations
    print partial_gene_orderings(len(x), n)
    for e in permutations(x, n):
        print e

def calculate(s, t):
    len_s = len(s) + 1
    len_t = len(t) + 1
    m = np.zeros((len_s, len_t))
    m[:,0], m[0, :] = xrange(len_s), xrange(len_t)
    for i in xrange(1, len_s):
        for j in xrange(1, len_t):
            c1 = m[i-1, j] + 1
            c2 = m[i, j-1] + 1
            c3 = m[i-1, j-1] + 2 if s[i-1] != t[j-1] else m[i-1, j-1] 
            m[i, j] = min(c1, c2, c3)

    print m


if __name__ == '__main__':
    #counting_DNA_Nucleotide('AGCTTTTCATTCTGACTGCAACGGGCAATATGTCTCTGTGTGGATTAAAAAAAGAGTGTCTGATAGCAGC')
    #counting_point_mutation('GAGCCTACTAACGGGAT', 'CATCGTAATGACGGCCT')
    #transcribing_DNA_into_RNA('GATGGAACTTGACTACGTAAATT')
    #complementing_a_strand_of_DNA('AAAACCCGGT')
    #rabbits_and_recurrence_relations(5, 3)
    #computing_GC_content('AGCTATAG')
    #protein_translation('AUGGCCAUGGCGCCCAGAACUGAGAUCAAUAGUACCCGUAUUAACGGGUGA')
    #finding_a_motif_in_DNA('GATATATGCATATACTT', 'ATAT')
    #consensus_and_profile(['ATCCAGCT', 'GGGCAACT', 'ATGGATCT', 'AAGCAACC','TTGGAACT', 'ATGCCATT', 'ATGGCACT'])
    #mortal_fibonacci_rabbits(6, 3)
    #a_brief_introduction_to_graph_theory(labels, dnastrings, 3)
    #fail
    #open_reading_frames('AGCCATGTAGCTAACTCAGGTTACATGGGGATGACCCCGCGACTTGGATTAGAGTCTCTTTTGGAATAAGCCTGAATGATCCGAGTAGCATCTCAG')
    #enumerating_gene_orders(3)
    #chaining_the_amino_acids('SKADYEK')
    #no_name('TCAATGCATGCGGGTCTATATGCAT')
    #the_billion_year_war('TCAATGCATGCGGGTCTATATGCAT')
    #enumerating_kmers_lexicographically('ACGT', 2)
    #genes_are_discontiguous('ATGGTCTACATAGCTGACAAACAGCACGTAGCAATCGGTCGAATCTCGAGAGGCATATGGTCACATGATCGGTCGAGCGTGTTTCAAAGTTTGCGCCTAG',['ATCGGTCGAA', 'ATCGGTCGAGCGTGT'])
    #longest_increasing_subsequence(5, (5,1,4,2,3))
    #genome_assembly_as_shortest_superstring(['ATTAGACCTG',
    #                                        'CCTGCCGGAA'
    #                                        'AGACCTGCCG',
    #                                        'GCCGGAATAC'])

    #kmer_composition('CTTCGAAAGTTTGGGCCGAGTCTTACAGTCGGTCTTGAAGCAAAGTAACGAACTCCACGGCCCTGACTACCGAACCAGTTGTGAGTACTCAACTGGGTGAGAGTGCAGTCCCTATTGAGTTTCCGAGACTCACCGGGATTTTCGATCCAGCCTCAGTCCAGTCTTGTGGCCAACTCACCAAATGACGTTGGAATATCCCTGTCTAGCTCACGCAGTACTTAGTAAGAGGTCGCTGCAGCGGGGCAAGGAGATCGGAAAATGTGCTCTATATGCGACTAAAGCTCCTAACTTACACGTAGACTTGCCCGTGTTAAAAACTCGGCTCACATGCTGTCTGCGGCTGGCTGTATACAGTATCTACCTAATACCCTTCAGTTCGCCGCACAAAAGCTGGGAGTTACCGCGGAAATCACAG',4)
    #partial_gene_orderings(21, 7)
    enumerating_oriented_gene_orderings(2)
    calculate('PLEASANTLY', 'MEANLY')
