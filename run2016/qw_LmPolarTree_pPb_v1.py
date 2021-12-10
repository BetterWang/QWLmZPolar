import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

process = cms.Process("CumuV3")

process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load("TrackingTools/TransientTrack/TransientTrackBuilder_cfi")
process.load("Configuration.Geometry.GeometryDB_cff")
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.load("CondCore.CondDB.CondDB_cfi")
process.load("RecoHI.HiEvtPlaneAlgos.HiEvtPlane_cfi")
process.load("RecoHI.HiEvtPlaneAlgos.hiEvtPlaneFlat_cfi")

options = VarParsing.VarParsing('analysis')
options.register('HLT',
                'HM120',
                VarParsing.VarParsing.multiplicity.singleton,
                VarParsing.VarParsing.varType.string,
                "HM120, HM150, HM185, HM250")

options.parseArguments()

dbTag = 'NA'
if options.HLT == 'HM120':
    dbTag = 'HeavyIonRPRcd_pPb2016_HM120_offline'
if options.HLT == 'HM150':
    dbTag = 'HeavyIonRPRcd_pPb2016_HM150_offline'
if options.HLT == 'HM185':
    dbTag = 'HeavyIonRPRcd_pPb2016_HM185_offline'
if options.HLT == 'HM250':
    dbTag = 'HeavyIonRPRcd_pPb2016_HM250_offline'

print options.HLT
print dbTag

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '80X_dataRun2_Prompt_v16', '')

#process.CondDB.connect = "sqlite_file:HeavyIonRPRcd_pPb2016_HM120_offline.db"
process.CondDB.connect = "sqlite_file:"+dbTag+".db"
process.PoolDBESSource = cms.ESSource("PoolDBESSource",
    process.CondDB,
    toGet = cms.VPSet(
        cms.PSet(
            record = cms.string('HeavyIonRPRcd'),
            tag = cms.string(dbTag)
            )
        )
    )
process.es_prefer_flatparms = cms.ESPrefer('PoolDBESSource','')

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.MessageLogger.cerr.FwkReport.reportEvery = 100

process.options = cms.untracked.PSet(
    SkipEvent = cms.untracked.vstring('ProductNotFound')
    )

process.source = cms.Source("PoolSource",
#        fileNames = cms.untracked.vstring("file:/afs/cern.ch/user/q/qwang/work/cleanroomRun2/Ana/data/pPb_V0_v1.root"),
        fileNames = cms.untracked.vstring("/store/user/davidlw/PAHighMultiplicity0/RecoSkim2016_pPb_V0Cascade_v1/170301_201930/0000/pPb_HM_28.root"),
	secondaryFileNames = cms.untracked.vstring(
#		'file:/eos/cms/store/hidata/PARun2016C/PAHighMultiplicity0/AOD/PromptReco-v1/000/285/479/00000/3AB7179C-DCAE-E611-980E-FA163EC8DDF7.root',
#		'file:/eos/cms/store/hidata/PARun2016C/PAHighMultiplicity0/AOD/PromptReco-v1/000/285/480/00000/0E343491-06AF-E611-AF4F-FA163E0C8993.root',
#		'file:/eos/cms/store/hidata/PARun2016C/PAHighMultiplicity0/AOD/PromptReco-v1/000/285/480/00000/CAAC6AB7-06AF-E611-A23C-FA163EA53949.root',
#		'file:/eos/cms/store/hidata/PARun2016C/PAHighMultiplicity0/AOD/PromptReco-v1/000/285/480/00000/D0F23BC7-06AF-E611-8D86-FA163EA3E531.root',
#		'file:/eos/cms/store/hidata/PARun2016C/PAHighMultiplicity0/AOD/PromptReco-v1/000/285/480/00000/FE0873CE-06AF-E611-92B7-02163E0140FE.root'
		'file:/eos/cms/store/hidata/PARun2016C/PAHighMultiplicity0/AOD/PromptReco-v1/000/285/480/00000/AC8FA173-08AF-E611-94F2-02163E014561.root',
		'file:/eos/cms/store/hidata/PARun2016C/PAHighMultiplicity0/AOD/PromptReco-v1/000/285/480/00000/A417C575-08AF-E611-9BFC-FA163E05A16C.root',
		'file:/eos/cms/store/hidata/PARun2016C/PAHighMultiplicity0/AOD/PromptReco-v1/000/285/480/00000/34DF5A88-08AF-E611-BC70-FA163E5AF33F.root',
		'file:/eos/cms/store/hidata/PARun2016C/PAHighMultiplicity0/AOD/PromptReco-v1/000/285/480/00000/1E07EF6E-08AF-E611-A8B7-FA163EFF24E2.root',
		)
    )

