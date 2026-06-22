#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 14:47:02 2026

@author: g4code
"""

import argparse, json
import os
import tempfile, subprocess
from pathlib import Path
from piper_runner_class import piper_runner_class
from scoring_setup import setup_scoring
from pdb_2_fasta import pdb2fasta_runner
from complex_scoring_runner import complex_scoring_runner
bpath = Path(__file__).parent.resolve()

    

def base_info():
    base_json = Path(f'{bpath}/basic_info.json')
    if base_json.is_file():
        with open(base_json, 'r') as f:
            ret_data = json.load(f)
        f.close()
        return ret_data
    else:
        return False
    
    

def parse_advanced(argsin):
    if not argsin.advanced:
        tjson = {}
        tjson['radius_for_clustering'] = argsin.radius_for_clustering
        tjson['translations_for_clustering'] = argsin.translations_for_clustering
        with open(f'{argsin.odirfull}/advanced.json', 'w') as f:
            json.dump(tjson, f)
        f.close()
        argsin.advanced = f'{argsin.odirfull}/advanced.json'
            
            
        


def parse_inputs(argsin):
    if not argsin.ligand:
        print('ligand pdb needed')
        quit()
    if not argsin.receptor:
        print('receptor pdb needed')
        quit()
    bd = base_info()
    if bd:
        provided_data = list(bd.keys())
    if not argsin.piper:
        if 'piper_location' not in provided_data:
            print('you need to specify piper location')
            quit()
        else:
            argsin.piper_path = Path(bd['piper_location'])
    else:
        argsin.piper_path = args.piper
    if 'gpu_runner_location' in list(bd.keys()):
        argsin.gpu_runner_location = bd['gpu_runner_location']
    if argsin.output:        
        if not args.output.is_dir():
            
            try:
                args.output.mkdir()
            except Exception as e:
                print(f'error making working directory {e}')
                quit()
        argsin.odirfull = args.output.absolute()
        
            
    else:
        argsin.odirfull = os.getcwd()
    parse_advanced(argsin)
    
    

class main_runner:
    def __init__(self, argsin):
        self.argsin = argsin
        
    def parse_inputs(self):
        r_pdbfas = pdb2fasta_runner(bpath, self.argsin.receptor)
        self.receptor_chdic = r_pdbfas.chain_dict
        
        l_pdbfas = pdb2fasta_runner(bpath, self.argsin.ligand)
        self.ligand_chdic = l_pdbfas.chain_dict
    
    def runner(self):
        print('piper run')
        pip_run = piper_runner_class(self.argsin)
        
        if not pip_run.success:
            print('There was an error running the piper run please check inputs')
            quit()
            
        print('scoring setup')
        
        set_score = setup_scoring(self.argsin.output, self.argsin.ligand, self.argsin.receptor)
        set_score.runner()
        self.argsin.ligand_a3ms = set_score.lig_res
        self.argsin.receptor_a3ms = set_score.rec_res
        
        
        
        print('scoring run')
        self.argsin.complex_dir = str(Path(pip_run.mod_count[0]).parent)
        complex_run = complex_scoring_runner(self.argsin)
        complex_run.runner()
        
        
        
def main(argsin):

    print('piper run')
    pip_run = piper_runner_class(argsin)
    
    if not pip_run.success:
        print('There was an error running the piper run please check inputs')
        quit()
        
    print('scoring setup')
    
    set_score = setup_scoring(argsin.output, argsin.lgand, argsin.receptor)
    
    
    print('scoring run')
            
    
    
    
    
    
    

    




if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-r",
                        "--receptor",
                        help="Antigen pdb",
                        required=True,  
                        type=Path)
    parser.add_argument("-l",
                        "--ligand",
                        help="Antibody pdb",
                        required=True,                          
                        type=Path)    
    parser.add_argument("-a",
                        "--advanced",
                        help="Advanced options json",
                        type=Path)      
    parser.add_argument("-o",
                        "--output",
                        help="Output dir",
                        type=Path)     
    parser.add_argument('--minimize', 
                        action='store_true', 
                        help='Minimize results')
    parser.add_argument("-p",
                        "--piper",
                        help="Piper location",
                        type=Path) 
    parser.add_argument("-g",
                        "--gpu",
                        help="Index of gpu to use",
                        default=0,
                        type=int)    

    parser.add_argument("--num-gpus",
                        help="amount of gpus to use.",
                        default=1,
                        type=int)       
    parser.add_argument('-n', '--nanobody',help='is the system a nanobody',  action='store_true')    
    
    agroup = parser.add_argument_group('advanced', '''These are advanced options please dont touch unless you know what you are doing
                              also please dont use these and the advanced json option''')    
    # agroup.add_argument("--fft_cell_spacing",
    #                     help="Dont touch unless you know what you are doing",
    #                     type=float)    
    # agroup.add_argument("--fft_mask_radius",
    #                     help="Dont touch unless you know what you are doing",
    #                     type=float)   
    # agroup.add_argument("--fft_num_eigens",
    #                     help="Dont touch unless you know what you are doing",
    #                     type=float)   
    # agroup.add_argument("--max_models",
    #                     help="Dont touch unless you know what you are doing",
    #                     type=int)   
    agroup.add_argument("--radius_for_clustering",
                        help="Dont touch unless you know what you are doing",
                        default=3.0,
                        type=float)     
    agroup.add_argument("--translations_for_clustering",
                        help="Dont touch unless you know what you are doing",
                        default=4000,
                        type=int)       
    # agroup.add_argument("--mask_repulse",
    #                     help="Dont touch unless you know what you are doing")
    
    args = parser.parse_args()
    parse_inputs(args)
    ok = main_runner(args)
    ok.runner()
