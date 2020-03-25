import pymba
from pymba import Vimba, VimbaException
from pymba import Frame
from typing import Optional
from time import sleep
import datetime
import cv2

# ======================================================= #
# Obtain all ID's of connected Allied vision cameras
	# Note only tested on usb-connected cameras
	# For other camera types, use lsusb via commandline for listing connected devices (linux only)
# ======================================================= #
def getCameraID():

	with Vimba() as vimba:
			cameras = vimba.camera_ids()

	return cameras

# ======================================================= #
# List all the features of a given camera
	# Note not all features will be adjustable
# ======================================================= #
def listFeatures(cameraID):

	with Vimba() as vimba:
			camera = vimba.camera(cameraID)
			camera.open()

			features = []

			for feature_name in camera.feature_names():
				features.append(feature_name)

			camera.close()

	return features

# ======================================================= #
# Obtain basic information for a specific feature for a given camera
	# For more detailed information see the method below
# ======================================================= #
def getFeatureRanges(cameraID, name):

	with Vimba() as vimba:
		camera = vimba.camera(cameraID)
		camera.open()

		feature = camera.feature(name)

		try:
			value = feature.value
			range_ = feature.range
		except VimbaException as e:
			value = e
			range_ = None

		# print('\n\t'.join(
		# 	str(x) for x in (
		# 		name,
		# 		'value : {}'.format(value),
		# 		'range: {}'.format(range_))
		# 	if x is not None))

		feature_info = [value, range_]

		camera.close()

	return feature_info

# ======================================================= #
# Obtain detailed information for a specific feature of a given camera
	# Note that the output is a raw string and will need some parsing to be readable
# ======================================================= #
def getFeatureInfo(cameraID, name):

	with Vimba() as vimba:
		camera = vimba.camera(cameraID)
		camera.open()

		feature = camera.feature(name)
		featureInfo = feature.info

		camera.close()

	return featureInfo


# ======================================================= #
# Several functions for altering the default settings. 
	# Note that the ranges of some features may co-vary 
	# with other settings. 
# ======================================================= #

# ======================================================= #
# Generic function suited to any feature type 
# ======================================================= #

def setFeatureValue(cameraID, feature, value, verbose=False):

	with Vimba() as vimba:
		camera = vimba.camera(cameraID)
		camera.open()

		if verbose == True:
			feature = camera.feature(feature)
			initial = feature.value
			feature.value = value

			print(str(feature) + " is now: " + str(value) + ", was " + str(initial))

		elif verbose == False:
			feature = camera.feature(feature)
			feature.value = value

		camera.close()

# ======================================================= #
# Convenience functions for specific features
# ======================================================= #

def setExposure(cameraID, value, verbose=False):

	with Vimba() as vimba:
		camera = vimba.camera(cameraID)
		camera.open()

		if verbose == True:
			feature = camera.feature("ExposureTime")
			initial = feature.value

			feature.value = value

			print("Exposure has been changed from " + str(initial) + " to " + str(value))

		elif verbose == False:
			feature = camera.feature("ExposureTime")
			feature.value = value

		camera.close()


def setFrameRate(cameraID, value, verbose=False):

	with Vimba() as vimba:
		camera = vimba.camera(cameraID)
		camera.open()

		if verbose == True:
			feature = camera.feature("AcquisitionFrameRate")
			initial = feature.value
			feature.value = value

			print("Frame-rate has been changed from " + str(initial) + " to " + str(value))

		elif verbose == False:
			feature = camera.feature("AcquisitionFrameRate")
			feature.value = value

		camera.close()


def setAcquisitionMode(cameraID, value, verbose=False):

	with Vimba() as vimba:
		camera = vimba.camera(cameraID)
		camera.open()

		if verbose == True:
			feature = camera.feature("AcquisitionMode")
			initial = feature.value
			feature.value = value

			print("Acquisition mode has been changed from " + str(initial) + " to " + str(value))

		elif verbose == False:
			feature = camera.feature("AcquisitionMode")
			feature.value = value

		camera.close()


# ======================================================= #
# Export a single frame as a pandas csv to a folder (path)
	# Redundant with updated functions but will keep for 
	# future uses of callbacks
# ======================================================= #
def export_frame(frame, path):

	image = frame.buffer_data_numpy()

	timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%Hh%Mm%Ss%fµs')

	cv2.imwrite(path + str(timestamp) + '.jpg', image)

# ======================================================= #
# Acquire a frame from a given camera
# ======================================================= #
def acquire_frame(cameraID, path, filename=None):

	with Vimba() as vimba:
		camera = vimba.camera(cameraID)
		camera.open()

		camera.arm(mode='SingleFrame')

		frame = camera.acquire_frame()
		image = frame.buffer_data_numpy()

		if filename == None:
			timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%Hh%Mm%Ss%fµs')
			filename = path + str(timestamp) + ".jpg"
		else:
			filename = path + filename

		cv2.imwrite(filename, image)

		camera.disarm()
		camera.close()

# ======================================================= #
# Acquire a single frame and return the matrix data
# ======================================================= #
def acquire_frame_raw(cameraID):

	with Vimba() as vimba:
		camera = vimba.camera(cameraID)
		camera.open()

		camera.arm(mode='SingleFrame')

		frame = camera.acquire_frame()
		image = frame.buffer_data_numpy()

		camera.disarm()
		camera.close()

	return image

# ======================================================= #
# Acquire a single frame and return the filename
# ======================================================= #
def acquire_frame_temp(cameraID, filename):

	with Vimba() as vimba:
		camera = vimba.camera(cameraID)
		camera.open()

		camera.arm(mode='SingleFrame')

		frame = camera.acquire_frame()
		image = frame.buffer_data_numpy()

		filename = filename + '.jpg'

		cv2.imwrite(filename, image)

		camera.disarm()
		camera.close()

	return filename

# ======================================================= #
# Same as above except suited to streaming images
# ======================================================= #

# ======================================================= #
# Acquire a stream of images for a given length of time
	# and export to a path 
# ======================================================= #
def acquire_stream(cameraID, time, path):

	pixelFormatConversions = {
    		'BayerRG8': cv2.COLOR_BAYER_RG2RGB,
	}

	def export_stream(frame: Frame) -> None:

		image = frame.buffer_data_numpy()

		# Colour space conversion, perhaps not required
		try:
			image = cv2.cvtColor(image, pixelFormatConversions[frame.pixel_format])
		except:
		 	pass

		timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%Hh%Mm%Ss%fµs')
		filename = str(timestamp) + ".jpg"

		cv2.imwrite(path + filename, image)


	with Vimba() as vimba:
		camera = vimba.camera(cameraID)
		camera.open()

		camera.arm('Continuous', export_stream)
		camera.start_frame_acquisition()

		sleep(time)

		camera.stop_frame_acquisition()

		# Required to stop the session crashing
		sleep(3)

		camera.disarm()
		camera.close()
