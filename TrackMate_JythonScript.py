#### set parameters:
### spot detection 
DO_SUBPIXEL_LOCALIZATION = True
RADIUS = 7.5
THRESHOLD = 0.5
DO_MEDIAN_FILTERING = False
#TARGET_CHANNEL = 1			### commented out here because given as function in initiating script
### LAP tracker
LINKING_MAX_DISTANCE = 15.0
#gap closing
ALLOW_GAP_CLOSING = True
GAP_CLOSING_MAX_DISTANCE = 15.0
MAX_FRAME_GAP = 2	# only parameter that I've modified
#splitting
ALLOW_TRACK_SPLITTING = False	#was true... do I want to allow splitting or not?? Doesn't currently work with XY-extractor
SPLITTING_MAX_DISTANCE = 15.0
#merging
ALLOW_TRACK_MERGING = False
MERGING_MAX_DISTANCE = 15.0


import sys
from ij import IJ, ImagePlus, ImageStack, WindowManager
from fiji.plugin.trackmate import Model, Settings, TrackMate, SelectionModel, Logger
from fiji.plugin.trackmate.detection import LogDetectorFactory, DogDetectorFactory
from fiji.plugin.trackmate.tracking.sparselap import SparseLAPTrackerFactory
from fiji.plugin.trackmate.tracking.oldlap import LAPTrackerFactory
from fiji.plugin.trackmate.tracking import LAPUtils
from fiji.plugin.trackmate.visualization.hyperstack import HyperStackDisplayer
from fiji.plugin.trackmate.features import FeatureFilter


from fiji.plugin.trackmate.io import TmXmlReader, TmXmlWriter
from fiji.plugin.trackmate.util import TMUtils
from fiji.plugin.trackmate.action import ExportStatsToIJAction, ExportTracksToXML
from fiji.plugin.trackmate.detection import DetectorKeys

from fiji.plugin.trackmate.features import FeatureAnalyzer, ModelFeatureUpdater, SpotFeatureCalculator
from fiji.plugin.trackmate.features.spot import SpotContrastAndSNRAnalyzerFactory, SpotContrastAndSNRAnalyzer
from fiji.plugin.trackmate.features.track import TrackDurationAnalyzer, TrackSpeedStatisticsAnalyzer



IJ.log("\\Clear")

# Get currently selected image
imp = WindowManager.getCurrentImage()
#imp = IJ.openImage('http://fiji.sc/samples/FakeTracks.tif')
#imp.show()


#----------------------------
# Create the model object now
#----------------------------

# Some of the parameters we configure below need to have
# a reference to the model at creation. So we create an
# empty model now.

model = Model()

# Send all messages to ImageJ log window.
model.setLogger(Logger.IJ_LOGGER)



#------------------------
# Prepare settings object
#------------------------

settings = Settings()
settings.setFrom(imp)

# Configure detector - We use the Strings for the keys
settings.detectorFactory = LogDetectorFactory()
settings.detectorSettings = { 
    'DO_SUBPIXEL_LOCALIZATION' : DO_SUBPIXEL_LOCALIZATION,
    'RADIUS' : RADIUS,
    'TARGET_CHANNEL' : TARGET_CHANNEL,
    'THRESHOLD' : THRESHOLD,
    'DO_MEDIAN_FILTERING' : DO_MEDIAN_FILTERING,
}  





# Configure spot filters - Classical filter on quality
# I don't want to filter out anything
#filter1 = FeatureFilter('QUALITY', 30, True)
#settings.addSpotFilter(filter1)

# Configure tracker - We want to allow merges and fusions
#		from http://forum.imagej.net/t/trackmate-scripting-automatically-exporting-spots-in-tracks-links-in-tracks-tracks-statistics-and-branching-analysis-to-csv/6256
settings.trackerFactory = LAPTrackerFactory()
settings.trackerSettings = LAPUtils.getDefaultLAPSettingsMap() # almost good enough
#print(LAPUtils.getDefaultLAPSettingsMap())