import HLTrigger.HLTfilters.hltHighLevel_cfi
process.hltHM120 = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone()
process.hltHM120.HLTPaths = [
	"HLT_PAFullTracks_Multiplicity120_v*",
#	"HLT_PAFullTracks_Multiplicity150_v*",
#	"HLT_PAFullTracks_Multiplicity185_*",
#	"HLT_PAFullTracks_Multiplicity220_v*",
#	"HLT_PAFullTracks_Multiplicity250_v*",
#	"HLT_PAFullTracks_Multiplicity280_v*",
]
process.hltHM120.andOr = cms.bool(True)
process.hltHM120.throw = cms.bool(False)

process.hltHM150 = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone()
process.hltHM150.HLTPaths = [
	"HLT_PAFullTracks_Multiplicity120_v*",
	"HLT_PAFullTracks_Multiplicity150_v*",
#	"HLT_PAFullTracks_Multiplicity185_*",
#	"HLT_PAFullTracks_Multiplicity220_v*",
#	"HLT_PAFullTracks_Multiplicity250_v*",
#	"HLT_PAFullTracks_Multiplicity280_v*",
]
process.hltHM150.andOr = cms.bool(True)
process.hltHM150.throw = cms.bool(False)

process.hltHM185 = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone()
process.hltHM185.HLTPaths = [
#	"HLT_PAFullTracks_Multiplicity120_v*",
#	"HLT_PAFullTracks_Multiplicity150_v*",
	"HLT_PAFullTracks_Multiplicity185_*",
#	"HLT_PAFullTracks_Multiplicity220_v*",
#	"HLT_PAFullTracks_Multiplicity250_v*",
#	"HLT_PAFullTracks_Multiplicity280_v*",
]
process.hltHM185.andOr = cms.bool(True)
process.hltHM185.throw = cms.bool(False)

process.hltHM250 = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone()
process.hltHM250.HLTPaths = [
#	"HLT_PAFullTracks_Multiplicity120_v*",
#	"HLT_PAFullTracks_Multiplicity150_v*",
#	"HLT_PAFullTracks_Multiplicity185_*",
#	"HLT_PAFullTracks_Multiplicity220_v*",
	"HLT_PAFullTracks_Multiplicity250_v*",
#	"HLT_PAFullTracks_Multiplicity280_v*",
]
process.hltHM250.andOr = cms.bool(True)
process.hltHM250.throw = cms.bool(False)


process.TFileService = cms.Service("TFileService",
    fileName = cms.string('cumu.root')
    )

process.load("HeavyIonsAnalysis.VertexAnalysis.PAPileUpVertexFilter_cff")

process.PAprimaryVertexFilter = cms.EDFilter("VertexSelector",
    src = cms.InputTag("offlinePrimaryVertices"),
    cut = cms.string("!isFake && abs(z) <= 25 && position.Rho <= 2 && tracksSize >= 2"),
    filter = cms.bool(True), # otherwise it won't filter the events
    )

process.NoScraping = cms.EDFilter("FilterOutScraping",
    applyfilter = cms.untracked.bool(True),
    debugOn = cms.untracked.bool(False),
    numtrack = cms.untracked.uint32(10),
    thresh = cms.untracked.double(0.25)
    )

process.QWVertex = cms.EDProducer('QWVertexProducer',
    vertexSrc = cms.untracked.InputTag('offlinePrimaryVertices')
	)
process.QWPrimaryVz = cms.EDProducer('QWVectorSelector',
    vectSrc = cms.untracked.InputTag('QWVertex', 'vz'),
	)
