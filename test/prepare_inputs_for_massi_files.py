import os
import select
import ROOT
import sys
sys.path.append('..')
from objects.Payload     import Payload
from utils.beamSpotMerge import cleanAndSort
from utils.beamSpotMerge import splitByDrift
from utils.beamSpotMerge import averageBeamSpot
from utils.getFileList   import get_files

specialRuns     = [319018,319019,318984]


files  = get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/2018/StreamExpressAlignment/BS_UL2018A_HP_crab_106X_dataRun2_newTkAl_v18/190812_114423/0000/*.txt'         , prependPath=True)
files += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/2018/StreamExpressAlignment/BS_UL2018A_HP_crab_106X_dataRun2_newTkAl_v18/190812_114423/0001/*.txt'         , prependPath=True)

files += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/2018/StreamExpressAlignment/BS_UL2018B_HP_NoFill6768_6778_NoSpecialRuns_crab_106X_dataRun2_newTkAl_v18/190812_114430/0000/*.txt'      , prependPath=True)
files += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/2018/StreamExpress/BS_UL2018B_Fill6768_6778_Legacy_crab_106X_dataRun2_newTkAl_v18//190809_131128/0000/*.txt'                          , prependPath=True)

files += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/2018/StreamExpressAlignment/BS_UL2018B_SpecialRuns_Legacy_crab_106X_dataRun2_newTkAl_v18/190809_131138/0000/*.txt'         , prependPath=True)

files += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/2018/StreamExpressAlignment/BS_UL2018C_HP_crab_106X_dataRun2_newTkAl_v18/190812_114410/0000/*.txt'                   , prependPath=True)
files += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/2018/StreamExpressAlignment/BS_UL2018C_HP_crab_106X_dataRun2_newTkAl_v18/190812_114410/0001/*.txt'                   , prependPath=True)
files += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/2018/StreamExpressAlignment/BS_UL2018C_Legacy_LowPU_crab_106X_dataRun2_newTkAl_v18/190812_114437/0000/*.txt'                   , prependPath=True)

files += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/2018/StreamExpressAlignment/BS_UL2018D_HP_crab_106X_dataRun2_newTkAl_v18/190812_114357/0000/*.txt'      , prependPath=True)
files += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/2018/StreamExpressAlignment/BS_UL2018D_HP_crab_106X_dataRun2_newTkAl_v18/190812_114357/0001/*.txt'      , prependPath=True)
files += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/2018/StreamExpressAlignment/BS_UL2018D_HP_crab_106X_dataRun2_newTkAl_v18/190812_114357/0002/*.txt'      , prependPath=True)
files += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/2018/StreamExpressAlignment/BS_UL2018D_HP_crab_106X_dataRun2_newTkAl_v18/190812_114357/0003/*.txt'      , prependPath=True)
files += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/2018/StreamExpressAlignment/BS_UL2018D_HP_crab_106X_dataRun2_newTkAl_v18/190812_114357/0004/*.txt'      , prependPath=True)

files += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/2018/StreamExpressAlignment/BS_UL2018B_HP_NoFill6768_6778_NoSpecialRuns_crab_106X_dataRun2_newTkAl_v18/190812_114430/0000/*.txt'      , prependPath=True)
files += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/2018/StreamExpress/BS_UL2018B_Fill6768_6778_Legacy_crab_106X_dataRun2_newTkAl_v18//190809_131128/0000/*.txt'                          , prependPath=True)
files += get_files('/eos/cms/store/group/phys_tracking/beamspot/13TeV/2018/StreamExpressAlignment/BS_UL2018B_SpecialHV_crab_106X_dataRun2_newTkAl_v18_newCert/190820_141347/0000/*.txt'      , prependPath=True)

## HI missing


# ROOT.SetBatch(true)
print 'start loading payloads ...'
myPayload = Payload(files)
print '... payloads loaded'

ROOT.gROOT.SetBatch(True)

# convert results into a dictionary  { Run : {Lumi Range: BeamSpot Fit Object} }
allBS = myPayload.fromTextToBS() 

for irun, ivalues in allBS.iteritems():
    allBS[irun] = cleanAndSort(ivalues, cleanForSigmaZ = True)

# check drifts and create IOV
for irun, ibs in allBS.iteritems():
    fname = 'txtForMassi_UL2018/BeamFitResults_Run' + str(irun) + '.txt'
    if irun not in specialRuns:
      pairs = splitByDrift(ibs, slopes = True, maxLumi = 5)    
    else:
      pairs = splitByDrift(ibs, slopes = True, maxLumi = 1)    
    for p in pairs:
        myrange = set(range(p[0], p[1] + 1)) & set(ibs.keys())
        bs_list = [ibs[i] for i in sorted(list(myrange))]
        aveBeamSpot = averageBeamSpot(bs_list)
        aveBeamSpot.Dump(fname, 'a+')


exit()





