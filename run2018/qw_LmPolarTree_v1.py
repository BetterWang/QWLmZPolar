import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

process = cms.Process("LmPolar")

process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load("TrackingTools/TransientTrack/TransientTrackBuilder_cfi")
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')

options = VarParsing.VarParsing('analysis')

options.register('rap',
                'Mid',
                VarParsing.VarParsing.multiplicity.singleton,
                VarParsing.VarParsing.varType.string,
                "Mid/Fwd")

options.register('BDT',
                0.20,
                VarParsing.VarParsing.multiplicity.singleton,
                VarParsing.VarParsing.varType.float,
                "BDT cut")

options.parseArguments()

print options.rap
print options.BDT


process.load("RecoHI.HiEvtPlaneAlgos.HiEvtPlane_cfi")
process.load("RecoHI.HiEvtPlaneAlgos.hiEvtPlaneFlat_cfi")

process.load("CondCore.CondDB.CondDB_cfi")

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.MessageLogger.cerr.FwkReport.reportEvery = 100

from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '103X_dataRun2_Prompt_v2', '')

process.GlobalTag.snapshotTime = cms.string("9999-12-31 23:59:59.000")
process.GlobalTag.toGet.extend([
	cms.PSet(record = cms.string("HeavyIonRcd"),
		tag = cms.string("CentralityTable_HFtowers200_DataPbPb_periHYDJETshape_run2v1033p1x01_offline"),
		connect = cms.string("frontier://FrontierProd/CMS_CONDITIONS"),
		label = cms.untracked.string("HFtowers")
		),
	])

process.CondDB.connect = "sqlite_file:HeavyIonRPRcd_PbPb2018_offline.db"
process.PoolDBESSource = cms.ESSource("PoolDBESSource",
        process.CondDB,
        toGet = cms.VPSet(
            cms.PSet(
                record = cms.string('HeavyIonRPRcd'),
                tag = cms.string('HeavyIonRPRcd')
                )
            )
        )
process.es_prefer_flatparms = cms.ESPrefer('PoolDBESSource','')

process.hiEvtPlane.trackTag = cms.InputTag("generalTracks")
process.hiEvtPlane.vertexTag = cms.InputTag("offlinePrimaryVerticesRecovery")
process.hiEvtPlane.loadDB = cms.bool(True)
process.hiEvtPlane.useNtrk = cms.untracked.bool(False)
process.hiEvtPlane.caloCentRef = cms.double(-1)
process.hiEvtPlane.caloCentRefWidth = cms.double(-1)
process.hiEvtPlaneFlat.caloCentRef = cms.double(-1)
process.hiEvtPlaneFlat.caloCentRefWidth = cms.double(-1)
process.hiEvtPlaneFlat.vertexTag = cms.InputTag("offlinePrimaryVerticesRecovery")
process.hiEvtPlaneFlat.useNtrk = cms.untracked.bool(False)


process.load("RecoHI.HiCentralityAlgos.CentralityBin_cfi")
process.centralityBin.Centrality = cms.InputTag("hiCentrality")
process.centralityBin.centralityVariable = cms.string("HFtowers")

process.options = cms.untracked.PSet(
        SkipEvent = cms.untracked.vstring('ProductNotFound')
        )

process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring("file:/afs/cern.ch/user/q/qwang/work/cleanroomRun2/Ana/data/PbPb2018_RERECO_V0Skim.root"),
        secondaryFileNames = cms.untracked.vstring(
            "file:/eos/cms/store/group/phys_heavyions/qwang/data/FF31F840-542E-1A49-ACF7-9043F8169E67.root"
            ),
        inputCommands=cms.untracked.vstring(
            'keep *',
            'drop *_hiEvtPlane_*_*'
            )
        )

process.TFileService = cms.Service("TFileService",
        fileName = cms.string('cumu.root')
        )

process.load('HeavyIonsAnalysis.Configuration.hfCoincFilter_cff')
process.load('HeavyIonsAnalysis.Configuration.collisionEventSelection_cff')
process.load('RecoHI.HiCentralityAlgos.CentralityFilter_cfi')
process.load('PbPb18_HIMB_rereco')

process.eventSelection = cms.Sequence(
	process.primaryVertexFilter
	* process.hfCoincFilter2Th4
	* process.clusterCompatibilityFilter
    )

process.QWVertex = cms.EDProducer('QWVertexProducer',
        vertexSrc = cms.untracked.InputTag('offlinePrimaryVerticesRecovery')
        )

process.QWPrimaryVz = cms.EDProducer('QWVectorSelector',
        vectSrc = cms.untracked.InputTag('QWVertex', 'vz'),
        )

process.QWVzFilter15 = cms.EDFilter('QWDoubleFilter',
        src = cms.untracked.InputTag('QWPrimaryVz'),
        dmin = cms.untracked.double(-15.),
        dmax = cms.untracked.double(15.),
        )