process.QWVzFilter15 = cms.EDFilter('QWDoubleFilter',
    src = cms.untracked.InputTag('QWPrimaryVz'),
    dmin = cms.untracked.double(-15.),
    dmax = cms.untracked.double(15.),
	)
process.QWPrimaryVertexSelection = cms.Sequence( process.QWVertex * process.QWPrimaryVz * process.QWVzFilter15 )

process.load("HeavyIonsAnalysis.Configuration.hfCoincFilter_cff")
process.load("HeavyIonsAnalysis.VertexAnalysis.pileUpFilter_cff")

process.eventSelection = cms.Sequence(process.hfCoincFilter * process.PAprimaryVertexFilter * process.NoScraping * process.olvFilter_pPb8TeV_dz1p0 * process.QWPrimaryVertexSelection)

process.load('RecoHI.HiCentralityAlgos.CentralityFilter_cfi')
process.ppNoffFilter120 = process.centralityFilter.clone(
    selectedBins = cms.vint32(
        *range(120, 150)
        ),
    BinLabel = cms.InputTag("Noff")
    )

process.ppNoffFilter150 = process.centralityFilter.clone(
    selectedBins = cms.vint32(
        *range(150, 185)
        ),
    BinLabel = cms.InputTag("Noff")
    )

process.ppNoffFilter185 = process.centralityFilter.clone(
    selectedBins = cms.vint32(
        *range(185, 250)
    ),
    BinLabel = cms.InputTag("Noff")
    )

process.ppNoffFilter250 = process.centralityFilter.clone(
    selectedBins = cms.vint32(
        *range(250, 320)
        ),
    BinLabel = cms.InputTag("Noff")
    )

process.QWV0EventLambda = cms.EDProducer('QWV0VectProducer',
    vertexSrc = cms.untracked.InputTag('offlinePrimaryVertices'),
    trackSrc = cms.untracked.InputTag('generalTracks'),
    V0Src = cms.untracked.InputTag('generalV0CandidatesNew', 'Lambda'),
    daughter_cuts = cms.untracked.PSet(
        ),
    cuts = cms.untracked.VPSet(
        cms.untracked.PSet(
            Massmin = cms.untracked.double(1.08),
            Massmax = cms.untracked.double(1.16),
            DecayXYZMin = cms.untracked.double(5.0),
            ThetaXYZMin = cms.untracked.double(0.999),
            ptMin = cms.untracked.double(0.2),
            ptMax = cms.untracked.double(8.5),
            Rapmin = cms.untracked.double(-1.0),
            Rapmax = cms.untracked.double(1.0)
            )
        ),
    )

process.vectMassLm120 = cms.EDAnalyzer('QWMassAnalyzer',
    srcMass = cms.untracked.InputTag("QWV0EventLambda", "mass"),
    srcPt   = cms.untracked.InputTag("QWV0EventLambda", "pt"),
    srcEta  = cms.untracked.InputTag("QWV0EventLambda", "rapidity"),
    srcPhi  = cms.untracked.InputTag("QWV0EventLambda", "phi"),
    Nbins   = cms.untracked.int32(160),
    start   = cms.untracked.double(1.08),
    end     = cms.untracked.double(1.16),
    )

process.vectMassLm150 = process.vectMassLm120.clone()
process.vectMassLm185 = process.vectMassLm120.clone()
process.vectMassLm250 = process.vectMassLm120.clone()

