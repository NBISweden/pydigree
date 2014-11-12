#!/usr/bin/env python

from array import array
from itertools import izip
from pydigree._pydigree import choice_with_probs, linkeq_chrom


class Chromosome(object):
    """
    Chromsome is a class that keeps track of marker frequencies and distances.
    Not an actual chromosome with genotypes, which you would find under
    Individual.

    Markers are currently diallelic and frequencies are given for minor
    alleles. Marker frequencies must sum to 1. Major allele frequency
    is then f = 1 - f_minor.

    linkageequilibrium_chromosome generates chromsomes that are generated from
    simulating all markers with complete independence (linkage equilibrium).
    This is not typically what you want: you won't find any LD for association
    etc. linkageequilibrium_chromosome is used for 'seed' chromosomes when
    initializing a population pool or when simulating purely family-based
    studies for linkage analysis.
    """
    def __init__(self, label=None):
        # Chromosome name
        self.label = label
        # A list of floats that represent the position of the marker in cM
        self.genetic_map = []
        # A list of integers that doesnt do anything. Just for decoration
        self.physical_map = []
        # A list of floats representing minor allele frequencies
        self.frequencies = []
        # List of marker names
        self.labels = []
        # The typecode for the arrays. 'B' represents unsigned char, and can
        # store one byte of data, so:
        # 255 different values - 1 missing value = 254 possible alleles.
        # B is the smallest typecode in terms of memory usage.
        self.typecode = 'B'  # Unsigned char

    def __str__(self):
        return 'Chromosome %s: %s markers, %s cM' % \
            (self.label if self.label is not None else 'object',
             len(self.frequencies), max(self.genetic_map))

    def __iter__(self):
        return izip(self.labels, self.genetic_map, self.physical_map)

    def _iinfo(self):
        return izip(self.labels, self.genetic_map, self.physical_map,
                    self.frequencies)
    
    def nmark(self):
        return len(self.genetic_map)

    def size(self):
        return self.genetic_map[-1] - self.genetic_map[0]

    def add_genotype(self, frequency, map_position, label=None, bp=None):
        try:
            frequency = float(frequency) if frequency is not None else None
        except TypeError:
            raise ValueError('Invalid value for frequency %s' % frequency)
        self.genetic_map.append(map_position)
        self.frequencies.append(frequency)
        self.physical_map.append(bp)
        self.labels.append(label)

    def set_frequency(self, position, frequency):
        """ Manually change an allele frequency """
        self.frequencies[position] = frequency

    def linkageequilibrium_chromosome(self):
        """ Returns a randomly generated chromosome """
        if None in self.frequencies:
            raise ValueError('Not all frequencies are specified')
        chrom = linkeq_chrom(self.frequencies)
        return array(self.typecode, chrom)
