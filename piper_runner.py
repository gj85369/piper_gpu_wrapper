#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 21:34:51 2026

@author: g4code
"""
import argparse, json
import os
import tempfile, subprocess
from pathlib import Path

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
    
    


def main(argsin):
    
    cmd = [str(argsin.piper_path)]
    cmd.append('--antibody')
    if argsin.advanced:
        cmd.append('--advanced')
        cmd.append(str(argsin.advanced))
    
    
    if not argsin.minimize:
        cmd.append('--dont-minimize')
    if argsin.odirfull:
        cmd.append('--output-dir')
        cmd.append(str(argsin.odirfull))
    cmd.append('--lig')
    cmd.append(str(argsin.ligand))
    cmd.append('--rec')
    cmd.append(str(argsin.receptor))
    cos = os.environ.copy()
    cos['CUDA_VISIBLE_DEVICES'] = str(argsin.gpu)
    print(' '.join(cmd))
    subprocess.check_output(' '.join(cmd), shell=True, universal_newlines=True, env=cos)
    




if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-r",
                        "--receptor",
                        help="Receptor pdb",
                        required=True,  
                        type=Path)
    parser.add_argument("-l",
                        "--ligand",
                        help="Ligand pdb",
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
    agroup = parser.add_argument_group('advanced', '''These are advanced options please dont touch unless you know what you are doing
                              also please dont use these and the advanced json option''')    
    agroup.add_argument("--fft_cell_spacing",
                        help="Dont touch unless you know what you are doing",
                        type=float)    
    agroup.add_argument("--fft_mask_radius",
                        help="Dont touch unless you know what you are doing",
                        type=float)   
    agroup.add_argument("--fft_num_eigens",
                        help="Dont touch unless you know what you are doing",
                        type=float)   
    agroup.add_argument("--max_models",
                        help="Dont touch unless you know what you are doing",
                        type=int)   
    agroup.add_argument("--radius_for_clustering",
                        help="Dont touch unless you know what you are doing",
                        type=float)     
    agroup.add_argument("--translations_for_clustering",
                        help="Dont touch unless you know what you are doing",
                        type=int)       
    agroup.add_argument("--mask_repulse",
                        help="Dont touch unless you know what you are doing")
    
    args = parser.parse_args()
    if not args.ligand:
        print('ligand pdb needed')
        quit()
    if not args.receptor:
        print('receptor pdb needed')
        quit()
    bd = base_info()
    if bd:
        provided_data = list(bd.keys())
    
    if not args.piper:
        if 'piper_location' not in provided_data:
            print('you need to specify piper location')
            quit()
        else:
            args.piper_path = Path(bd['piper_location'])
    else:
        args.piper_path = args.piper
     
    
    if args.output:        
        args.odirfull = args.output.absolute()
    else:
        args.odirfull = False
    
    main(args)
