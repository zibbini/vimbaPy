from vimba import *
import datetime
import time
from time import sleep
import cv2
import threading

# ======================================================= #
# Retrieve ids of all connected cameras
# ======================================================= #
def getCameraID():

	with Vimba.get_instance() as vimba:
		cams = vimba.get_all_cameras()

		cams_ID = []

		for cam in cams:
			cams_ID.append(cam.get_id())

	return cams_ID

# ======================================================= #
# List all features for a given camera
	# Note not all features will be adjustable
# ======================================================= #
def listFeatures(cameraID):

	with Vimba.get_instance() as vimba:
		with vimba.get_camera_by_id(cameraID) as cam:

			features = []

			for feature in cam.get_all_features():
				features.append(feature.get_name())

	return features

# ======================================================= #
# Obtain current value for a given feature
# ======================================================= #
def getCurrentFeatureValue(cameraID, name):

	with Vimba.get_instance() as vimba:
		with vimba.get_camera_by_id(cameraID) as cam:

			feature = cam.get_feature_by_name(feat_name=name)

			return str(feature.get())

# ======================================================= #
# Obtain range of available values for a numeric feature
# ======================================================= #
def getFeatureRange(cameraID, name):

	with Vimba.get_instance() as vimba:
		with vimba.get_camera_by_id(cameraID) as cam:

			feature = cam.get_feature_by_name(feat_name=name)

			return feature.get_range()




# ======================================================= #
# Set feature value for a given feature
# ======================================================= #
def setFeatureValue(cameraID, name, value, verbose=True):

	with Vimba.get_instance() as vimba:
		with vimba.get_camera_by_id(cameraID) as cam:

			feature = cam.get_feature_by_name(feat_name=name)

			if verbose == True:

				current = feature.get()

				feature.set(value)

				after = feature.get()

				print("Was:" + str(current) + ", now:" + str(after))

			elif verbose == False:

				feature.set(value)



# ======================================================= #
# Setup camera for OpenCV
# ======================================================= #
def setup_camera(cam: Camera):

    with cam:

        opencv_formats = intersect_pixel_formats(cam.get_pixel_formats(), OPENCV_PIXEL_FORMATS)
        color_formats = intersect_pixel_formats(opencv_formats, COLOR_PIXEL_FORMATS)

        if color_formats:
            cam.set_pixel_format(color_formats[0])

        else:
            mono_formats = intersect_pixel_formats(opencv_formats, MONO_PIXEL_FORMATS)

            if mono_formats:
                cam.set_pixel_format(mono_formats[0])

            else:
                abort('Camera does not support a OpenCV compatible format natively.')

# ======================================================= #
# Acquire a frame from a given camera and export to 'path'
# ======================================================= #
def acquire_frame(cameraID, path, filename=None, timeout_ms: int = 2000):

	with Vimba.get_instance() as vimba:
		with vimba.get_camera_by_id(cameraID) as cam:

			setup_camera(cam)

			frame = cam.get_frame(timeout_ms=timeout_ms)
			#image = frame.as_numpy_ndarray()

			if filename == None:
				timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%Hh%Mm%Ss%fµs')
				filename = path + str(timestamp) + ".jpg"
			else:
				filename = path + filename

			cv2.imwrite(filename, frame.as_opencv_image())

# ======================================================= #
# Same as above except returns filename to current environment
# ======================================================= #
def acquire_frame_file(cameraID, path, filename=None, timeout_ms: int = 2000):

	with Vimba.get_instance() as vimba:
		with vimba.get_camera_by_id(cameraID) as cam:

			setup_camera(cam)

			frame = cam.get_frame(timeout_ms=timeout_ms)
			#image = frame.as_numpy_ndarray()

			if filename == None:
				timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%Hh%Mm%Ss%fµs')
				filename = path + str(timestamp) + ".jpg"
			else:
				filename = path + filename

			cv2.imwrite(filename, frame.as_opencv_image())

	return filename

# ======================================================= #
# Same as above but for use with temp files
# ======================================================= #
def acquire_frame_temp(cameraID, filename, timeout_ms: int = 2000):

	with Vimba.get_instance() as vimba:
		with vimba.get_camera_by_id(cameraID) as cam:

			setup_camera(cam)

			frame = cam.get_frame(timeout_ms=timeout_ms)
			#image = frame.as_numpy_ndarray()

			filename = filename + '.jpg'

			cv2.imwrite(filename, frame.as_opencv_image())

	return filename

# ======================================================= #
# Acquire a frame from a given camera and return raw data
# ======================================================= #
def acquire_frame_raw(cameraID, timeout_ms: int = 2000):

	with Vimba.get_instance() as vimba:
		with vimba.get_camera_by_id(cameraID) as cam:

			setup_camera(cam)

			frame = cam.get_frame(timeout_ms=timeout_ms)
			image = frame.as_numpy_ndarray()

			return image

# ======================================================= #
# Acquire a stream of images and export
# ======================================================= #
def acquire_stream(cameraID, frame_buffer, time, path):

	def export(cam: Camera, frame: Frame):

	    if frame.get_status() == FrameStatus.Complete:

			timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%Hh%Mm%Ss%fµs')
			filename = path + str(timestamp) + ".jpg"
			cv2.imwrite(filename, frame.as_opencv_image())

	    cam.queue_frame(frame)

	with Vimba.get_instance() as vimba:
		with vimba.get_camera_by_id(cameraID) as cam:

			setup_camera(cam)

			cam.start_streaming(handler=export, buffer_count=frame_buffer)
			
			sleep(time)
	
			cam.stop_streaming()


