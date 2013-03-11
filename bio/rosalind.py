from collections import defaultdict

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

def transcribing_DNA_into_RNA(dnastring):
    l = []
    for n in dnastring:
        if n == 'T':
            l.append('U')
        else:
            l.append(n)
    print ''.join(l)

def complementing_a_strand_of_DNA(dnastring):
    complement = {'A':'T', 'G':'C', 'C':'G', 'T':'A'}
    print ''.join([complement.get(n, n) for n in dnastring])[::-1]


def counting_point_mutation(s, t):
    '''http://rosalind.info/problems/hamm/'''
    assert(len(s) == len(t))
    print len([1 for i, n in enumerate(s) if t[i]!=n]) 

if __name__ == '__main__':
    counting_DNA_Nucleotide('AGCTTTTCATTCTGACTGCAACGGGCAATATGTCTCTGTGTGGATTAAAAAAAGAGTGTCTGATAGCAGC')
    counting_point_mutation('GAGCCTACTAACGGGAT', 'CATCGTAATGACGGCCT')
    transcribing_DNA_into_RNA('GATGGAACTTGACTACGTAAATT')
    complementing_a_strand_of_DNA('AAAACCCGGT')
