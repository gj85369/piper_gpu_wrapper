#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 09:55:14 2026

@author: g4code
"""

import argparse, json
import os
import tempfile, subprocess
from pathlib import Path

bpath = Path(__file__).parent.resolve()

cmd = f'{bpath}/pdb2fasta /home/g4code/projects/casp26/8UFO.pdb'

ok = subprocess.check_output(cmd, shell=True, universal_newlines=True)

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

print(parse_pdb2fasta(ok))