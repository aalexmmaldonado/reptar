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

"""Tests many-body utilities"""

import pytest
import os
import shutil
import numpy as np
from reptar import File
from reptar.mb import mb_contributions

import sys
sys.path.append("..")
from .paths import *

# Ensures we execute from file directory (for relative paths).
os.chdir(os.path.dirname(os.path.realpath(__file__)))

def test_2h2o_mb_from_data():
    """Computing 2-body energy and gradient contributions.
    """
    exdir_path = get_140h2o_samples_path()

    exdir_file = File(exdir_path, mode='r')

    # Computing reptar values
    E = np.array(exdir_file.get('2h2o/energy_ele_rimp2.ccpvtz'))[:10]  # Eh
    G = np.array(exdir_file.get('2h2o/grads_rimp2.ccpvtz'))[:10]  # Eh/A
    entity_ids = np.array(exdir_file.get('2h2o/entity_ids'))
    r_prov_ids = exdir_file.get('2h2o/r_prov_ids')
    r_prov_specs = np.array(exdir_file.get('2h2o/r_prov_specs'))[:10]

    E_lower = np.array(exdir_file.get('1h2o/energy_ele_rimp2.ccpvtz')) # Eh
    G_lower = np.array(exdir_file.get('1h2o/grads_rimp2.ccpvtz'))  # Eh/A
    entity_ids_lower = np.array(exdir_file.get('1h2o/entity_ids'))
    r_prov_ids_lower = exdir_file.get('1h2o/r_prov_ids')
    r_prov_specs_lower = np.array(exdir_file.get('1h2o/r_prov_specs'))

    E_mb, G_mb = mb_contributions(
        E, G, entity_ids, r_prov_ids, r_prov_specs, E_lower, G_lower,
        entity_ids_lower, r_prov_ids_lower, r_prov_specs_lower,
        n_workers=1
    )

    assert E_mb[5] == -0.0025468531256365168
    assert G_mb[5][1][2] == -0.02043695304313046

def test_4h2o_mb_from_data():
    """Many-body prediction of water tetramers."""
    exdir_path = get_temelso_path()

    exdir_file = File(exdir_path, mode='r')

    isomer_key = '4h2o'

    E_true = exdir_file.get(f'{isomer_key}/energy_ele_mp2.def2tzvp_orca')
    G_true = exdir_file.get(f'{isomer_key}/grads_mp2.def2tzvp_orca')
    assert np.allclose(E_true, np.array([-305.30169218, -305.2999005, -305.29520327]))
    E_mb = np.zeros(E_true.shape)
    G_mb = np.zeros(G_true.shape)
    entity_ids = exdir_file.get(f'{isomer_key}/entity_ids')
    r_prov_ids = None
    r_prov_specs = None

    def get_lower_data(group_key, e_key, g_key):
        E_lower = exdir_file.get(f'{group_key}/{e_key}')
        print(E_lower.dtype)
        G_lower = exdir_file.get(f'{group_key}/{g_key}')
        entity_ids_lower = exdir_file.get(f'{group_key}/entity_ids')
        r_prov_ids_lower = exdir_file.get(f'{group_key}/r_prov_ids')
        r_prov_specs_lower = exdir_file.get(f'{group_key}/r_prov_specs')
        return E_lower, G_lower, entity_ids_lower, r_prov_ids_lower, r_prov_specs_lower

    lower_data = []
    lower_data.append((
        get_lower_data(
            f'{isomer_key}/samples_1h2o',
            'energy_ele_mp2.def2tzvp_orca', 'grads_mp2.def2tzvp_orca'
        )
    ))
    lower_data.append((
        get_lower_data(
            f'{isomer_key}/samples_2h2o',
            'energy_ele_nbody_mp2.def2tzvp_orca', 'grads_nbody_mp2.def2tzvp_orca'
        )
    ))
    lower_data.append((
        get_lower_data(
            f'{isomer_key}/samples_3h2o',
            'energy_ele_nbody_mp2.def2tzvp_orca', 'grads_nbody_mp2.def2tzvp_orca'
        )
    ))

    for data in lower_data:
        E_mb, G_mb = mb_contributions(
            E_mb, G_mb, entity_ids, r_prov_ids, r_prov_specs,
            *data, operation='add', n_workers=1
        )

    assert np.allclose(E_mb, np.array([-305.30075391, -305.29900387, -305.29489548]))
