from __future__ import division
import os

import pydigree as pyd
from pydigree.stats.mixedmodel import MixedModel

testdir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       'test_data',
                       'h2test')

# A dataset simulated to have population h2 = 50%
# Evaluated by SOLAR to have h2 = 45.92%
pedigree_file = os.path.join(testdir, 'h2test.pedigrees')
phenotype_file = os.path.join(testdir, 'h2test.csv')

solar_h2 = 0.4592420

def makemm():
    peds = pyd.io.read_ped(pedigree_file)
    pyd.io.read_phenotypes(peds, phenotype_file)
    mm = MixedModel(peds, outcome='synthetic')
    mm.add_genetic_effect()

    return mm

def test_fisherscoring():
    model = makemm()
    model.maximize(method='FS')

    total_var = sum(model.variance_components)
    # Allow a deviation up to 5 percentage points
    assert (model.variance_components[-2]/total_var - solar_h2) < 0.05  

def test_newtonraphson():
    model = makemm()
    model.maximize(method='NR')

    total_var = sum(model.variance_components)
    # Allow a deviation up to 5 percentage points
    assert (model.variance_components[-2]/total_var - solar_h2) < 0.05 

def test_aireml():
    model = makemm()
    model.maximize(method='NR')

    total_var = sum(model.variance_components)
    # Allow a deviation up to 5 percentage points
    assert (model.variance_components[-2]/total_var - solar_h2) < 0.05 

def test_emreml():
    model = makemm()
    model.maximize(method='EM')

    total_var = sum(model.variance_components)
    # Allow a deviation up to 5 percentage points
    assert (model.variance_components[-2]/total_var - solar_h2) < 0.05 

if __name__ == '__main__':
    test_fisherscoring()