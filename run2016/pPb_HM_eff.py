import FWCore.ParameterSet.Config as cms

Noff = cms.EDProducer("QWNtrkOfflineProducer",
    vertexSrc = cms.untracked.InputTag("offlinePrimaryVertices"),
    trackSrc  = cms.untracked.InputTag("generalTracks")
    )


QWEvent = cms.EDProducer("QWEventProducer",
    vertexSrc = cms.untracked.InputTag('offlinePrimaryVertices', ""),
    trackSrc = cms.untracked.InputTag('generalTracks'),
    fweight = cms.untracked.InputTag('Hijing_8TeV_MB_eff_v2.root'),
    centralitySrc = cms.untracked.InputTag("Noff"),
    dzdzerror = cms.untracked.double(3.0),
    d0d0error = cms.untracked.double(3.0),
    pterrorpt = cms.untracked.double(0.1),
    ptMin = cms.untracked.double(0.3),
    ptMax= cms.untracked.double(3.0),
    Etamin = cms.untracked.double(-2.4),
    Etamax = cms.untracked.double(2.4)
    )

makeEvent = cms.Sequence(Noff*QWEvent)

# monitoring
histNoff = cms.EDAnalyzer('QWHistAnalyzer',
    src = cms.untracked.InputTag("Noff"),
    Nbins = cms.untracked.int32(600),
    start = cms.untracked.double(0),
    end = cms.untracked.double(600)
    )

vectPhi = cms.EDAnalyzer('QWVectorAnalyzer',
    src = cms.untracked.InputTag("QWEvent", "phi"),
    hNbins = cms.untracked.int32(5000),
    hstart = cms.untracked.double(0),
    hend = cms.untracked.double(5000),
    cNbins = cms.untracked.int32(1000),
    cstart = cms.untracked.double(-3.14159265358979323846),
    cend = cms.untracked.double(3.14159265358979323846)
    )

vectPt = cms.EDAnalyzer('QWVectorAnalyzer',
    src = cms.untracked.InputTag("QWEvent", "pt"),
    hNbins = cms.untracked.int32(5000),
    hstart = cms.untracked.double(0),
    hend = cms.untracked.double(5000),
    cNbins = cms.untracked.int32(1000),
    cstart = cms.untracked.double(0),
    cend = cms.untracked.double(5)
    )

vectEta = cms.EDAnalyzer('QWVectorAnalyzer',
    src = cms.untracked.InputTag("QWEvent", "eta"),
    hNbins = cms.untracked.int32(5000),
    hstart = cms.untracked.double(0),
    hend = cms.untracked.double(5000),
    cNbins = cms.untracked.int32(1000),
    cstart = cms.untracked.double(-2.5),
    cend = cms.untracked.double(2.5)
    )

vectEtaW = vectEta.clone( srcW = cms.untracked.InputTag("QWEvent", "weight") )
vectPtW = vectPt.clone( srcW = cms.untracked.InputTag("QWEvent", "weight") )
vectPhiW = vectPhi.clone( srcW = cms.untracked.InputTag("QWEvent", "weight") )

vectMon = cms.Sequence(histNoff*vectPhi*vectPt*vectEta)
vectMonW = cms.Sequence(histNoff*vectPhi*vectPt*vectEta*vectPhiW*vectPtW*vectEtaW)
