#! /bin/env cmsRun

from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing("analysis")
options.setDefault('maxEvents', 100)
options.register('skip', 0, VarParsing.multiplicity.singleton, VarParsing.varType.int, "skip N events")
options.setDefault('outputFile', 'copy.root')
options.register(
   'pick',
   '',
   VarParsing.multiplicity.list,
   VarParsing.varType.string,
   'Pick single events'
)
options.parseArguments()

import FWCore.ParameterSet.Config as cms
process = cms.Process("NOTIMPORTANT")
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
		options.inputFiles
		)
)

process.source.skipEvents = cms.untracked.uint32(options.skip)
if options.pick:
	process.source.eventsToProcess = cms.untracked.VEventRange(options.pick)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvents) )
process.out = cms.OutputModule(
	"PoolOutputModule",
	outputCommands = cms.untracked.vstring('keep *'),
	fileName = cms.untracked.string(options.outputFile)
	)
process.end = cms.EndPath(process.out)
