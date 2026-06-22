#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 17:57:27 2026

@author: g4code
"""
import subprocess


class pdb2fasta_runner:
    def __init__(self, bpath, in_pdb):
        self.bpath = bpath
        self.in_pdb = in_pdb
        self.runner()
    
    
    def run_pdb2fasta(self):
        cmd = f'{self.bpath}/pdb2fasta {self.in_pdb}'
        self.pdb2fasta_results = subprocess.check_output(cmd, shell=True, universal_newlines=True)
        
    def parse_pdb2fasta(self):
        lns = []
        for inst in self.pdb2fasta_results.split('\n'):
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
        self.chain_dict = chdic        

    def runner(self):
        self.run_pdb2fasta()
        self.parse_pdb2fasta()