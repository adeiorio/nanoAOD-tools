#!/usr/bin/env python
import os
import sys
import ROOT
import math
import datetime
from array import array
from skimtree_utils import *

localrun = False # True #
if not(localrun):
    from samples import *
else:
    from samples.samples import *
sample = sample_dict[sys.argv[1]]
part_idx = sys.argv[2]
file_list = map(str, sys.argv[3].strip('[]').split(','))
print(file_list)

Debug = False # True #
MCReco = True
DeltaFilter = True

startTime = datetime.datetime.now()
print("Starting running at " + str(startTime))

ROOT.gROOT.SetBatch()

leadingjet_ptcut = 150.

chain = ROOT.TChain('Events')
print(chain)
for infile in file_list: 
    print("Adding %s to the chain" %(infile))
    chain.Add(infile)

tree = InputTree(chain)
print("Number of entries: " +str(tree.GetEntries()))

isMC = True
if ('Data' in sample.label):
    isMC = False

MCReco = MCReco * isMC

#++++++++++++++++++++++++++++++++++
#++   branching the new trees    ++
#++++++++++++++++++++++++++++++++++
outTreeFile = ROOT.TFile(sample.label+"_part"+str(part_idx)+".root", "RECREATE") #some name of the output file
trees = []
for i in range(10):
    trees.append(None)
#systZero = systWeights()
# defining the operations to be done with the systWeights class
maxSysts = 0
addPDFsyst = False
addPDF = True
addQ2 = False
addTopPt = False
addVHF = False
addTTSplit = False
addTopTagging = False
addWTagging = False
addTrigSF = False
nPDF = 0

systTree = systWeights()
systTree.prepareDefault(True, addQ2, addPDFsyst, addTopPt, addVHF, addTTSplit)
systTree.addSelection("signal")
systTree.initTreesSysts(trees, outTreeFile)

systTree.setWeightPlace(0,1.)
'''
systTree.setWeightName("btagUp",1.)
systTree.setWeightName("btagDown",1.)
systTree.setWeightName("mistagUp",1.)
systTree.setWeightName("mistagDown",1.)
systTree.setWeightName("puUp",1.)
systTree.setWeightName("puDown",1.)
'''
systTree.setWeightName("lepUp",1.)
systTree.setWeightName("lepDown",1.)


#++++++++++++++++++++++++++++++++++
#++     variables to branch      ++
#++++++++++++++++++++++++++++++++++

#Reconstructed Wprime
if MCReco:
    MC_Wprime_pt = array.array('f', [0.])
    MC_Wprime_eta = array.array('f', [0.])
    MC_Wprime_phi = array.array('f', [0.])
    MC_Wprime_m = array.array('f', [0.])
    MC_Wprime_mt = array.array('f', [0.])
closest_Wprime_pt = array.array('f', [0.])
closest_Wprime_eta = array.array('f', [0.])
closest_Wprime_phi = array.array('f', [0.])
closest_Wprime_m = array.array('f', [0.])
closest_Wprime_mt = array.array('f', [0.])
chi_Wprime_pt = array.array('f', [0.])
chi_Wprime_eta = array.array('f', [0.])
chi_Wprime_phi = array.array('f', [0.])
chi_Wprime_m = array.array('f', [0.])
chi_Wprime_mt = array.array('f', [0.])
sublead_Wprime_pt = array.array('f', [0.])
sublead_Wprime_eta = array.array('f', [0.])
sublead_Wprime_phi = array.array('f', [0.])
sublead_Wprime_m = array.array('f', [0.])
sublead_Wprime_mt = array.array('f', [0.])
best_Wprime_pt = array.array('f', [0.])
best_Wprime_eta = array.array('f', [0.])
best_Wprime_phi = array.array('f', [0.])
best_Wprime_m = array.array('f', [0.])
best_Wprime_mt = array.array('f', [0.])

#Reconstructed Top
if MCReco:
    MC_RecoTop_pt = array.array('f', [0.])
    MC_RecoTop_eta = array.array('f', [0.])
    MC_RecoTop_phi = array.array('f', [0.])
    MC_RecoTop_m = array.array('f', [0.])
    MC_RecoTop_mt = array.array('f', [0.])
    MC_RecoTop_isNeg = array.array('i', [0])
    MC_RecoTop_chi2 = array.array('i', [0])
closest_RecoTop_pt = array.array('f', [0.])
closest_RecoTop_eta = array.array('f', [0.])
closest_RecoTop_phi = array.array('f', [0.])
closest_RecoTop_m = array.array('f', [0.])
closest_RecoTop_mt = array.array('f', [0.])
closest_RecoTop_isNeg = array.array('i', [0])
closestRecoTop_chi2 = array.array('i', [0])
chi_RecoTop_pt = array.array('f', [0.])
chi_RecoTop_eta = array.array('f', [0.])
chi_RecoTop_phi = array.array('f', [0.])
chi_RecoTop_m = array.array('f', [0.])
chi_RecoTop_mt = array.array('f', [0.])
chi_RecoTop_isNeg = array.array('i', [0])
chi_RecoTop_chi2 = array.array('i', [0])
sublead_RecoTop_pt = array.array('f', [0.])
sublead_RecoTop_eta = array.array('f', [0.])
sublead_RecoTop_phi = array.array('f', [0.])
sublead_RecoTop_m = array.array('f', [0.])
sublead_RecoTop_mt = array.array('f', [0.])
sublead_RecoTop_isNeg = array.array('i', [0])
sublead_RecoTop_chi2 = array.array('i', [0])
best_RecoTop_pt = array.array('f', [0.])
best_RecoTop_eta = array.array('f', [0.])
best_RecoTop_phi = array.array('f', [0.])
best_RecoTop_m = array.array('f', [0.])
best_RecoTop_mt = array.array('f', [0.])
best_RecoTop_isNeg = array.array('i', [0])
best_RecoTop_chi2 = array.array('i', [0])

nJet = array.array('i', [0])
#Jet produced after top semilep decay
if MCReco:
    MC_TopJet_pt = array.array('f', [0.])
    MC_TopJet_eta = array.array('f', [0.])
    MC_TopJet_phi = array.array('f', [0.])
    MC_TopJet_m = array.array('f', [0.])
closest_TopJet_pt = array.array('f', [0.])
closest_TopJet_eta = array.array('f', [0.])
closest_TopJet_phi = array.array('f', [0.])
closest_TopJet_m = array.array('f', [0.])
closest_TopJet_isBTagged = array.array('i', [0])
chi_TopJet_pt = array.array('f', [0.])
chi_TopJet_eta = array.array('f', [0.])
chi_TopJet_phi = array.array('f', [0.])
chi_TopJet_m = array.array('f', [0.])
chi_TopJet_isBTagged = array.array('i', [0])
sublead_TopJet_pt = array.array('f', [0.])
sublead_TopJet_eta = array.array('f', [0.])
sublead_TopJet_phi = array.array('f', [0.])
sublead_TopJet_m = array.array('f', [0.])
sublead_TopJet_isBTagged = array.array('i', [0])
best_TopJet_pt = array.array('f', [0.])
best_TopJet_eta = array.array('f', [0.])
best_TopJet_phi = array.array('f', [0.])
best_TopJet_m = array.array('f', [0.])
best_TopJet_isBTagged = array.array('i', [0])

Event_HT = array.array('f', [0.])