process.QWPrimaryVertexSelection = cms.Sequence (process.QWVertex * process.QWPrimaryVz * process.QWVzFilter15)

process.Cent0 = process.centralityFilter.clone(
        selectedBins = cms.vint32(
            *range(0, 20)
            ),
        BinLabel = cms.InputTag("centralityBin", "HFtowers")
        )

process.Cent10 = process.centralityFilter.clone(
        selectedBins = cms.vint32(
            *range(20, 60)
            ),
        BinLabel = cms.InputTag("centralityBin", "HFtowers")
        )

process.Cent30 = process.centralityFilter.clone(
        selectedBins = cms.vint32(
            *range(60, 100)
            ),
        BinLabel = cms.InputTag("centralityBin", "HFtowers")
        )

process.Cent50 = process.centralityFilter.clone(
        selectedBins = cms.vint32(
            *range(100, 160)
            ),
        BinLabel = cms.InputTag("centralityBin", "HFtowers")
        )

process.Cent80 = process.centralityFilter.clone(
        selectedBins = cms.vint32(
            *range(160, 200)
            ),
        BinLabel = cms.InputTag("centralityBin", "HFtowers")
        )

process.vectMass0  = process.vectMassLm.clone();
process.vectMass10 = process.vectMassLm.clone();
process.vectMass30 = process.vectMassLm.clone();
process.vectMass50 = process.vectMassLm.clone();
process.vectMass80 = process.vectMassLm.clone();

process.vectMon0  = cms.Sequence( process.vectMass0 );
process.vectMon10 = cms.Sequence( process.vectMass10);
process.vectMon30 = cms.Sequence( process.vectMass30);
process.vectMon50 = cms.Sequence( process.vectMass50);
process.vectMon80 = cms.Sequence( process.vectMass80);


process.QWV0Event = process.QWV0EventLm.clone()

if options.rap == 'Fwd':
    process.QWV0Event.cuts[0].AbsRapmax = cms.untracked.double(2.0)
    process.QWV0Event.cuts[0].AbsRapmin = cms.untracked.double(1.0)

process.QWV0MVA = cms.EDProducer('QWV0MVAVectProducer'
        , vertexSrc = cms.untracked.InputTag('offlinePrimaryVerticesRecovery')
        , V0Src = cms.untracked.InputTag('QWV0Event', 'Lambda')
        , dbCent = cms.untracked.InputTag('dbCent')
        , mvaXML = cms.untracked.string('MC_Full_BDT250_D4.LM.weights.xml')
        , mvaCut = cms.untracked.double(options.BDT)
        )

process.QWV0MVAVector = cms.EDProducer('QWV0VectProducer'
        , vertexSrc = cms.untracked.InputTag('offlinePrimaryVerticesRecovery')
        , trackSrc = cms.untracked.InputTag('generalTracks')
        , V0Src = cms.untracked.InputTag('QWV0MVA', 'Lambda')
        , daughter_cuts = cms.untracked.PSet(
            )
        , cuts = cms.untracked.VPSet(
            cms.untracked.PSet(
                )
            )
        )

process.EPOrg = cms.EDProducer('QWEvtPlaneProducer',
        src = cms.untracked.InputTag('hiEvtPlaneFlat'),
        level = cms.untracked.int32(0)
        )

process.EPFlat = cms.EDProducer('QWEvtPlaneProducer',
        src = cms.untracked.InputTag('hiEvtPlaneFlat'),
        level = cms.untracked.int32(2)
        )

