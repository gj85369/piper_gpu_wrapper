#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 09:55:14 2026

@author: g4code
"""

import argparse
import json
import os
import tempfile
import subprocess
from pathlib import Path
from glob import glob

from Bio import SeqIO
from msa_mmseqs import get_MSAs_mmseq

bpath = Path(__file__).parent.resolve()



def parse_pdb2fasta(pdb2fasta_results):
    lns = []
    for inst in pdb2fasta_results.split('\n'):
        if len(inst) > 0:
            lns.append(inst)
    
    chdic = {}
    for i in range(0,len(lns)):
        if lns[i][0] == '>':
            pts = lns[i].split()
            chpt = [x for x in pts if ':' in x][0]
            chain_name = chpt.split(':')[1].strip()
            fast_seq = lns[i+1].strip()
            chdic[chain_name] = fast_seq
    return chdic



def make_file(file_name, file_contents):
    with open(file_name, 'w') as f:
        for inst in file_contents:
            f.write(inst)
    f.close()
def write_fastas(chain_dict, fasta_dir):
    for inst in list(chain_dict.keys()):
        fc = [f'>{inst.upper()}\n', chain_dict[inst]]
        make_file(f'{fasta_dir}/{inst.upper()}.fasta', fc)
        


def mas_mmseqs_api(fasta_dir, output_dir):
    seq_dict = {}
    fasta_files = glob(fasta_dir.strip('/') + '/*.fa')
    fasta_files += glob(fasta_dir.strip('/') + '/*.fas')
    fasta_files += glob(fasta_dir.strip('/') + '/*.fasta')
    print(fasta_files)
    for filename in fasta_files:
        print(filename)
        label = os.path.splitext(os.path.basename(filename))[0]
        with open(filename, 'r') as f:
            for record in SeqIO.parse(f, "fasta"):
                seq_dict[label] = record.seq
                break
    a3m_dict = get_MSAs_mmseq(seq_dict, output_path=output_dir)
        
    


def run_pdb2fasta(pdb_path):
    cmd = f'{bpath}/pdb2fasta {pdb_path}'
    ok = subprocess.check_output(cmd, shell=True, universal_newlines=True)
    return ok