'''
closest_TopJet_isDFL = array.array('i', [0])
closest_TopJet_isDFM = array.array('i', [0])
closest_TopJet_isDFT = array.array('i', [0])
closest_TopJet_isDCL = array.array('i', [0])
closest_TopJet_isDCM = array.array('i', [0])
closest_TopJet_isDCT = array.array('i', [0])
chi_TopJet_isDFL = array.array('i', [0])
chi_TopJet_isDFM = array.array('i', [0])
chi_TopJet_isDFT = array.array('i', [0])
chi_TopJet_isDCL = array.array('i', [0])
chi_TopJet_isDCM = array.array('i', [0])
chi_TopJet_isDCT = array.array('i', [0])
sublead_TopJet_isDFL = array.array('i', [0])
sublead_TopJet_isDFM = array.array('i', [0])
sublead_TopJet_isDFT = array.array('i', [0])
sublead_TopJet_isDCL = array.array('i', [0])
sublead_TopJet_isDCM = array.array('i', [0])
sublead_TopJet_isDCT = array.array('i', [0])
best_TopJet_isDFL = array.array('i', [0])
best_TopJet_isDFM = array.array('i', [0])
best_TopJet_isDFT = array.array('i', [0])
best_TopJet_isDCL = array.array('i', [0])
best_TopJet_isDCM = array.array('i', [0])
best_TopJet_isDCT = array.array('i', [0])
'''

#Prompt jet from Wprime decay
if MCReco:
    MC_WpJet_pt = array.array('f', [0.])
    MC_WpJet_eta = array.array('f', [0.])
    MC_WpJet_phi = array.array('f', [0.])
    MC_WpJet_m = array.array('f', [0.])
closest_WpJet_pt = array.array('f', [0.])
closest_WpJet_eta = array.array('f', [0.])
closest_WpJet_phi = array.array('f', [0.])
closest_WpJet_m = array.array('f', [0.])
closest_WpJet_isBTagged = array.array('i', [0])
chi_WpJet_pt = array.array('f', [0.])
chi_WpJet_eta = array.array('f', [0.])
chi_WpJet_phi = array.array('f', [0.])
chi_WpJet_m = array.array('f', [0.])
chi_WpJet_isBTagged = array.array('i', [0])
sublead_WpJet_pt = array.array('f', [0.])
sublead_WpJet_eta = array.array('f', [0.])
sublead_WpJet_phi = array.array('f', [0.])
sublead_WpJet_m = array.array('f', [0.])
sublead_WpJet_isBTagged = array.array('i', [0])
best_WpJet_pt = array.array('f', [0.])
best_WpJet_eta = array.array('f', [0.])
best_WpJet_phi = array.array('f', [0.])
best_WpJet_m = array.array('f', [0.])
best_WpJet_isBTagged = array.array('i', [0])
'''
closest_WpJet_isDFL = array.array('i', [0])
closest_WpJet_isDFM = array.array('i', [0])
closest_WpJet_isDFT = array.array('i', [0])
closest_WpJet_isDCL = array.array('i', [0])
closest_WpJet_isDCM = array.array('i', [0])
closest_WpJet_isDCT = array.array('i', [0])
chi_WpJet_isDFL = array.array('i', [0])
chi_WpJet_isDFM = array.array('i', [0])
chi_WpJet_isDFT = array.array('i', [0])
chi_WpJet_isDCL = array.array('i', [0])
chi_WpJet_isDCM = array.array('i', [0])
chi_WpJet_isDCT = array.array('i', [0])
sublead_WpJet_isDFL = array.array('i', [0])
sublead_WpJet_isDFM = array.array('i', [0])
sublead_WpJet_isDFT = array.array('i', [0])
sublead_WpJet_isDCL = array.array('i', [0])
sublead_WpJet_isDCM = array.array('i', [0])
sublead_WpJet_isDCT = array.array('i', [0])
best_WpJet_isDFL = array.array('i', [0])
best_WpJet_isDFM = array.array('i', [0])
best_WpJet_isDFT = array.array('i', [0])
best_WpJet_isDCL = array.array('i', [0])
best_WpJet_isDCM = array.array('i', [0])
best_WpJet_isDCT = array.array('i', [0])
'''

#Lepton
DetReco_Lepton_pt = array.array('f', [0.])
DetReco_Lepton_eta = array.array('f', [0.])
DetReco_Lepton_phi = array.array('f', [0.])
DetReco_Lepton_m = array.array('f', [0.])
#DetReco_Lepton_SF = array.array('f', [0.])
isEle = array.array('i', [0])
isMu = array.array('i', [0])

#MET (phi = 0, m = 0 for every event)
MET_pt = array.array('f', [0.])
MET_phi = array.array('f', [0.])
#MET_eta = array.array('f', [0.])
#MET_m = array.array('f', [0.])

w_nominal = array.array('f', [0.])
w_PDF = array.array('f', [0.]*110)
passed_mu = array.array('f', [0.])
passed_ele = array.array('f', [0.])
passed_ht = array.array('f', [0.])

#++++++++++++++++++++++++++++++++++
#++   branching the new trees    ++
#++++++++++++++++++++++++++++++++++
if MCReco:
    systTree.branchTreesSysts(trees, "signal", "MC_Wprime_pt", outTreeFile, MC_Wprime_pt)
    systTree.branchTreesSysts(trees, "signal", "MC_Wprime_eta", outTreeFile, MC_Wprime_eta)
    systTree.branchTreesSysts(trees, "signal", "MC_Wprime_phi", outTreeFile, MC_Wprime_phi)
    systTree.branchTreesSysts(trees, "signal", "MC_Wprime_m", outTreeFile, MC_Wprime_m)
    systTree.branchTreesSysts(trees, "signal", "MC_Wprime_mt", outTreeFile, MC_Wprime_mt)
systTree.branchTreesSysts(trees, "signal", "closest_Wprime_pt", outTreeFile, closest_Wprime_pt)
systTree.branchTreesSysts(trees, "signal", "closest_Wprime_eta", outTreeFile, closest_Wprime_eta)
systTree.branchTreesSysts(trees, "signal", "closest_Wprime_phi", outTreeFile, closest_Wprime_phi)
systTree.branchTreesSysts(trees, "signal", "closest_Wprime_m", outTreeFile, closest_Wprime_m)
systTree.branchTreesSysts(trees, "signal", "closest_Wprime_mt", outTreeFile, closest_Wprime_mt)
systTree.branchTreesSysts(trees, "signal", "chi_Wprime_pt", outTreeFile, chi_Wprime_pt)
systTree.branchTreesSysts(trees, "signal", "chi_Wprime_eta", outTreeFile, chi_Wprime_eta)
systTree.branchTreesSysts(trees, "signal", "chi_Wprime_phi", outTreeFile, chi_Wprime_phi)
systTree.branchTreesSysts(trees, "signal", "chi_Wprime_m", outTreeFile, chi_Wprime_m)
systTree.branchTreesSysts(trees, "signal", "chi_Wprime_mt", outTreeFile, chi_Wprime_mt)
systTree.branchTreesSysts(trees, "signal", "sublead_Wprime_pt", outTreeFile, sublead_Wprime_pt)
systTree.branchTreesSysts(trees, "signal", "sublead_Wprime_eta", outTreeFile, sublead_Wprime_eta)
systTree.branchTreesSysts(trees, "signal", "sublead_Wprime_phi", outTreeFile, sublead_Wprime_phi)
systTree.branchTreesSysts(trees, "signal", "sublead_Wprime_m", outTreeFile, sublead_Wprime_m)
systTree.branchTreesSysts(trees, "signal", "sublead_Wprime_mt", outTreeFile, sublead_Wprime_mt)
systTree.branchTreesSysts(trees, "signal", "best_Wprime_pt", outTreeFile, best_Wprime_pt)
systTree.branchTreesSysts(trees, "signal", "best_Wprime_eta", outTreeFile, best_Wprime_eta)
systTree.branchTreesSysts(trees, "signal", "best_Wprime_phi", outTreeFile, best_Wprime_phi)
systTree.branchTreesSysts(trees, "signal", "best_Wprime_m", outTreeFile, best_Wprime_m)
systTree.branchTreesSysts(trees, "signal", "best_Wprime_mt", outTreeFile, best_Wprime_mt)

