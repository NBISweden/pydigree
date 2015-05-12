from pydigree.io import smartopen as open


def read_kinship(filename):
    '''
    Reads a KinInbCoef formatted file of kinship and inbreeding coefficients

    Arguments
    ------
    filename: the filename to be read
    
    Returns: a dictionary in the format 
    {frozenset({(fam, ind_a), (fam, ind_b)}): kinship/inbreeding
    '''
    kindict = {}
    with open(filename) as f:
        for line in f:
            fam, ida, idb, phi = line.strip().split()
            kindict[frozenset({(fam, ida), (fam, idb)})] = float(phi)
    return kindict