settings.trackerSettings['LINKING_MAX_DISTANCE'] = LINKING_MAX_DISTANCE
settings.trackerSettings['LINKING_FEATURE_PENALTIES'] = {}
#gap closing
settings.trackerSettings['ALLOW_GAP_CLOSING'] = ALLOW_GAP_CLOSING
settings.trackerSettings['GAP_CLOSING_MAX_DISTANCE'] = GAP_CLOSING_MAX_DISTANCE
settings.trackerSettings['MAX_FRAME_GAP'] = MAX_FRAME_GAP
settings.trackerSettings['GAP_CLOSING_FEATURE_PENALTIES'] = {}
#splitting
settings.trackerSettings['ALLOW_TRACK_SPLITTING'] = ALLOW_TRACK_SPLITTING
settings.trackerSettings['SPLITTING_MAX_DISTANCE'] = SPLITTING_MAX_DISTANCE
settings.trackerSettings['SPLITTING_FEATURE_PENALTIES'] = {}
#merging
settings.trackerSettings['ALLOW_TRACK_MERGING'] = ALLOW_TRACK_MERGING
settings.trackerSettings['MERGING_MAX_DISTANCE'] = MERGING_MAX_DISTANCE
settings.trackerSettings['MERGING_FEATURE_PENALTIES'] = {}
#etc
#settings.trackerSettings['ALTERNATIVE_LINKING_COST_FACTOR'] = 1.05
#settings.trackerSettings['BLOCKING_VALUE'] = Infinity
#settings.trackerSettings['CUTOFF_PERCENTILE'] = 0.9




### I'm skipping all of this, I want all data outputted and will filter later on in other scripts
## Configure track analyzers - Later on we want to filter out tracks 
## based on their displacement, so we need to state that we want 
## track displacement to be calculated. By default, out of the GUI, 
## not features are calculated. 

## The displacement feature is provided by the TrackDurationAnalyzer.

#settings.addTrackAnalyzer(TrackDurationAnalyzer())

## Configure track filters - We want to get rid of the two immobile spots at 
## the bottom right of the image. Track displacement must be above 10 pixels.

#filter2 = FeatureFilter('TRACK_DISPLACEMENT', 10, True)
#settings.addTrackFilter(filter2)


#-------------------
# Instantiate plugin
#-------------------

trackmate = TrackMate(model, settings)

#--------
# Process
#--------

ok = trackmate.checkInput()
if not ok:
    sys.exit("A:" + str(trackmate.getErrorMessage()))

ok = trackmate.process()
if not ok:
    sys.exit("B: " + str(trackmate.getErrorMessage()))


#----------------
# Display results
#----------------

selectionModel = SelectionModel(model)
displayer =  HyperStackDisplayer(model, selectionModel, imp)
displayer.render()
displayer.refresh()

# Echo results with the logger we set at start:
model.getLogger().log(str(model))

# Export stats to results table
### UNDER CONSTRUCTION
ExportStatsToIJAction().execute(trackmate)




IJ.log("\nTracker settings as follows:")
for x in settings.trackerSettings:
	IJ.log(' - ' + x + ' : ' + str(settings.trackerSettings[x]))

IJ.log("\nDetector settings as follows:")
for x in settings.detectorSettings:
	IJ.log(' - ' + x + ' : ' + str(settings.detectorSettings[x]))
IJ.log("")




#try:
#	savedir
#except NameError:
#	savedir = IJ.getDirectory("")	# this needs to be better defined!
#
#IJ.selectWindow("Spots in tracks statistics")
#savename = savedir + "track stats.csv"
#IJ.saveAs("results",savename)
#
#IJ.log("\nspot stats saved as: "+savename)
#
#
#
#IJ.log("\n\n\n---SCRIPT FINISHED---")
#print("---SCRIPT FINISHED---")