systTree.branchTreesSysts(trees, "signal", "nJet", outTreeFile, nJet)
if MCReco:
    systTree.branchTreesSysts(trees, "signal", "MC_RecoTop_pt", outTreeFile, MC_RecoTop_pt)
    systTree.branchTreesSysts(trees, "signal", "MC_RecoTop_eta", outTreeFile, MC_RecoTop_eta)
    systTree.branchTreesSysts(trees, "signal", "MC_RecoTop_phi", outTreeFile, MC_RecoTop_phi)
    systTree.branchTreesSysts(trees, "signal", "MC_RecoTop_m", outTreeFile, MC_RecoTop_m)
    systTree.branchTreesSysts(trees, "signal", "MC_RecoTop_mt", outTreeFile, MC_RecoTop_mt)
    systTree.branchTreesSysts(trees, "signal", "MC_RecoTop_isNeg", outTreeFile, MC_RecoTop_isNeg)
systTree.branchTreesSysts(trees, "signal", "closest_RecoTop_pt", outTreeFile, closest_RecoTop_pt)
systTree.branchTreesSysts(trees, "signal", "closest_RecoTop_eta", outTreeFile, closest_RecoTop_eta)
systTree.branchTreesSysts(trees, "signal", "closest_RecoTop_phi", outTreeFile, closest_RecoTop_phi)
systTree.branchTreesSysts(trees, "signal", "closest_RecoTop_m", outTreeFile, closest_RecoTop_m)
systTree.branchTreesSysts(trees, "signal", "closest_RecoTop_mt", outTreeFile, closest_RecoTop_mt)
systTree.branchTreesSysts(trees, "signal", "closest_RecoTop_isNeg", outTreeFile, closest_RecoTop_isNeg)
systTree.branchTreesSysts(trees, "signal", "chi_RecoTop_pt", outTreeFile, chi_RecoTop_pt)
systTree.branchTreesSysts(trees, "signal", "chi_RecoTop_eta", outTreeFile, chi_RecoTop_eta)
systTree.branchTreesSysts(trees, "signal", "chi_RecoTop_phi", outTreeFile, chi_RecoTop_phi)
systTree.branchTreesSysts(trees, "signal", "chi_RecoTop_m", outTreeFile, chi_RecoTop_m)
systTree.branchTreesSysts(trees, "signal", "chi_RecoTop_mt", outTreeFile, chi_RecoTop_mt)
systTree.branchTreesSysts(trees, "signal", "chi_RecoTop_isNeg", outTreeFile, chi_RecoTop_isNeg)
systTree.branchTreesSysts(trees, "signal", "sublead_RecoTop_pt", outTreeFile, sublead_RecoTop_pt)
systTree.branchTreesSysts(trees, "signal", "sublead_RecoTop_eta", outTreeFile, sublead_RecoTop_eta)
systTree.branchTreesSysts(trees, "signal", "sublead_RecoTop_phi", outTreeFile, sublead_RecoTop_phi)
systTree.branchTreesSysts(trees, "signal", "sublead_RecoTop_m", outTreeFile, sublead_RecoTop_m)
systTree.branchTreesSysts(trees, "signal", "sublead_RecoTop_mt", outTreeFile, sublead_RecoTop_mt)
systTree.branchTreesSysts(trees, "signal", "sublead_RecoTop_isNeg", outTreeFile, sublead_RecoTop_isNeg)
systTree.branchTreesSysts(trees, "signal", "best_RecoTop_pt", outTreeFile, best_RecoTop_pt)
systTree.branchTreesSysts(trees, "signal", "best_RecoTop_eta", outTreeFile, best_RecoTop_eta)
systTree.branchTreesSysts(trees, "signal", "best_RecoTop_phi", outTreeFile, best_RecoTop_phi)
systTree.branchTreesSysts(trees, "signal", "best_RecoTop_m", outTreeFile, best_RecoTop_m)
systTree.branchTreesSysts(trees, "signal", "best_RecoTop_mt", outTreeFile, best_RecoTop_mt)
systTree.branchTreesSysts(trees, "signal", "best_RecoTop_isNeg", outTreeFile, best_RecoTop_isNeg)

if MCReco:
    systTree.branchTreesSysts(trees, "signal", "MC_TopJet_pt", outTreeFile, MC_TopJet_pt)
    systTree.branchTreesSysts(trees, "signal", "MC_TopJet_eta", outTreeFile, MC_TopJet_eta)
    systTree.branchTreesSysts(trees, "signal", "MC_TopJet_phi", outTreeFile, MC_TopJet_phi)
    systTree.branchTreesSysts(trees, "signal", "MC_TopJet_m", outTreeFile, MC_TopJet_m)
systTree.branchTreesSysts(trees, "signal", "closest_TopJet_pt", outTreeFile, closest_TopJet_pt)
systTree.branchTreesSysts(trees, "signal", "closest_TopJet_eta", outTreeFile, closest_TopJet_eta)
systTree.branchTreesSysts(trees, "signal", "closest_TopJet_phi", outTreeFile, closest_TopJet_phi)
systTree.branchTreesSysts(trees, "signal", "closest_TopJet_m", outTreeFile, closest_TopJet_m)
systTree.branchTreesSysts(trees, "signal", "closest_TopJet_isBTagged", outTreeFile, closest_TopJet_isBTagged)
systTree.branchTreesSysts(trees, "signal", "chi_TopJet_pt", outTreeFile, chi_TopJet_pt)
systTree.branchTreesSysts(trees, "signal", "chi_TopJet_eta", outTreeFile, chi_TopJet_eta)
systTree.branchTreesSysts(trees, "signal", "chi_TopJet_phi", outTreeFile, chi_TopJet_phi)
systTree.branchTreesSysts(trees, "signal", "chi_TopJet_m", outTreeFile, chi_TopJet_m)
systTree.branchTreesSysts(trees, "signal", "chi_TopJet_isBTagged", outTreeFile, chi_TopJet_isBTagged)
systTree.branchTreesSysts(trees, "signal", "sublead_TopJet_pt", outTreeFile, sublead_TopJet_pt)
systTree.branchTreesSysts(trees, "signal", "sublead_TopJet_eta", outTreeFile, sublead_TopJet_eta)
systTree.branchTreesSysts(trees, "signal", "sublead_TopJet_phi", outTreeFile, sublead_TopJet_phi)
systTree.branchTreesSysts(trees, "signal", "sublead_TopJet_m", outTreeFile, sublead_TopJet_m)
systTree.branchTreesSysts(trees, "signal", "sublead_TopJet_isBTagged", outTreeFile, sublead_TopJet_isBTagged)
systTree.branchTreesSysts(trees, "signal", "best_TopJet_pt", outTreeFile, best_TopJet_pt)
systTree.branchTreesSysts(trees, "signal", "best_TopJet_eta", outTreeFile, best_TopJet_eta)
systTree.branchTreesSysts(trees, "signal", "best_TopJet_phi", outTreeFile, best_TopJet_phi)
systTree.branchTreesSysts(trees, "signal", "best_TopJet_m", outTreeFile, best_TopJet_m)
systTree.branchTreesSysts(trees, "signal", "best_TopJet_isBTagged", outTreeFile, best_TopJet_isBTagged)