process.tree = cms.EDAnalyzer('QWTreeMaker',
        Vtags = cms.untracked.VPSet(
            cms.PSet(
                tag = cms.untracked.InputTag('EPOrg', 'angle'),
                name = cms.untracked.string('EPOrg')
            ),
            cms.PSet(
                tag = cms.untracked.InputTag('EPOrg', 'sumSin'),
                name = cms.untracked.string('EPOrgSin')
            ),
            cms.PSet(
                tag = cms.untracked.InputTag('EPOrg', 'sumCos'),
                name = cms.untracked.string('EPOrgCos')
            ),
            cms.PSet(
                tag = cms.untracked.InputTag('EPFlat', 'angle'),
                name = cms.untracked.string('EPFlat')
            ),
            cms.PSet(
                tag = cms.untracked.InputTag('EPFlat', 'sumSin'),
                name = cms.untracked.string('EPFlatSin')
            ),
            cms.PSet(
                tag = cms.untracked.InputTag('EPFlat', 'sumCos'),
                name = cms.untracked.string('EPFlatCos')
            ),
            cms.PSet(
                tag = cms.untracked.InputTag('QWV0EventLambda', 'pdgId'),
                name = cms.untracked.string('pdgId')
                ),
            cms.PSet(
                tag = cms.untracked.InputTag('QWV0EventLambda', 'pTrkPt'),
                name = cms.untracked.string('pTrkPt')
                ),
            cms.PSet(
                tag = cms.untracked.InputTag('QWV0EventLambda', 'pTrkPx'),
                name = cms.untracked.string('pTrkPx')
                ),
            cms.PSet(
                tag = cms.untracked.InputTag('QWV0EventLambda', 'pTrkPy'),
                name = cms.untracked.string('pTrkPy')
                ),
            cms.PSet(
                tag = cms.untracked.InputTag('QWV0EventLambda', 'pTrkPz'),
                name = cms.untracked.string('pTrkPz')
                ),
            cms.PSet(
                tag = cms.untracked.InputTag('QWV0EventLambda', 'pTrkEta'),
                name = cms.untracked.string('pTrkEta')
                ),
            cms.PSet(
                tag = cms.untracked.InputTag('QWV0EventLambda', 'nTrkPt'),
                name = cms.untracked.string('nTrkPt')
                ),
            cms.PSet(
                tag = cms.untracked.InputTag('QWV0EventLambda', 'nTrkPx'),
                name = cms.untracked.string('nTrkPx')
                ),
            cms.PSet(
                tag = cms.untracked.InputTag('QWV0EventLambda', 'nTrkPy'),
                name = cms.untracked.string('nTrkPy')
                ),
            cms.PSet(
                tag = cms.untracked.InputTag('QWV0EventLambda', 'nTrkPz'),
                name = cms.untracked.string('nTrkPz')
                ),
            cms.PSet(
                tag = cms.untracked.InputTag('QWV0EventLambda', 'nTrkEta'),
                name = cms.untracked.string('nTrkEta')
                ),
            cms.PSet(
                tag = cms.untracked.InputTag('QWV0EventLambda', 'pPxCM'),
                name = cms.untracked.string('pPxCM')
                ),
            cms.PSet(
                tag = cms.untracked.InputTag('QWV0EventLambda', 'pPyCM'),
                name = cms.untracked.string('pPyCM')
                ),
            cms.PSet(
                tag = cms.untracked.InputTag('QWV0EventLambda', 'pPzCM'),
                name = cms.untracked.string('pPzCM')
                ),
            cms.PSet(
                tag = cms.untracked.InputTag('QWV0EventLambda', 'nPxCM'),
                name = cms.untracked.string('nPxCM')
                ),
            cms.PSet(
                tag = cms.untracked.InputTag('QWV0EventLambda', 'nPyCM'),
                name = cms.untracked.string('nPyCM')
                ),
            cms.PSet(
                tag = cms.untracked.InputTag('QWV0EventLambda', 'nPzCM'),
                name = cms.untracked.string('nPzCM')
                ),
            cms.PSet(
                tag = cms.untracked.InputTag('QWV0EventLambda', 'pt'),
                name = cms.untracked.string('pt')
                ),
            cms.PSet(
                tag = cms.untracked.InputTag('QWV0EventLambda', 'phi'),
                name = cms.untracked.string('phi')
                ),
            cms.PSet(
                tag = cms.untracked.InputTag('QWV0EventLambda', 'eta'),
                name = cms.untracked.string('eta')
                ),
            cms.PSet(
                tag = cms.untracked.InputTag('QWV0EventLambda', 'rapidity'),
                name = cms.untracked.string('rapidity')
                ),
            cms.PSet(
                tag = cms.untracked.InputTag('QWV0EventLambda', 'mass'),
                name = cms.untracked.string('mass')
                ),
        ),
        Dtags = cms.untracked.VPSet(
            cms.PSet(
                tag = cms.untracked.InputTag('dbNoff'),
                name = cms.untracked.string('Cent')
                ),
            cms.PSet(
                tag = cms.untracked.InputTag('QWPrimaryVz'),
                name = cms.untracked.string('vz')
                ),
            cms.PSet(
                tag = cms.untracked.InputTag('QWEventInfo', 'RunId'),
                name = cms.untracked.string('RunId')
                ),
            cms.PSet(
                tag = cms.untracked.InputTag('QWEventInfo', 'EventId'),
                name = cms.untracked.string('EventId')
                ),
            cms.PSet(
                tag = cms.untracked.InputTag('QWEventInfo', 'Lumi'),
                name = cms.untracked.string('Lumi')
                ),
            )
    )

