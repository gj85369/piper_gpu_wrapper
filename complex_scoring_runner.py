#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 23:06:46 2026

@author: g4code
"""
import argparse
import sys
import os
import subprocess
from pathlib import Path

from glob import glob
from multiprocessing import Pool
import copy
bpath = Path(__file__).parent.resolve()


def run_inst(inls):
    cmdlist, gpun = inls
    outlist = []
    for cmdl in cmdlist:
        cmd, fname = cmdl
        print(f'running complex {fname}')
        cos = os.environ.copy()
        cos['CUDA_VISIBLE_DEVICES'] = str(gpun)
        outlist.append(subprocess.check_output(cmd, shell=True, universal_newlines=True, env=cos))
    return outlist


def ret_mod(inint, gpunumber):
    return inint%gpunumber

class complex_scoring_runner:
    def __init__(self, argsin):
        self.argsin = argsin
        self.out_dir = f'{self.argsin.output}/scoring_output'
        os.makedirs(self.out_dir, exist_ok=True)
        
    
    def make_command(self):
        cmd = [self.argsin.gpu_runner_location]
        for inst in self.argsin.rec_res:
            cmd.append('-r')
            cmd.append(inst)
        for inst in self.argsin.lig_res:
            cmd.append('-l')
            cmd.append(inst)            
        cmd.append('-c')
        cmd.append(self.argsin.complex_dir)
        cmd.append('-o')
        cmd.append(self.out_dir)
        if self.argsin.nanobody:
            cmd.append('--nanobody')
        self.cmd = cmd
        
        
        
    def runner(self):
        cfiles = glob(f'{self.argsin.complex_dir}/*.pdb')
        pyinst = [sys.executable]
        self.make_command()
        vlist = self.cmd
        cind = vlist.index('-c')
        oind = vlist.index('-o')

        instances = []
        instdic = {}
        for i in range(0,int(self.argsin.num_gpus)):
            instdic[i] = []
        
        for i in range(0,len(cfiles)):
            finst = cfiles[i]
            print(f'running {finst}')
            vtmp = copy.deepcopy(vlist)
            fname = finst.split('/')[-1].split('.pdb')[0]
            vtmp[cind + 1] = finst
            vtmp[oind + 1] = f'{vlist[oind+1]}/{fname}'
            tl = pyinst + vtmp
            cid = ret_mod(i, self.argsin.num_gpus)
            instdic[cid].append([' '.join(tl), fname])
        
        for i in range(0,int(self.argsin.num_gpus)):
            instances.append([instdic[i], str(i)])
            
        with Pool(processes=self.argsin.num_gpus) as p:
            instances = p.map(run_inst, instances)
    
    
    






