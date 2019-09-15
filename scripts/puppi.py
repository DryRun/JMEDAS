import FWCore.ParameterSet.Config as cms
###
### cmsRun ClusterWithToolboxAndPlot.py
###  make jet plots from miniAOD with some additional jet collections clustered 
### Jet Algorithm HATS 2015 - Dolen, Rappoccio, Stupak
### Updated for Jet Algorithm HATS 2016 - Dolen, Pilot, Kries, Perloff, Tran
###
# setenv SCRAM_ARCH slc6_amd64_gcc530
# cmsrel CMSSW_8_0_8
# cd CMSSW_8_0_8/src
# git clone git@github.com:cms-jet/JMEDAS.git Analysis/JMEDAS
# git clone git@github.com:cms-jet/JetToolbox.git Analysis/JetToolbox -b jetToolbox_763
# scram b -j 8
# cmsenv
# cd Analysis/JMEDAS/test/
# cmsRun ClusterWithToolboxAndMakeHistos.py

process = cms.Process("Ana")

### SETUP
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("Configuration.EventContent.EventContent_cff")
process.load("Configuration.StandardSequences.GeometryRecoDB_cff")
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.GlobalTag.globaltag = '94X_mc2017_realistic_v12'
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(False) )
process.options.allowUnscheduled = cms.untracked.bool(True)

### INPUT
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
#'/store/mc/RunIIFall17MiniAODv2/ZprimeToTT_M3000_W300_TuneCP2_13TeV-madgraphMLM-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/80000/0C8FF51D-9A26-E911-A64C-24BE05C626B1.root',
'/store/mc/RunIIFall17MiniAODv2/QCD_Pt_300to470_TuneCP5_13TeV_pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/10000/F2B124C3-C541-E811-8769-0025907859B4.root'
    )
)

### ADD SOME NEW JET COLLECTIONS
from Analysis.JetToolbox.jetToolbox_cff import *

# AK R=0.4 jets from Puppi inputs
jetToolbox(process, 'ak4', 'ak4PuppiJet', 'out', 
  PUMethod='Puppi',
  addPruning=False, 
  addSoftDrop=False ,           # add basic grooming
  addTrimming=False, 
  addFiltering=False, 
  addSoftDropSubjets=False,
  addNsub=True, maxTau=4,                       # add Nsubjettiness tau1, tau2, tau3, tau4
  JETCorrPayload = 'AK4PFPuppi', JETCorrLevels = ['L2Relative', 'L3Absolute']
)

# AK R=0.4 jets from CHS inputs
jetToolbox(process, 'ak4', 'ak4CHSJet', 'out', 
  PUMethod='CHS',
  addPruning=False, 
  addSoftDrop=False ,           # add basic grooming
  addTrimming=False, 
  addFiltering=False, 
  addSoftDropSubjets=False,
  addNsub=True, maxTau=4,                       # add Nsubjettiness tau1, tau2, tau3, tau4
  JETCorrPayload = 'AK4PFCHS', JETCorrLevels = ['L2Relative', 'L3Absolute']
)

### MAKE SOME HISTOGRAMS
process.ana = cms.EDAnalyzer('JetTester')

### OUT
process.TFileService = cms.Service("TFileService",
      fileName = cms.string("puppi_histograms.root"),
      closeFileFast = cms.untracked.bool(True)
  )

# Uncomment the following line if you would like to output the jet collections in a root file
process.endpath = cms.EndPath(process.out) 

process.p = cms.Path(process.ana)