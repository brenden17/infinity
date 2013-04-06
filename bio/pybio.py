from Bio.Seq import Seq
from Bio.SeqIO import parse
from Bio import SeqIO
from Bio import GenBank
from Bio import ExPASy

def seq():
    my_seq = Seq('AGC')
    print my_seq
    print my_seq.alphabet.letters

def get_seq_from_files(filename):
    ext = filename.split('.')[-1]
    table = {'fasta':'fasta', 'gbk':'genbank'}
    fmt = table.get(ext, 'fasta')
    handle = open(filename)
    for r in parse(handle, fmt):
        print r.id
        print r.seq
    handle.close()

def get_genbak(l):
    handle = BenBank.download_many(['6273291', '6273290'])
    for seq_record in SeqIO.parse(handle, 'genbank'):
        print seq_record.seq
        print seq_record.features

    handle.close()

def get_swissport(l):
    handle = ExPASy.get_sport_raw('023729')
    pass

def get_seq(source, fmt):
    handle = None
    if fmt == 'fasta':
        handle = open(source)
    elif fmt == 'genbank':
        hanlde = open(sourc)
    elif fmt == 'swiss':
        handle = ExPASy.get_sprot_raw(source)
    else:
        raise TypeError('Need to choose correct file format')

    record_iterator = SeqIO.parse(handle, fmt)
    #handle.close()
    return record_iterator

def test():
    ir = get_seq('./files/ls_orchid.fasta', 'fasta')
    for n in ir:
        print n

if __name__ == '__main__':
    #seq()
    #files('./files/ls_orchid.fasta')
    #files('./files/ls_orchid.gbk')
    test()
