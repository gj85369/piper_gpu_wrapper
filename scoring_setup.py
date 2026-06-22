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

from pdb_2_fasta import pdb2fasta_runner

bpath = Path(__file__).parent.resolve()


class setup_scoring:
    def __init__(self, working_dir, ligand, receptor):
        self.working_dir = working_dir
        self.ligand = ligand
        self.receptor = receptor
        
        
    def make_dirs(self, indir):
        os.makedirs(f'{indir}/fastas', exist_ok=True)
        os.makedirs(f'{indir}/msas', exist_ok=True)
        return [f'{indir}/fastas', f'{indir}/msas']
    
    def rec_run(self):
        os.makedirs(f'{self.working_dir}/receptor', exist_ok=True)
        self.rec_fas, self.rec_mas = self.make_dirs(f'{self.working_dir}/receptor')
        pfrun = pdb2fasta_runner(bpath, self.receptor)
        self.rec_chain_dict = pfrun.chain_dict
        self.write_fastas(self.rec_chain_dict, self.rec_fas)
        self.msa_mmseqs_api(self.rec_fas, self.rec_mas)

        
        
    def lig_run(self):
        os.makedirs(f'{self.working_dir}/ligand', exist_ok=True)
        self.lig_fas, self.lig_mas = self.make_dirs(f'{self.working_dir}/ligand')
        pfrun = pdb2fasta_runner(bpath, self.ligand)
        self.lig_chain_dict = pfrun.chain_dict
        self.write_fastas(self.lig_chain_dict, self.lig_fas)
        self.msa_mmseqs_api(self.lig_fas, self.lig_mas)        

        
        
        
        
    # def parse_pdb2fasta(self):
    #     lns = []
    #     for inst in self.pdb2fasta_results.split('\n'):
    #         if len(inst) > 0:
    #             lns.append(inst)
        
    #     chdic = {}
    #     for i in range(0,len(lns)):
    #         if lns[i][0] == '>':
    #             pts = lns[i].split()
    #             chpt = [x for x in pts if ':' in x][0]
    #             chain_name = chpt.split(':')[1].strip()
    #             fast_seq = lns[i+1].strip()
    #             chdic[chain_name] = fast_seq
    #     self.chain_dict = chdic
    
    
    
    def make_file(self, file_name, file_contents):
        with open(file_name, 'w') as f:
            for inst in file_contents:
                f.write(inst)
        f.close()
    def write_fastas(self, chain_dict, fasta_dir):
        for inst in list(chain_dict.keys()):
            fc = [f'>{inst.upper()}\n', chain_dict[inst]]
            self.make_file(f'{fasta_dir}/{inst.upper()}.fasta', fc)
            
    
    
    def msa_mmseqs_api(self, running_dir, out_dir):
        seq_dict = {}
        fasta_files = glob(running_dir + '/*.fa')
        fasta_files += glob(running_dir + '/*.fas')
        fasta_files += glob(running_dir + '/*.fasta')
        print(fasta_files)
        for filename in fasta_files:
            print(filename)
            label = os.path.splitext(os.path.basename(filename))[0]
            with open(filename, 'r') as f:
                for record in SeqIO.parse(f, "fasta"):
                    seq_dict[label] = record.seq
                    break
        a3m_dict = get_MSAs_mmseq(seq_dict, output_path=out_dir)
        return a3m_dict
            
        
    
    
    # def run_pdb2fasta(self):
    #     cmd = f'{bpath}/pdb2fasta {self.model_pdb}'
    #     self.pdb2fasta_results = subprocess.check_output(cmd, shell=True, universal_newlines=True)
    def check_a3ms(self):
        self.lig_res = glob(f'{self.lig_mas}/*/mmseqs/aggregated.a3m')
        self.rec_res = glob(f'{self.rec_mas}/*/mmseqs/aggregated.a3m')
        
        return self.lig_res + self.rec_res
    
    def runner(self):
        self.rec_run()
        self.lig_run()
        print(self.check_a3ms())
        
        
        

