# MIT License
# 
# Copyright (c) 2022, Alex M. Maldonado
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Tests sampling structures from exdir Groups"""

import pytest
import os
import shutil
import numpy as np
from reptar import creator
from reptar.sampler import add_structures_to_group
import itertools

import sys
sys.path.append("..")
from .paths import *

# Ensures we execute from file directory (for relative paths).
os.chdir(os.path.dirname(os.path.realpath(__file__)))

# Source paths
xtb_dir = './tmp/xtb'

# Writing paths
sampling_dir = './tmp/sampling/'
os.makedirs(sampling_dir, exist_ok=True)

def test_1h2o_120meoh_prod_sampling():
    """Sampling from xTB MD reptar file.
    """
    source_path = os.path.join(xtb_dir, '1h2o_120meoh_md.exdir')
    dest_path = f'{sampling_dir}/test_1h2o_120meoh_prod_sampling.exdir'

    source = creator()
    source.load(source_path, mode='r')
    source_key = '/prod_1'

    dest = creator()
    dest.load(dest_path, mode='w', allow_remove=True)
    dest_key = '/wat.2met-pes'
    dest.rfile.init_group(dest_key)

    quantity = 100
    comp_labels = ('WAT', 'MET', 'MET')

    add_structures_to_group(
        source.rfile, source_key, dest.rfile, dest_key, quantity,
        comp_labels, center_structures=False, copy_EG=False, write=True
    )
    assert np.array_equal(
        dest.rfile.get(f'{dest_key}/atomic_numbers'),
        np.array([8, 1, 1, 8, 1, 6, 1, 1, 1, 8, 1, 6, 1, 1, 1])
    )
    assert np.array_equal(
        dest.rfile.get(f'{dest_key}/entity_ids'),
        np.array([0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2])
    )
    assert dest.rfile.get(f'{dest_key}/geometry').shape == (100, 15, 3)
    assert dest.rfile.get(f'{dest_key}/r_prov_specs').shape == (100, 5)
    assert len(dest.rfile.get(f'{dest_key}/r_prov_ids')) == 1
    assert dest.rfile.get(f'{dest_key}/r_centered') == False
    assert np.array_equal(
        dest.rfile.get(f'{dest_key}/comp_ids'), np.array(comp_labels)
    )

    add_structures_to_group(
        source.rfile, source_key, dest.rfile, dest_key,
        quantity, comp_labels, center_structures=True, copy_EG=False, write=True
    )
    assert np.array_equal(
        dest.rfile.get(f'{dest_key}/atomic_numbers'),
        np.array([8, 1, 1, 8, 1, 6, 1, 1, 1, 8, 1, 6, 1, 1, 1])
    )
    assert np.array_equal(
        dest.rfile.get(f'{dest_key}/entity_ids'),
        np.array([0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2])
    )
    assert dest.rfile.get(f'{dest_key}/geometry').shape == (200, 15, 3)
    assert dest.rfile.get(f'{dest_key}/r_prov_specs').shape == (200, 5)
    assert len(dest.rfile.get(f'{dest_key}/r_prov_ids')) == 1
    assert dest.rfile.get(f'{dest_key}/r_centered') == True
    assert np.array_equal(
        dest.rfile.get(f'{dest_key}/comp_ids'), np.array(comp_labels)
    )

def test_sampling_from_wat_2met_pes():
    """Sampling from a sampled exdir group.
    """
    src_path = f'{sampling_dir}/test_1h2o_120meoh_prod_sampling.exdir'

    source = creator()
    source.load(src_path, mode='a')
    source_key = '/wat.2met-pes'
    dest_key = '/wat.met-pes'
    source.rfile.init_group(dest_key)

    quantity = 100
    comp_labels = ('WAT', 'MET')

    add_structures_to_group(
        source.rfile, source_key, source.rfile, dest_key,
        quantity, comp_labels, center_structures=True, copy_EG=False
    )

    assert np.array_equal(
        source.rfile.get(f'{dest_key}/entity_ids'),
        np.array([0, 0, 0, 1, 1, 1, 1, 1, 1])
    )
    assert len(source.rfile.get(f'{dest_key}/r_prov_ids')) == 1
    assert source.rfile.get(f'{dest_key}/r_centered') == True
    assert np.array_equal(
        source.rfile.get(f'{dest_key}/comp_ids'), np.array(comp_labels)
    )
