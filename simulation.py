import uproot
import awkward as ak
import numpy as np

def load_jet_data(filepath):
    file = uproot.open(filepath)
    tree = file['Events']
    branches = ['nJet', 'Jet_pt', 'Jet_eta', 'Jet_phi', 'Jet_mass']
    jets = tree.arrays(branches, library='ak')
    return jets

def filter_jets(jets, pt_min=30, eta_max=2.4):
    """Apply basic quality cuts to jets."""
    pt = jets['Jet_pt']
    eta = jets['Jet_eta']
    mask = (pt > pt_min) & (np.abs(eta) < eta_max)
    filtered_pt = pt[mask]
    filtered_eta = eta[mask]
    filtered_phi = jets['Jet_phi'][mask]
    filtered_mass = jets['Jet_mass'][mask]
    return ak.zip({
        'Jet_pt': filtered_pt,
        'Jet_eta': filtered_eta,
        'Jet_phi': filtered_phi,
        'Jet_mass': filtered_mass
    })

def get_jet_multiplicity(jets):
    return ak.num(jets['Jet_pt'])