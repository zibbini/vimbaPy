from vimbaPy import _pymba, _VimbaPython

# Print connected cameras using both modules
print(_pymba.getCameraID())
print(_VimbaPython.getCameraID())

# Grab first camera ID
cam = _pymba.getCameraID()
cam = cam[0]

# Print some feature information
print(_pymba.getFeatureRanges(cameraID=cam, name="ExposureAuto"))
print(_pymba.getFeatureRanges(cameraID=cam, name="ExposureTime"))
print(_pymba.getFeatureRanges(cameraID=cam, name="AcquisitionFrameRate"))
print(_pymba.getFeatureRanges(cameraID=cam, name="Gain"))
print(_pymba.getFeatureRanges(cameraID=cam, name="BlackLevel"))
print(_pymba.getFeatureRanges(cameraID=cam, name="AcquisitionMode")) 

# Turn off automatic exposure adjustment for streaming below
_VimbaPython.setFeatureValue(cameraID=cam, name="ExposureAuto", value="Off", verbose=True)

# Set feature values for max fps
_VimbaPython.setFeatureValue(cameraID=cam, name='ExposureTime', value=2000, verbose=True)
_VimbaPython.setFeatureValue(cameraID=cam, name='Gain', value=0, verbose=True)

# Stream images to disk for 5 seconds (Asynchronous)
_VimbaPython.acquire_stream(
	cameraID=cam, 
	frame_buffer=10, 
	time=5, 
	path='/home/z/Documents/testFrames/')

# Same as above but with pymba
_pymba.acquire_stream(
	cameraID=cam, 
	time=5, 
	path='/home/z/Documents/testFrames/')

# Check the frame rate obtained with exposure of 2000 nano S
print(_pymba.getFeatureRanges(cameraID=cam, name="AcquisitionFrameRate"))