process.QWEventInfo = cms.EDProducer('QWEventInfoProducer')

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
                tag = cms.untracked.InputTag('QWV0Event', 'pdgId'),
                name = cms.untracked.string('pdgId')
                ),
            cms.PSet(
                tag = cms.untracked.InputTag('QWV0Event', 'pTrkPt'),
                name = cms.untracked.string('pTrkPt')
                ),
            cms.PSet(
                tag = cms.untracked.InputTag('QWV0Event', 'pTrkPx'),
                name = cms.untracked.string('pTrkPx')
                ),
            cms.PSet(
                tag = cms.untracked.InputTag('QWV0Event', 'pTrkPy'),
                name = cms.untracked.string('pTrkPy')
                ),
            cms.PSet(
                tag = cms.untracked.InputTag('QWV0Event', 'pTrkPz'),
                name = cms.untracked.string('pTrkPz')
                ),
            cms.PSet(
                tag = cms.untracked.InputTag('QWV0Event', 'pTrkEta'),
                name = cms.untracked.string('pTrkEta')
                ),
            cms.PSet(
                tag = cms.untracked.InputTag('QWV0Event', 'nTrkPt'),
                name = cms.untracked.string('nTrkPt')
                ),
            cms.PSet(
                tag = cms.untracked.InputTag('QWV0Event', 'nTrkPx'),
                name = cms.untracked.string('nTrkPx')
                ),
            cms.PSet(
                tag = cms.untracked.InputTag('QWV0Event', 'nTrkPy'),
                name = cms.untracked.string('nTrkPy')
                ),
            cms.PSet(
                tag = cms.untracked.InputTag('QWV0Event', 'nTrkPz'),
                name = cms.untracked.string('nTrkPz')
                ),
            cms.PSet(
                tag = cms.untracked.InputTag('QWV0Event', 'nTrkEta'),
                name = cms.untracked.string('nTrkEta')
                ),
            cms.PSet(
                tag = cms.untracked.InputTag('QWV0Event', 'pPxCM'),
                name = cms.untracked.string('pPxCM')
                ),
            cms.PSet(
                tag = cms.untracked.InputTag('QWV0Event', 'pPyCM'),
                name = cms.untracked.string('pPyCM')
                ),
            cms.PSet(
                tag = cms.untracked.InputTag('QWV0Event', 'pPzCM'),
                name = cms.untracked.string('pPzCM')
                ),
            cms.PSet(
                tag = cms.untracked.InputTag('QWV0Event', 'nPxCM'),
                name = cms.untracked.string('nPxCM')
                ),
            cms.PSet(
                tag = cms.untracked.InputTag('QWV0Event', 'nPyCM'),
                name = cms.untracked.string('nPyCM')
                ),
            cms.PSet(
                tag = cms.untracked.InputTag('QWV0Event', 'nPzCM'),
                name = cms.untracked.string('nPzCM')
                ),
            cms.PSet(
                tag = cms.untracked.InputTag('QWV0Event', 'pt'),
                name = cms.untracked.string('pt')
                ),
            cms.PSet(
                tag = cms.untracked.InputTag('QWV0Event', 'phi'),
                name = cms.untracked.string('phi')
                ),
            cms.PSet(
                tag = cms.untracked.InputTag('QWV0Event', 'eta'),
                name = cms.untracked.string('eta')
                ),
            cms.PSet(
                tag = cms.untracked.InputTag('QWV0Event', 'rapidity'),
                name = cms.untracked.string('rapidity')
                ),
            cms.PSet(
                tag = cms.untracked.InputTag('QWV0Event', 'mass'),
                name = cms.untracked.string('mass')
                ),
        ),
        Dtags = cms.untracked.VPSet(
            cms.PSet(
                tag = cms.untracked.InputTag('dbCent'),
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

process.ana0 = cms.Path(
        process.eventSelection
        * process.QWPrimaryVertexSelection
        * process.Cent0
        * process.dbCent
        * process.QWV0Event
        * process.QWV0MVA
        * process.QWV0MVAVector
        * process.hiEvtPlane
        * process.hiEvtPlaneFlat
        * process.EPOrg
        * process.EPFlat
        * process.QWEventInfo
        * process.tree
        * process.histCentBin
        * process.vectMon0
        )

process.ana10 = cms.Path(
        process.eventSelection
        * process.QWPrimaryVertexSelection
        * process.Cent10
        * process.dbCent
        * process.QWV0Event
        * process.QWV0MVA
        * process.QWV0MVAVector
        * process.hiEvtPlane
        * process.hiEvtPlaneFlat
        * process.EPOrg
        * process.EPFlat
        * process.QWEventInfo
        * process.tree
        * process.histCentBin
        * process.vectMon10
        )

process.ana30 = cms.Path(
        process.eventSelection
        * process.QWPrimaryVertexSelection
        * process.Cent30
        * process.dbCent
        * process.QWV0Event
        * process.QWV0MVA
        * process.QWV0MVAVector
        * process.hiEvtPlane
        * process.hiEvtPlaneFlat
        * process.EPOrg
        * process.EPFlat
        * process.QWEventInfo
        * process.tree
        * process.histCentBin
        * process.vectMon30
        )

process.ana50 = cms.Path(
        process.eventSelection
        * process.QWPrimaryVertexSelection
        * process.Cent50
        * process.dbCent
        * process.QWV0Event
        * process.QWV0MVA
        * process.QWV0MVAVector
        * process.hiEvtPlane
        * process.hiEvtPlaneFlat
        * process.EPOrg
        * process.EPFlat
        * process.QWEventInfo
        * process.tree
        * process.histCentBin
        * process.vectMon50
        )

process.ana80 = cms.Path(
        process.eventSelection
        * process.QWPrimaryVertexSelection
        * process.Cent80
        * process.dbCent
        * process.QWV0Event
        * process.QWV0MVA
        * process.QWV0MVAVector
        * process.hiEvtPlane
        * process.hiEvtPlaneFlat
        * process.EPOrg
        * process.EPFlat
        * process.QWEventInfo
        * process.tree
        * process.histCentBin
        * process.vectMon80
        )



process.schedule = cms.Schedule(
        process.ana0,
        process.ana10,
        process.ana30,
        process.ana50,
        process.ana80,
#        process.out
        )

from HLTrigger.Configuration.CustomConfigs import MassReplaceInputTag
process = MassReplaceInputTag(process,"offlinePrimaryVertices","offlinePrimaryVerticesRecovery")

