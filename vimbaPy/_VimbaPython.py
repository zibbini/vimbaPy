from vimba import *
import datetime
from time import sleep
import cv2
import os


def getCameraID():

	"""
	Obtain the ID's of all connected Allied Vision cameras. 

	"""

	with Vimba.get_instance() as vimba:
		cams = vimba.get_all_cameras()

		cameras = []

		for cam in cams:
			cameras.append(cam.get_id())

	return cameras

class createInstance:

	"""
	Create an independent instance for operating a given camera.

	Arguments:
		- cameraID: Character string. Camera ID for a specific camera. 
		- liveViewWidth: Numeric. Width of live camera view in pixels. Default is 520 px. 
		- liveViewHeight: Numeric. Height of live camera view in pixels. Default is 400 px.
		- path: Character string. Path to save frames. Default is current working directory.

	"""

	def __init__(self, cameraID, liveViewWidth=520, liveViewHeight=400, path=os.getcwd()):

		self.cameraID = cameraID
		self.liveViewWidth = liveViewWidth
		self.liveViewHeight = liveViewHeight
		self.path = path

	def setPath(self, path):

		"""
		Set a new path for saving frames.

		Arguments:
			- path: Character string. File path for saving frames. 

		"""

		self.path = path

	def listFeatures(self):

		"""
		List all features for the given camera. 

			Note that not all features will be adjustable. 

		"""

		with Vimba.get_instance() as vimba:
			with vimba.get_camera_by_id(self.cameraID) as cam:

				features = []

				for feature in cam.get_all_features():
					features.append(feature.get_name())

		return features

	def getFeatureInfo(self, feature):

		"""
		Retrieve some basic feature information for a given feature.

		Values are returned as a nested list, with the first slot being the 
		current value, and the second being the range. Min and max are the 
		first and second slots respectively for the latter.

		Arguments:
			- feature: Character string. Name of feature to retrieve info from.

		"""

		with Vimba.get_instance() as vimba:
			with vimba.get_camera_by_id(self.cameraID) as cam:

				feature = cam.get_feature_by_name(feat_name=feature)

				value = str(feature.get())
				range_ = feature.get_range()

				return [value, range_]

	def setSingleFeature(self, feature, value, verbose=False):

		"""
		Set the value for a given feature.

		Arguments:
			- feature: Character string. Name of feature to set value for.
			- value: Numeric or character string. New value to set feature to.
			- verbose: Boolean. Whether to print additional information. Default is False.

		"""

		with Vimba.get_instance() as vimba:
			with vimba.get_camera_by_id(self.cameraID) as cam:

				feat = cam.get_feature_by_name(feat_name=feature)

				if verbose == True:

					initial = feat.get()
					feat.set(value)

					print(str(feature) + " is now: " + str(value) + ", was " + str(initial))

				elif verbose == False:

					feat.set(value)

				else:
					print("Expected value of type Boolean. Available values for 'verbose' are True or False.")

	def setMultiFeature(self, features, verbose=False):

		"""
		Set the value for a given set of features

		Arguments:
			- features: Dictionary. Feature names and corresponding values to set them to.
			- verbose: Boolean. Whether to print additional information. Default is False.

		"""
		
		with Vimba.get_instance() as vimba:
			with vimba.get_camera_by_id(self.cameraID) as cam:

				for feature in features:

					feat = cam.get_feature_by_name(feat_name=feature)

					if verbose == True:
						initial = feat.get()
						feat.set(features[feature])

						print(str(feature) + " is now: " + str(features[feature]) + ", was " + str(initial))

					elif verbose == False:
						feat.set(features[feature])

					else:
						print("Expected value of type Boolean. Available values for 'verbose' are True or False.")

	@staticmethod
	def setup_camera(cam: Camera):

		"""
		Helper function for setting up a camera for OpenCV

		"""

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

		print("Camera setup for OpenCV complete.")

	def incompleteFrameErrorMsg(self):

		"""
		Helper function for printing a basic error message if a frame is incomplete.

		"""

		print("Acquisition at " + str(self.cameraID) + " returned incomplete frame(s).")

	def acquire_frame(self, features=None, timeout_ms=2000, path=None, filename=None, returnFilename=False):

		"""
		Acquire a frame and export to a given path.

		The path argument is optional for users who would like to export to a specific path.
		If left empty, the frame will be exported to the path specified in the given instance.
		This will be the current working directory if you did not specify path when creating the instance
		or set a new path with .setPath().

		Arguments:
			- features: Dictionary. Feature names and corresponding values to set them to.
			- timeout_ms: Numeric. Camera timeout in miliseconds. Default is 2000.
			- path: Character string. File path to save frames. Default is None.
			- filename: Character string. Filename to save frame by. Default is the current time if left as None.
			- returnFilename: Boolean. Whether to return the full file-path to the saved frame. Default is False.

		"""

		if path == None:
			path = self.path

		with Vimba.get_instance() as vimba:
			with vimba.get_camera_by_id(self.cameraID) as cam:

				if not features == None:
					for feature in features:
						feat = cam.get_feature_by_name(feat_name=feature)
						feat.set(features[feature])

				self.setup_camera(cam)

				frame = cam.get_frame(timeout_ms=2000)

				if frame.get_status() == FrameStatus.Complete:

					image = frame.as_numpy_ndarray()

					if filename == None:
						timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%Hh%Mm%Ss%fµs')
						filename = str(timestamp) + ".jpg"

					cv2.imwrite(path + filename, image)

				else:
					self.incompleteFrameErrorMsg()

		if returnFilename == True:
			return path + filename

	def display(self, cam: Camera, frame: Frame):

		"""
		Frame handler that displays frames.

		"""

		if frame.get_status() == FrameStatus.Complete:

			image = frame.as_numpy_ndarray()

			msg = "Capturing from \'{}\'."
			im_resize = cv2.resize(image, (self.liveViewWidth, self.liveViewHeight))
			cv2.imshow(msg.format(self.cameraID), im_resize)

			key = cv2.waitKey(1)

		else:
			self.incompleteFrameErrorMsg()

		cam.queue_frame(frame)

	def export(self, cam: Camera, frame: Frame):

		"""
		Frame handler that exports frames to a given path.

		"""

		if frame.get_status() == FrameStatus.Complete:	

			image = frame.as_numpy_ndarray()

			timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%Hh%Mm%Ss%fµs')
			filename = str(timestamp) + ".jpg"

			cv2.imwrite(os.path.join(self.path + filename), image)

		else:
			self.incompleteFrameErrorMsg()

		cam.queue_frame(frame)

	def export_withCounter(self, cam: Camera, frame: Frame):

		"""
		Frame handler that exports frames to a given path with 
		a counter for numbering frames.

		"""

		if frame.get_status() == FrameStatus.Complete:	

			image = frame.as_numpy_ndarray()

			filename = str(self._counter) + ".jpg"

			cv2.imwrite(os.path.join(self.path + filename), image)

			self._counter += 1

		else:
			self.incompleteFrameErrorMsg()

		cam.queue_frame(frame)

	def stream(self, time, frame_buffer, callback, features=None, path=None):

		"""
		Stream frames with a given callback (Asynchronous).

		Arguments:
			- time: Numeric. Time to stream frames.
			- frame_buffer: Numeric. Size of frame buffer. 
			- callback: Class object. Callback for handling individual frames.
			- features: Dictionary. Feature names and corresponding values to set them to.
			- path: Character string. File path to save frames. Default is path specified for the current instance.

		"""

		if not path == None:
			self.path = path

		self._counter = 1

		with Vimba.get_instance() as vimba:
			with vimba.get_camera_by_id(self.cameraID) as cam:

				if not features == None:
					for feature in features:
						feat = cam.get_feature_by_name(feat_name=feature)
						feat.set(features[feature])

				self.setup_camera(cam)

				cam.start_streaming(handler=callback, buffer_count=frame_buffer)
				
				sleep(time)
		
				cam.stop_streaming()


# # Tests
# cams = getCameraID()
# cam = cams[0]
# cam_1 = createInstance(cam)

# # cam_1.setMultiFeature(features={"ExposureTime": 5000, "BlackLevel": 0}, verbose=True)
# # cam_1.setSingleFeature(feature="ExposureTime", value=5000, verbose=True)

# cam_1.stream(
# 	time=10, 
# 	frame_buffer=200, 
# 	callback=cam_1.export_withCounter, 
# 	path="/home/z/Documents/testFrames/")
