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