if MCReco:
    systTree.branchTreesSysts(trees, "signal", "MC_WpJet_pt", outTreeFile, MC_WpJet_pt)
    systTree.branchTreesSysts(trees, "signal", "MC_WpJet_eta", outTreeFile, MC_WpJet_eta)
    systTree.branchTreesSysts(trees, "signal", "MC_WpJet_phi", outTreeFile, MC_WpJet_phi)
    systTree.branchTreesSysts(trees, "signal", "MC_WpJet_m", outTreeFile, MC_WpJet_m)
systTree.branchTreesSysts(trees, "signal", "closest_WpJet_pt", outTreeFile, closest_WpJet_pt)
systTree.branchTreesSysts(trees, "signal", "closest_WpJet_eta", outTreeFile, closest_WpJet_eta)
systTree.branchTreesSysts(trees, "signal", "closest_WpJet_phi", outTreeFile, closest_WpJet_phi)
systTree.branchTreesSysts(trees, "signal", "closest_WpJet_m", outTreeFile, closest_WpJet_m)
systTree.branchTreesSysts(trees, "signal", "closest_WpJet_isBTagged", outTreeFile, closest_WpJet_isBTagged)
systTree.branchTreesSysts(trees, "signal", "chi_WpJet_pt", outTreeFile, chi_WpJet_pt)
systTree.branchTreesSysts(trees, "signal", "chi_WpJet_eta", outTreeFile, chi_WpJet_eta)
systTree.branchTreesSysts(trees, "signal", "chi_WpJet_phi", outTreeFile, chi_WpJet_phi)
systTree.branchTreesSysts(trees, "signal", "chi_WpJet_m", outTreeFile, chi_WpJet_m)
systTree.branchTreesSysts(trees, "signal", "chi_WpJet_isBTagged", outTreeFile, chi_WpJet_isBTagged)
systTree.branchTreesSysts(trees, "signal", "sublead_WpJet_pt", outTreeFile, sublead_WpJet_pt)
systTree.branchTreesSysts(trees, "signal", "sublead_WpJet_eta", outTreeFile, sublead_WpJet_eta)
systTree.branchTreesSysts(trees, "signal", "sublead_WpJet_phi", outTreeFile, sublead_WpJet_phi)
systTree.branchTreesSysts(trees, "signal", "sublead_WpJet_m", outTreeFile, sublead_WpJet_m)
systTree.branchTreesSysts(trees, "signal", "sublead_WpJet_isBTagged", outTreeFile, sublead_WpJet_isBTagged)
systTree.branchTreesSysts(trees, "signal", "best_WpJet_pt", outTreeFile, best_WpJet_pt)
systTree.branchTreesSysts(trees, "signal", "best_WpJet_eta", outTreeFile, best_WpJet_eta)
systTree.branchTreesSysts(trees, "signal", "best_WpJet_phi", outTreeFile, best_WpJet_phi)
systTree.branchTreesSysts(trees, "signal", "best_WpJet_m", outTreeFile, best_WpJet_m)
systTree.branchTreesSysts(trees, "signal", "best_WpJet_isBTagged", outTreeFile, best_WpJet_isBTagged)

systTree.branchTreesSysts(trees, "signal", "DetReco_Lepton_pt", outTreeFile, DetReco_Lepton_pt)
systTree.branchTreesSysts(trees, "signal", "DetReco_Lepton_eta", outTreeFile, DetReco_Lepton_eta)
systTree.branchTreesSysts(trees, "signal", "DetReco_Lepton_phi", outTreeFile, DetReco_Lepton_phi)
systTree.branchTreesSysts(trees, "signal", "DetReco_Lepton_m", outTreeFile, DetReco_Lepton_m)
systTree.branchTreesSysts(trees, "signal", "passed_mu", outTreeFile, passed_mu)
systTree.branchTreesSysts(trees, "signal", "passed_ele", outTreeFile, passed_ele)
systTree.branchTreesSysts(trees, "signal", "passed_ht", outTreeFile, passed_ht)
#if(isMC):
    #systTree.branchTreesSysts(trees, "signal", "DetReco_Lepton_SF", outTreeFile, DetReco_Lepton_SF)
systTree.branchTreesSysts(trees, "signal", "isEle", outTreeFile, isEle)
systTree.branchTreesSysts(trees, "signal", "isMu", outTreeFile, isMu)
systTree.branchTreesSysts(trees, "signal", "Event_HT", outTreeFile, Event_HT)
systTree.branchTreesSysts(trees, "signal", "MET_pt", outTreeFile, MET_pt)
systTree.branchTreesSysts(trees, "signal", "MET_phi", outTreeFile, MET_phi)
print "Is MC: " + str(isMC) + "      option addPDF: " + str(addPDF)
if(isMC and addPDF):
    systTree.branchTreesSysts(trees, "signal", "w_PDF", outTreeFile, w_PDF)
w_nominal[0] = 1.

#++++++++++++++++++++++++++++++++++
#++      taking MC weights       ++
#++++++++++++++++++++++++++++++++++
if(isMC):
    h_genweight = ROOT.TH1F('h_genweight_add', 'h_genweight_add', 10, 0, 10)
    h_PDFweight = ROOT.TH1F()
    h_PDFweight.SetNameTitle("h_PDFweight_add","h_PDFweight_add")
    for infile in file_list: 
        print("Getting the histos from %s" %(infile))
        newfile  = ROOT.TFile.Open(infile)
        h_genw_tmp = ROOT.TH1F(newfile.Get("plots/h_genweight"))
        h_pdfw_tmp = ROOT.TH1F(newfile.Get("plots/h_PDFweight"))
        print(ROOT.TH1F(h_PDFweight).Integral())
        if(ROOT.TH1F(h_PDFweight).Integral() < 1.):
            h_PDFweight.SetBins(h_pdfw_tmp.GetXaxis().GetNbins(), h_pdfw_tmp.GetXaxis().GetXmin(), h_pdfw_tmp.GetXaxis().GetXmax())
        print("h_genweight first bin content is %f and h_PDFweight has %f bins" %(ROOT.TH1F(newfile.Get("plots/h_genweight")).GetBinContent(1), ROOT.TH1F(newfile.Get("plots/h_PDFweight")).GetNbinsX()))
        h_genweight.Add(h_genw_tmp)
        h_PDFweight.Add(h_pdfw_tmp)
    print("h_genweight first bin content is %f and h_PDFweight has %f bins" %(h_genweight.GetBinContent(1), h_PDFweight.GetNbinsX()))

