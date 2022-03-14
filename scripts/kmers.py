import math
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

def make_kmers(k, FASTA_filename, threshold=1022):
    kmers = []
    for record in SeqIO.parse(FASTA_filename, "fasta"):
        if(len(record.seq) <= threshold):
            continue
        for i in range(len(record.seq) - int(k) + 1):
            kmer_name = record.name.replace('-', '_')+'-'+str(i)
            seq_str = record.seq[i:int(k)+i]
            kmer_seq_record = SeqRecord(Seq(seq_str), id=kmer_name, 
                                        name=kmer_name,
                                        description='Created with kmers module')
            kmers.append(kmer_seq_record)
    return kmers
