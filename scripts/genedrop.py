#!/usr/bin/env python

import pydigree
import sys
import time
import itertools
import argparse

import numpy as np

from pydigree import ibs

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', required=True,
                    help='Pedigree file for simulations')
parser.add_argument('-n', '--niter', type=lambda x: int(float(x)), default=10000,
                    help='Number of simulations per pedigree')
parser.add_argument('--only', metavar='PED',
                    help='Only simulate specified pedigrees',
                    nargs='*', dest='onlypeds')
parser.add_argument('--obs', type=float, default=1.0,
                    help='Maximum observed value of test statistic')
parser.add_argument('--writedist', 
                    help='Write null distribution to file')
args = parser.parse_args()


def sbool(ped, inds, loc):
    npairs = float(len(inds) * (len(inds) - 1) / 2)
    r = [ibs(j.get_genotype(loc, checkhasgeno=False),
             k.get_genotype(loc, checkhasgeno=False),
             checkmissing=False) > 0 for j, k
         in itertools.combinations(inds, 2)]
    return sum(r) / npairs


def genedrop(ped, affs, scorer, iteration):
    if iteration % (args.niter / 10) == 0:
        print 'Simulation %s' % x
    ped.simulate_ibd_states(inds=affs)
    s = scorer(ped, affs, (0, 0))
    return s


scorefunction = sbool

pop = pydigree.Population(5000)
peds = pydigree.io.read_ped(args.file, pop)

nulldist = {}

for i, ped in enumerate(sorted(peds, key=lambda q: q.label)):
    if args.onlypeds and ped.label not in args.onlypeds:
        continue

    if len([x for x in ped if x.phenotypes['affected']]) < 2:
        print 'Error in pedigree {}: less than two affected individuals. Skipping.'.format(ped.label)
        continue

    # Clear the genotypes, if present
    ped.clear_genotypes()

    c = pydigree.Chromosome()
    c.add_genotype(0.5, 0)
    ped.add_chromosome(c)

    affs = [x for x in ped if x.phenotypes['affected']]

    print "Pedigree %s (%s/%s), %s simulations" % (ped.label, i+1, len(peds),  args.niter)

    sim_share = np.array([genedrop(ped, affs, scorefunction, x)
                             for x in xrange(args.niter)])
    nulldist[ped.label] = sim_share
    print 
#    print "Maximum simulated allele sharing: %s" % max(sim_share)
#    print "Empiric P: %s" % (len([x for x in sim_share if x >= args.obs]) / float(args.niter))

def stringify(n):
    if type(n) is str:
        return n
    else:
        return "{:.1e}".format(n)

print '\t'.join(['Pedigree','Min','Mean','SD','Max'])
for ped, dist in nulldist.iteritems():
    print '\t'.join(stringify(q) for q in [ped, dist.min(), dist.mean(), dist.std(), dist.max()])

if args.writedist:
    with open(args.writedist, 'w') as of:
        print "Outputting distribution to %s" % args.writedist
        for ped in sorted(peds, key=lambda q: q.label):
            try:
                of.write('{} {}\n'.format(ped.label, ' '.join(str(x) for x in nulldist[ped.label])))
            except KeyError:
                pass