#++++++++++++++++++++++++++++++++++
#++   looping over the events    ++
#++++++++++++++++++++++++++++++++++
for i in xrange(0,tree.GetEntries()):
    #++++++++++++++++++++++++++++++++++
    #++        taking objects        ++
    #++++++++++++++++++++++++++++++++++
    if Debug and i > 1000:
        break

    event = Event(tree,i)
    electrons = Collection(event, "Electron")
    muons = Collection(event, "Muon")
    jets = Collection(event, "Jet")
    njets = len(jets)
    fatjets = Collection(event, "FatJet")
    HT = Object(event, "HT")
    PV = Object(event, "PV")
    HLT = Object(event, "HLT")
    Flag = Object(event, 'Flag')
    met = Object(event, "MET")
    MET = {'metPx': met.pt*ROOT.TMath.Cos(met.phi), 'metPy': met.pt*ROOT.TMath.Sin(met.phi)}
    genpart = None
    if isMC:
        genpart = Collection(event, "GenPart")

    #++++++++++++++++++++++++++++++++++
    #++      defining variables      ++
    #++++++++++++++++++++++++++++++++++
    tightlep = None
    tightlep_p4 = None
    tightlep_p4t = None
    tightlep_SF = None
    recomet_p4t = None

    #++++++++++++++++++++++++++++++++++
    #++    starting the analysis     ++
    #++++++++++++++++++++++++++++++++++
    VetoMu = get_LooseMu(muons)
    goodMu = get_Mu(muons)
    VetoEle = get_LooseEle(electrons)
    goodEle = get_Ele(electrons)
    year = sample.year
    if(isMC):
        runPeriod = None
    else:
        runPeriod = sample.runP
    passMu, passEle, passHT, noTrigger = trig_map(HLT, year, runPeriod)

    passed_mu[0] = int(passMu)
    passed_ele[0] = int(passEle)
    passed_ht[0] = int(passHT)

    isMuon = (len(goodMu) == 1) and (len(goodEle) == 0) and len(VetoMu) == 0 and len(VetoEle) == 0 and (passMu or passHT)
    isElectron = (len(goodMu) == 0) and (len(goodEle) == 1) and len(VetoMu) == 0 and len(VetoEle) == 0 and (passEle or passHT)
    if(isMuon):
        isEle[0] = 0
        isMu[0] = 1
        tightlep = goodMu[0]
        tightlep_p4 = ROOT.TLorentzVector()
        tightlep_p4.SetPtEtaPhiM(goodMu[0].pt,goodMu[0].eta,goodMu[0].phi,goodMu[0].mass)
        tightlep_p4t = copy.deepcopy(tightlep_p4)
        tightlep_p4t.SetPz(0.)
        if(isMC):
            tightlep_SF = goodMu[0].effSF
            systTree.setWeightName("lepUp", copy.deepcopy(tightlep_SF))
            systTree.setWeightName("lepDown", copy.deepcopy(tightlep_SF))
    elif(isElectron):
        isEle[0] = 1
        isMu[0] = 0
        tightlep = goodEle[0]
        tightlep_p4 = ROOT.TLorentzVector()
        tightlep_p4.SetPtEtaPhiM(goodEle[0].pt,goodEle[0].eta,goodEle[0].phi,goodEle[0].mass)
        tightlep_p4t = copy.deepcopy(tightlep_p4)
        tightlep_p4t.SetPz(0.)
        if(isMC):
            tightlep_SF = goodEle[0].effSF
            systTree.setWeightName("lepUp", copy.deepcopy(tightlep_SF))
            systTree.setWeightName("lepDown", copy.deepcopy(tightlep_SF))
    else:
        #print('Event %i not a good' %(i))
        continue

    recomet_p4t = ROOT.TLorentzVector()
    recomet_p4t.SetPtEtaPhiM(met.pt, 0., met.phi, 0)

    if tightlep != None:
        nJet[0] = njets
        DetReco_Lepton_pt[0] = tightlep_p4.Pt()
        DetReco_Lepton_eta[0] = tightlep_p4.Eta()
        DetReco_Lepton_phi[0] = tightlep_p4.Phi()
        DetReco_Lepton_m[0] = tightlep_p4.M()
        '''
        if(isMC):
            DetReco_Lepton_SF[0] = tightlep_SF
        '''
        MET_pt[0] = met.pt
        #MET_eta[0] = 0.
        MET_phi[0] = met.phi
        #MET_m[0] = 0.
        Event_HT[0] = HT.eventHT
    else:
        nJet[0] = -1
        DetReco_Lepton_pt[0] = -100.
        DetReco_Lepton_eta[0] = -100.
        DetReco_Lepton_phi[0] = -100.
        DetReco_Lepton_m[0] = -100.
        '''
        if(isMC):
            DetReco_Lepton_SF[0] = -100.
        '''
        MET_pt[0] = -100.
        #MET_eta[0] = -100.
        MET_phi[0] = -100.
        #MET_m[0] = -100.
        Event_HT[0] = -100.

    goodJets = get_Jet(jets, 25)
    bjets, nobjets = bjet_filter(goodJets, 'DeepFlv', 'M')
    mcbjets = None
    mclepton = None

    recotop = TopUtilities()

    #MCtruth event reconstruction                                                      
    if MCReco:
        mcbjets = mcbjet_filter(jets)

        mctfound = False
        if isMuon:
            for muon in goodMu:
                if (muon.genPartFlav == 1 or muon.genPartFlav == 15) and not mctfound:
                    mclepton = muon
                    mctfound = True
                    if mclepton.genPartIdx == -1:
                        print 'MCTruth reconstruction not properly working - lepton step'
                        continue
        elif isElectron:
            for ele in goodEle:
                if (ele.genPartFlav == 1 or ele.genPartFlav == 15) and not mctfound:
                    mclepton = ele
                    mctfound = True
                    if mclepton.genPartIdx == -1:
                        print 'MCTruth reconstruction not properly working - lepton step'
                        continue


        if mclepton is None:
            continue

        mctop_p4 = None
        mctop_p4t = None
        IsmcNeg = False
        mcpromptbjet_p4 = None
        mctopbjet_p4 = None
        mctopbjet_p4_pre = None
        mcpromptbjet_p4t = None
        bjetcheck = True
        mcbjets = mcbjet_filter(jets)
        
        if len(mcbjets)>2:
            bjetcheck = False

        mclepton_p4 = ROOT.TLorentzVector()
        mclepton_p4.SetPtEtaPhiM(mclepton.pt, mclepton.eta, mclepton.phi, mclepton.mass)

        mcWprime_p4 = ROOT.TLorentzVector()
        mcWprime_p4t = ROOT.TLorentzVector()

        topgot_ak4 = False
        Wpgot_ak4 = False

        bottjets = sameflav_filter(mcbjets, 5)
        abottjets = sameflav_filter(mcbjets, -5)

        for bjet in mcbjets:
            bjet_p4 = ROOT.TLorentzVector()
            bjet_p4.SetPtEtaPhiM(bjet.pt, bjet.eta, bjet.phi, bjet.mass)

            if abs(bjet.partonFlavour)!=5:
                print 'bfilter not properly working'
                continue

            blepflav = genpart[mclepton.genPartIdx].pdgId*bjet.partonFlavour

            if bjet.hadronFlavour == 5:
                if blepflav < 0 and not topgot_ak4:
                    mctopbjet_p4_pre = copy.deepcopy(bjet_p4)
             
                    if deltaR(bjet_p4.Eta(), bjet_p4.Phi(), mclepton_p4.Eta(), mclepton_p4.Phi()) < 0.4:
                        bjet_p4 -= mclepton_p4
                    
                    mctopbjet_p4 = bjet_p4
                    mctop_p4, IsmcNeg = recotop.top4Momentum(mclepton_p4, bjet_p4, MET['metPx'], MET['metPy'])
                    IsmcNeg = IsmcNeg*DeltaFilter

                    if mctop_p4 is None:
                        continue
                        
                    mclepton_p4t = copy.deepcopy(mclepton_p4)
                    mclepton_p4t.SetPz(0.)
                    bjet_p4t = copy.deepcopy(bjet_p4)
                    bjet_p4t.SetPz(0.)
                    met_p4t = ROOT.TLorentzVector()
                    met_p4t.SetPtEtaPhiM(met.pt, 0., met.phi, 0)
                    mctop_p4t = mclepton_p4t + bjet_p4t + met_p4t
                    if mctop_p4t.Pz() !=0:
                        mctop_p4t.SetPz(0.)
                    topgot_ak4 = True

                elif blepflav > 0 and not Wpgot_ak4:
                    mcpromptbjet_p4 = bjet_p4
                    mcpromptbjet_p4t = copy.deepcopy(bjet_p4)
                    mcpromptbjet_p4t.SetPz(0.)
                    Wpgot_ak4 = True

        if topgot_ak4 and Wpgot_ak4:
            mcWprime_p4 = mctop_p4 + mcpromptbjet_p4
            mcWprime_p4t = mctop_p4t + mcpromptbjet_p4t
            mcChi2_topmass = Chi_TopMass(mctop_p4.M())
            MC_Wprime_m[0] = mcWprime_p4.M()
            MC_Wprime_m[0] = mcWprime_p4.M()
            MC_Wprime_mt[0] = mcWprime_p4t.M()
            MC_Wprime_pt[0] = mcWprime_p4.Pt()
            MC_Wprime_eta[0] = mcWprime_p4.Eta()
            MC_Wprime_phi[0] = mcWprime_p4.Phi()
            MC_RecoTop_m[0] = mctop_p4.M()
            MC_RecoTop_mt[0] = mctop_p4t.M()
            MC_RecoTop_pt[0] = mctop_p4.Pt()
            MC_RecoTop_eta[0] = mctop_p4.Eta()
            MC_RecoTop_phi[0] = mctop_p4.Phi()
            MC_RecoTop_isNeg[0] = int(IsmcNeg)
            MC_TopJet_m[0] = mctopbjet_p4.M()
            MC_TopJet_pt[0] = mctopbjet_p4.Pt()
            MC_TopJet_eta[0] = mctopbjet_p4.Eta()
            MC_TopJet_phi[0] = mctopbjet_p4.Phi()
            MC_WpJet_m[0] = mcpromptbjet_p4.M()
            MC_WpJet_pt[0] = mcpromptbjet_p4.Pt()
            MC_WpJet_eta[0] = mcpromptbjet_p4.Eta()
            MC_WpJet_phi[0] = mcpromptbjet_p4.Phi()
        else:
            MC_Wprime_m[0] = -100.
            MC_Wprime_mt[0] = -100.
            MC_Wprime_pt[0] = -100.
            MC_Wprime_eta[0] = -100.
            MC_Wprime_phi[0] = -100.
            MC_RecoTop_m[0] = -100.
            MC_RecoTop_mt[0] = -100.
            MC_RecoTop_pt[0] = -100.
            MC_RecoTop_eta[0] = -100.
            MC_RecoTop_phi[0] = -100.
            MC_RecoTop_isNeg[0] = -1
            MC_TopJet_m[0] = -100.
            MC_TopJet_pt[0] = -100.
            MC_TopJet_eta[0] = -100.
            MC_TopJet_phi[0] = -100.
            MC_WpJet_m[0] = -100.
            MC_WpJet_pt[0] = -100.
            MC_WpJet_eta[0] = -100.
            MC_WpJet_phi[0] = -100.

    #DetReco(nstruction)
    if len(goodJets) < 2:
        continue
        
    highptJets = get_Jet(goodJets, leadingjet_ptcut)
    if len(highptJets) < 1:
        continue

    closest_promptjet = None
    closest_promptjet_p4t = None
    closest_jet_p4 = None
    closest_jet_p4t = None
    closest_jet_p4_pre = None
    chi_promptjet = None
    chi_promptjet_p4t = None
    chi_jet_p4 = None
    chi_jet_p4t = None
    chi_jet_p4_pre = None
    sublead_promptjet = highptJets[0]
    sublead_promptjet_p4t = None
    sublead_jet_p4 = None
    sublead_jet_p4t = None
    sublead_jet_p4_pre = None
    best_promptjet = None
    best_promptjet_p4t = None
    best_jet_p4 = None
    best_jet_p4t = None
    DeltaR_nujet = 100.
    DeltaR_Idx = 0
    tm_chi = 1000.
    tm_Idx = 0
    mtop_p4 = None

    btag_countings_sublead = 0
    btag_countings_closest = 0
    btag_countings_chi = 0
    btag_countings_best = 0

    #jet reconstructing top with the smallest chi2 p4                                
    for k in range(len(goodJets)):
        mtop_p4, isdetrecoNeg = recotop.top4Momentum(tightlep_p4, goodJets[k].p4(), MET['metPx'], MET['metPy'])
        if mtop_p4 is None:
            continue
        chi = Chi_TopMass(mtop_p4.M())
        if chi < tm_chi:
            tm_chi = chi
            tm_Idx = k
    
    chi_jet_p4_pre = goodJets[tm_Idx].p4()
    chi_jet = goodJets[tm_Idx]
    if deltaR(chi_jet_p4_pre.Eta(), chi_jet_p4_pre.Phi(), tightlep.eta, tightlep.phi)\
 < 0.4:
        chi_jet_p4 = chi_jet_p4_pre - tightlep_p4
    else:
        chi_jet_p4 = chi_jet_p4_pre
    if tm_Idx == 0:
        if len(highptJets) > 1:
            chi_promptjet = highptJets[1]
        else:
            chi_promptjet = goodJets[1]
    else:
        chi_promptjet = highptJets[0]
        
    chi_recotop_p4, IsNeg_chi = recotop.top4Momentum(tightlep_p4, chi_jet_p4, MET['metPx'], MET['metPy'])
    IsNeg_chi = IsNeg_chi * DeltaFilter

    btag_countings_chi = len(bjet_filter([chi_promptjet, chi_jet], 'DeepFlv', 'M'))

    chi_jet_p4t = copy.deepcopy(chi_jet_p4)
    chi_jet_p4t.SetPz(0.)
    chi_recotop_p4t = tightlep_p4t + chi_jet_p4t + recomet_p4t
    chi_promptjet_p4t = copy.deepcopy(chi_promptjet.p4())
    chi_promptjet_p4t.SetPz(0.)

    #jet closest to MET p4                                                              
    closest_jet, detrecodR = closest(tightlep, goodJets)
    closest_jet_p4_pre = closest_jet.p4()
    
    if deltaR(closest_jet.eta, closest_jet.phi, tightlep.eta, tightlep.phi) < 0.4:
        closest_jet_p4 = closest_jet_p4_pre - tightlep_p4
    else:
        closest_jet_p4 = closest_jet_p4_pre
    
    if closest_jet == goodJets[0]:
        if len(highptJets) > 1:
            closest_promptjet = highptJets[1]
        else:
            closest_promptjet = goodJets[1]
    else:
        closest_promptjet = highptJets[0]

    closest_recotop_p4, IsNeg_closest = recotop.top4Momentum(tightlep_p4, closest_jet_p4, MET['metPx'], MET['metPy'])
    IsNeg_closest = IsNeg_closest * DeltaFilter

    btag_countings_closest = len(bjet_filter([closest_promptjet, closest_jet], 'DeepFlv', 'M'))

    closest_jet_p4t = copy.deepcopy(closest_jet_p4)
    closest_jet_p4t.SetPz(0.)
    closest_recotop_p4t = tightlep_p4t + closest_jet_p4t + recomet_p4t
    closest_promptjet_p4t = copy.deepcopy(closest_promptjet.p4())
    closest_promptjet_p4t.SetPz(0.)

    #subleading jet reconstruction                                                      
    if len(highptJets) > 1:
        sublead_jet_p4_pre = highptJets[1].p4()
        sublead_jet = highptJets[1]
    else:
        sublead_jet_p4_pre = goodJets[1].p4()

        sublead_jet = goodJets[1]
    if deltaR(sublead_jet_p4_pre.Eta(), sublead_jet_p4_pre.Phi(), tightlep.eta, tightlep.phi) < 0.4:
        sublead_jet_p4 = sublead_jet_p4_pre - tightlep_p4
    else:
        sublead_jet_p4 = sublead_jet_p4_pre

    sublead_recotop_p4, IsNeg_sublead = recotop.top4Momentum(tightlep_p4, sublead_jet_p4, MET['metPx'], MET['metPy'])
    IsNeg_sublead = IsNeg_sublead * DeltaFilter

    sublead_jet_p4t = copy.deepcopy(sublead_jet_p4)
    sublead_jet_p4t.SetPz(0.)
    sublead_recotop_p4t = tightlep_p4t + sublead_jet_p4t + recomet_p4t
    sublead_promptjet_p4t = copy.deepcopy(sublead_promptjet.p4())
    sublead_promptjet_p4t.SetPz(0.)

    btag_countings_sublead = len(bjet_filter([sublead_promptjet, sublead_jet], 'DeepFlv', 'M'))

    #best jet reconstruction                                                           
    BestFound = False
    best_recotop_p4 = None
    IsNeg_best = None
    if sublead_jet_p4_pre == closest_jet_p4_pre:
        best_jet_p4 = sublead_jet_p4
        best_jet = sublead_jet
        best_promptjet = sublead_promptjet
        BestFound = True
    elif sublead_jet_p4_pre == chi_jet_p4_pre:
        best_jet_p4 = sublead_jet_p4
        best_jet = sublead_jet
        best_promptjet = sublead_promptjet
        BestFound = True
    elif chi_jet_p4_pre == closest_jet_p4_pre:
        best_jet_p4 = chi_jet_p4
        best_jet = chi_jet
        best_promptjet = chi_promptjet
        BestFound = True

    if not BestFound:
        best_jet_p4 = chi_jet_p4
        best_jet = chi_jet
        best_promptjet = chi_promptjet
        BestFound = True

    if BestFound:
        best_recotop_p4, IsNeg_best = recotop.top4Momentum(tightlep_p4, best_jet_p4, MET['metPx'], MET['metPy'])
        IsNeg_best = IsNeg_best * DeltaFilter
        best_jet_p4t = copy.deepcopy(best_jet_p4)
        best_jet_p4t.SetPz(0.)
        best_recotop_p4t = tightlep_p4t + best_jet_p4t + recomet_p4t
        best_promptjet_p4t = copy.deepcopy(best_promptjet.p4())
        best_promptjet_p4t.SetPz(0.)

        btag_countings_best = len(bjet_filter([best_promptjet, best_jet], 'DeepFlv', 'M'))

    #Wprime reco                                                                        
    if closest_recotop_p4 != None :
        closest_Wprime_p4 = closest_recotop_p4 + closest_promptjet.p4()
        closest_Wprime_p4t = closest_recotop_p4t + closest_promptjet_p4t
        closest_Wprime_m[0] = closest_Wprime_p4.M()
        closest_Wprime_mt[0] = closest_Wprime_p4t.M()
        closest_Wprime_pt[0] = closest_Wprime_p4.Pt()
        closest_Wprime_eta[0] = closest_Wprime_p4.Eta()
        closest_Wprime_phi[0] = closest_Wprime_p4.Phi()
        closest_RecoTop_m[0] = closest_recotop_p4.M()
        closest_RecoTop_mt[0] = closest_recotop_p4t.M()
        closest_RecoTop_pt[0] = closest_recotop_p4.Pt()
        closest_RecoTop_eta[0] = closest_recotop_p4.Eta()
        closest_RecoTop_phi[0] = closest_recotop_p4.Phi()
        closest_RecoTop_isNeg[0] = int(IsNeg_closest)
        closest_TopJet_m[0] = closest_jet_p4.M()
        closest_TopJet_pt[0] = closest_jet_p4.Pt()
        closest_TopJet_eta[0] = closest_jet_p4.Eta()
        closest_TopJet_phi[0] = closest_jet_p4.Phi()
        closest_TopJet_isBTagged[0] = int(len(bjet_filter([closest_jet], 'DeepFlv', 'M')))
        closest_WpJet_m[0] = closest_promptjet.p4().M()
        closest_WpJet_pt[0] = closest_promptjet.p4().Pt()
        closest_WpJet_eta[0] = closest_promptjet.p4().Eta()
        closest_WpJet_phi[0] = closest_promptjet.p4().Phi()
        closest_WpJet_isBTagged[0] = int(len(bjet_filter([closest_promptjet], 'DeepFlv', 'M')))
    else:
        closest_Wprime_m[0] = -100.
        closest_Wprime_mt[0] = -100.
        closest_Wprime_pt[0] = -100.
        closest_Wprime_eta[0] = -100.
        closest_Wprime_phi[0] = -100.
        closest_RecoTop_m[0] = -100.
        closest_RecoTop_mt[0] = -100.
        closest_RecoTop_pt[0] = -100.
        closest_RecoTop_eta[0] = -100.
        closest_RecoTop_phi[0] = -100.
        closest_RecoTop_isNeg[0] = -1
        closest_TopJet_m[0] = -100.
        closest_TopJet_pt[0] = -100.
        closest_TopJet_eta[0] = -100.
        closest_TopJet_phi[0] = -100.
        closest_TopJet_isBTagged[0] = -1
        closest_WpJet_m[0] = -100.
        closest_WpJet_pt[0] = -100.
        closest_WpJet_eta[0] = -100.
        closest_WpJet_phi[0] = -100.
        closest_WpJet_isBTagged[0] = -1

    if chi_recotop_p4 != None :
        chi_Wprime_p4 = chi_recotop_p4 + chi_promptjet.p4()
        chi_Wprime_p4t = chi_recotop_p4t + chi_promptjet_p4t
        chi_Wprime_m[0] = chi_Wprime_p4.M()
        chi_Wprime_mt[0] = chi_Wprime_p4t.M()
        chi_Wprime_pt[0] = chi_Wprime_p4.Pt()
        chi_Wprime_eta[0] = chi_Wprime_p4.Eta()
        chi_Wprime_phi[0] = chi_Wprime_p4.Phi()
        chi_RecoTop_m[0] = chi_recotop_p4.M()
        chi_RecoTop_mt[0] = chi_recotop_p4t.M()
        chi_RecoTop_pt[0] = chi_recotop_p4.Pt()
        chi_RecoTop_eta[0] = chi_recotop_p4.Eta()
        chi_RecoTop_phi[0] = chi_recotop_p4.Phi()
        chi_RecoTop_isNeg[0] = int(IsNeg_chi)
        chi_TopJet_m[0] = chi_jet_p4.M()
        chi_TopJet_pt[0] = chi_jet_p4.Pt()
        chi_TopJet_eta[0] = chi_jet_p4.Eta()
        chi_TopJet_phi[0] = chi_jet_p4.Phi()
        chi_TopJet_isBTagged[0] = int(len(bjet_filter([chi_jet], 'DeepFlv', 'M')))
        chi_WpJet_m[0] = chi_promptjet.p4().M()
        chi_WpJet_pt[0] = chi_promptjet.p4().Pt()
        chi_WpJet_eta[0] = chi_promptjet.p4().Eta()
        chi_WpJet_phi[0] = chi_promptjet.p4().Phi()
        chi_WpJet_isBTagged[0] = int(len(bjet_filter([chi_promptjet], 'DeepFlv', 'M')))
    else:
        chi_Wprime_m[0] = -100.
        chi_Wprime_mt[0] = -100.
        chi_Wprime_pt[0] = -100.
        chi_Wprime_eta[0] = -100.
        chi_Wprime_phi[0] = -100.
        chi_RecoTop_m[0] = -100.
        chi_RecoTop_mt[0] = -100.
        chi_RecoTop_pt[0] = -100.
        chi_RecoTop_eta[0] = -100.
        chi_RecoTop_phi[0] = -100.
        chi_RecoTop_isNeg[0] = -1
        chi_TopJet_m[0] = -100.
        chi_TopJet_pt[0] = -100.
        chi_TopJet_eta[0] = -100.
        chi_TopJet_phi[0] = -100.
        chi_TopJet_isBTagged[0] = -1
        chi_WpJet_m[0] = -100.
        chi_WpJet_pt[0] = -100.
        chi_WpJet_eta[0] = -100.
        chi_WpJet_phi[0] = -100.
        chi_WpJet_isBTagged[0] = -1

    if sublead_recotop_p4 != None :
        sublead_Wprime_p4 = sublead_recotop_p4 + sublead_promptjet.p4()
        sublead_Wprime_p4t = sublead_recotop_p4t + sublead_promptjet_p4t
        sublead_Wprime_m[0] = sublead_Wprime_p4.M()
        sublead_Wprime_mt[0] = sublead_Wprime_p4t.M()
        sublead_Wprime_pt[0] = sublead_Wprime_p4.Pt()
        sublead_Wprime_eta[0] = sublead_Wprime_p4.Eta()
        sublead_Wprime_phi[0] = sublead_Wprime_p4.Phi()
        sublead_RecoTop_m[0] = sublead_recotop_p4.M()
        sublead_RecoTop_mt[0] = sublead_recotop_p4t.M()
        sublead_RecoTop_pt[0] = sublead_recotop_p4.Pt()
        sublead_RecoTop_eta[0] = sublead_recotop_p4.Eta()
        sublead_RecoTop_phi[0] = sublead_recotop_p4.Phi()
        sublead_RecoTop_isNeg[0] = int(IsNeg_sublead)
        sublead_TopJet_m[0] = sublead_jet_p4.M()
        sublead_TopJet_pt[0] = sublead_jet_p4.Pt()
        sublead_TopJet_eta[0] = sublead_jet_p4.Eta()
        sublead_TopJet_phi[0] = sublead_jet_p4.Phi()
        sublead_TopJet_isBTagged[0] = int(len(bjet_filter([sublead_jet], 'DeepFlv', 'M')))
        sublead_WpJet_m[0] = sublead_promptjet.p4().M()
        sublead_WpJet_pt[0] = sublead_promptjet.p4().Pt()
        sublead_WpJet_eta[0] = sublead_promptjet.p4().Eta()
        sublead_WpJet_phi[0] = sublead_promptjet.p4().Phi()
        sublead_WpJet_isBTagged[0] = int(len(bjet_filter([sublead_promptjet], 'DeepFlv', 'M')))
    else:
        sublead_Wprime_m[0] = -100.
        sublead_Wprime_mt[0] = -100.
        sublead_Wprime_pt[0] = -100.
        sublead_Wprime_eta[0] = -100.
        sublead_Wprime_phi[0] = -100.
        sublead_RecoTop_m[0] = -100.
        sublead_RecoTop_mt[0] = -100.
        sublead_RecoTop_pt[0] = -100.
        sublead_RecoTop_eta[0] = -100.
        sublead_RecoTop_phi[0] = -100.
        sublead_RecoTop_isNeg[0] = -1
        sublead_TopJet_m[0] = -100.
        sublead_TopJet_pt[0] = -100.
        sublead_TopJet_eta[0] = -100.
        sublead_TopJet_phi[0] = -100.
        sublead_TopJet_isBTagged[0] = -1
        sublead_WpJet_m[0] = -100.
        sublead_WpJet_pt[0] = -100.
        sublead_WpJet_eta[0] = -100.
        sublead_WpJet_phi[0] = -100.
        sublead_WpJet_isBTagged[0] = -1

    if best_recotop_p4 != None :
        best_Wprime_p4 = best_recotop_p4 + best_promptjet.p4()
        best_Wprime_p4t = best_recotop_p4t + best_promptjet_p4t
        best_Wprime_m[0] = best_Wprime_p4.M()
        best_Wprime_mt[0] = best_Wprime_p4t.M()
        best_Wprime_pt[0] = best_Wprime_p4.Pt()
        best_Wprime_eta[0] = best_Wprime_p4.Eta()
        best_Wprime_phi[0] = best_Wprime_p4.Phi()
        best_RecoTop_m[0] = best_recotop_p4.M()
        best_RecoTop_mt[0] = best_recotop_p4t.M()
        best_RecoTop_pt[0] = best_recotop_p4.Pt()
        best_RecoTop_eta[0] = best_recotop_p4.Eta()
        best_RecoTop_phi[0] = best_recotop_p4.Phi()
        best_RecoTop_isNeg[0] = int(IsNeg_best)
        best_TopJet_m[0] = best_jet_p4.M()
        best_TopJet_pt[0] = best_jet_p4.Pt()
        best_TopJet_eta[0] = best_jet_p4.Eta()
        best_TopJet_phi[0] = best_jet_p4.Phi()
        best_TopJet_isBTagged[0] = int(len(bjet_filter([best_jet], 'DeepFlv', 'M')))
        best_WpJet_m[0] = best_promptjet.p4().M()
        best_WpJet_pt[0] = best_promptjet.p4().Pt()
        best_WpJet_eta[0] = best_promptjet.p4().Eta()
        best_WpJet_phi[0] = best_promptjet.p4().Phi()
        best_WpJet_isBTagged[0] = int(len(bjet_filter([best_promptjet], 'DeepFlv', 'M')))
    else:
        best_Wprime_m[0] = -100.
        best_Wprime_mt[0] = -100.
        best_Wprime_pt[0] = -100.
        best_Wprime_eta[0] = -100.
        best_Wprime_phi[0] = -100.
        best_RecoTop_m[0] = -100.
        best_RecoTop_mt[0] = -100.
        best_RecoTop_pt[0] = -100.
        best_RecoTop_eta[0] = -100.
        best_RecoTop_phi[0] = -100.
        best_RecoTop_isNeg[0] = -1
        best_TopJet_m[0] = -100.
        best_TopJet_pt[0] = -100.
        best_TopJet_eta[0] = -100.
        best_TopJet_phi[0] = -100.
        best_TopJet_isBTagged[0] = -1
        best_WpJet_m[0] = -100.
        best_WpJet_pt[0] = -100.
        best_WpJet_eta[0] = -100.
        best_WpJet_phi[0] = -100.                    
        best_WpJet_isBTagged[0] = -1
        
    systTree.setWeightPlace(0,copy.deepcopy(w_nominal[0]))
    systTree.fillTreesSysts(trees, "signal")

trees[0].Print()
outTreeFile.cd()
if(isMC):
    print("h_genweight first bin content is %f and h_PDFweight has %f bins" %(h_genweight.GetBinContent(1), h_PDFweight.GetNbinsX()))
    h_genweight.Write()
    h_PDFweight.Write()
systTree.writeTreesSysts(trees, outTreeFile)

endTime = datetime.datetime.now()
print("Ending running at " + str(endTime))
