#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 21:34:51 2026

@author: g4code
"""
import os
import subprocess
from glob import glob
from pathlib import Path
import tempfile
bpath = Path(__file__).parent.resolve()

    

    


class piper_runner_class:
    def __init__(self, argsin):
        self.argsin = argsin
        os.makedirs(f'{self.argsin.odirfull}/piper_outs', exist_ok=True)
        self.piper_out_dir = f'{self.argsin.odirfull}/piper_outs'
        self.runner()
    
    
    def check_outs(self):
        recname = self.argsin.receptor.split('/')[-1].split('.pdb')[0]
        ligname = self.argsin.ligand.split('/')[-1].split('.pdb')[0]
        
        self.mod_count = glob(f'{self.argsin.odirfull}/piper_outs/{recname}_{ligname}.antibody/model*.pdb')
        if len(self.mod_count) > 0:
            return True
        else:
            return False
    def runner(self):
            
        cmd = [str(self.argsin.piper_path)]
        cmd.append('--antibody')
        if self.argsin.advanced:
            cmd.append('--advanced')
            cmd.append(str(self.argsin.advanced))
        
        
        if not self.argsin.minimize:
            cmd.append('--dont-minimize')
        if self.argsin.odirfull:
            cmd.append('--output-dir')
            cmd.append(str(self.piper_out_dir))
        cmd.append('--lig')
        cmd.append(str(self.argsin.ligand))
        cmd.append('--rec')
        cmd.append(str(self.argsin.receptor))
        cos = os.environ.copy()
        cos['CUDA_VISIBLE_DEVICES'] = str(self.argsin.gpu)
        print(' '.join(cmd))
        subprocess.check_output(' '.join(cmd), shell=True, universal_newlines=True, env=cos)
        self.success =  self.check_outs()
        
        
        