process.QWEventInfo = cms.EDProducer('QWEventInfoProducer')

process.EPOrg = cms.EDProducer('QWEvtPlaneProducer',
        src = cms.untracked.InputTag('hiEvtPlaneFlat'),
        level = cms.untracked.int32(0)
        )

process.EPFlat = cms.EDProducer('QWEvtPlaneProducer',
        src = cms.untracked.InputTag('hiEvtPlaneFlat'),
        level = cms.untracked.int32(2)
        )

process.hiEvtPlane.trackTag = cms.InputTag("generalTracks")
process.hiEvtPlane.vertexTag = cms.InputTag("offlinePrimaryVertices")
process.hiEvtPlane.loadDB = cms.bool(True)
process.hiEvtPlane.useNtrk = cms.untracked.bool(True)
process.hiEvtPlaneFlat.vertexTag = cms.InputTag("offlinePrimaryVertices")
process.hiEvtPlaneFlat.useNtrk = cms.untracked.bool(True)

process.Noff = cms.EDProducer("QWNtrkOfflineProducer",
    vertexSrc = cms.untracked.InputTag("offlinePrimaryVertices"),
    trackSrc  = cms.untracked.InputTag("generalTracks")
    )

process.dbNoff = cms.EDProducer('QWInt2Double',
    src = cms.untracked.InputTag('Noff')
    )

process.ana120 = cms.Path(
    process.hltHM120
    * process.eventSelection
    * process.Noff
    * process.ppNoffFilter120
    * process.dbNoff
    * process.QWV0EventLambda
    * process.QWEventInfo
    * process.hiEvtPlane
    * process.hiEvtPlaneFlat
    * process.EPOrg
    * process.EPFlat
    * process.tree
    * process.vectMassLm120
    )

process.ana150 = cms.Path(
    process.hltHM150
    * process.eventSelection
    * process.Noff
    * process.ppNoffFilter150
    * process.dbNoff
    * process.QWV0EventLambda
    * process.QWEventInfo
    * process.hiEvtPlane
    * process.hiEvtPlaneFlat
    * process.EPOrg
    * process.EPFlat
    * process.tree
    * process.vectMassLm120
    )

process.ana185 = cms.Path(
    process.hltHM185
    * process.eventSelection
    * process.Noff
    * process.ppNoffFilter185
    * process.dbNoff
    * process.QWV0EventLambda
    * process.QWEventInfo
    * process.hiEvtPlane
    * process.hiEvtPlaneFlat
    * process.EPOrg
    * process.EPFlat
    * process.tree
    * process.vectMassLm120
    )

process.ana250 = cms.Path(
    process.hltHM250
    * process.eventSelection
    * process.Noff
    * process.ppNoffFilter250
    * process.dbNoff
    * process.QWV0EventLambda
    * process.QWEventInfo
    * process.hiEvtPlane
    * process.hiEvtPlaneFlat
    * process.EPOrg
    * process.EPFlat
    * process.tree
    * process.vectMassLm120
    )

if options.HLT == "HM120":
    process.schedule = cms.Schedule(process.ana120)
if options.HLT == "HM150":
    process.schedule = cms.Schedule(process.ana150)
if options.HLT == "HM185":
    process.schedule = cms.Schedule(process.ana185)
if options.HLT == "HM250":
    process.schedule = cms.Schedule(process.ana250)
