from pymba import Vimba, VimbaException, Frame
from time import sleep
import os
import cv2
import datetime


def getCameraID():

	"""
	Obtain the ID's of all connected Allied Vision cameras. 

	"""

	with Vimba() as vimba:
			cameras = vimba.camera_ids()

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
		self.pixelFormatConversions = {'BayerRG8': cv2.COLOR_BAYER_RG2RGB}
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

		with Vimba() as vimba:

			camera = vimba.camera(self.cameraID)
			camera.open()

			features = []

			for feature_name in camera.feature_names():
				features.append(feature_name)

			camera.close()

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

		with Vimba() as vimba:
			camera = vimba.camera(self.cameraID)
			camera.open()

			feature = camera.feature(feature)

			try:
				value = feature.value
				range_ = feature.range
			except VimbaException as e:
				value = e
				range_ = None

			feature_info = [value, range_]

			camera.close()

		return feature_info

	def setFeatureValue(self, feature, value, verbose=False):

		"""
		Set the value for a given feature.

		Arguments:
			- feature: Character string. Name of feature to set value for.
			- value: Numeric or character string. New value to set feature to.
			- verbose: Boolean. Whether to print additional information. Default is False.

		"""

		with Vimba() as vimba:
			camera = vimba.camera(self.cameraID)
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

	def incompleteFrameErrorMsg(self):

		"""
		Helper function for printing a basic error message if a frame is incomplete.

		"""

		print("Acquisition at " + str(self.cameraID) + " returned incomplete frame(s).")

	def acquire_frame(self, path=None, filename=None, returnFilename=False):

		"""
		Acquire a frame and export to a given path.

		The path argument is optional for users who would like to export to a specific path.
		If left empty, the frame will be exported to the path specified in the given instance.
		This will be the current working directory if you did not specify path when creating the instance
		or set a new path with .setPath().

		Arguments:
			- path: Character string. File path to save frames. Default is None.
			- filename: Character string. Filename to save frame by. Default is the current time if left as None.
			- returnFilename: Boolean. Whether to return the full file-path to the saved frame. Default is False.

		"""

		if path == None:
			path = self.path

		with Vimba() as vimba:
			camera = vimba.camera(self.cameraID)
			camera.open()

			camera.arm(mode="SingleFrame")

			frame = camera.acquire_frame()
					
			if not frame.data.receiveStatus == -1:

				image = frame.buffer_data_numpy()

				try:
					image = cv2.cvtColor(image, self.pixelFormatConversions[frame.pixel_format])
				except:
					pass

				if filename == None:
					timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%Hh%Mm%Ss%fµs')
					filename = str(timestamp) + ".jpg"

				cv2.imwrite(path + filename, image)

			else:
				self.incompleteFrameErrorMsg()

			camera.disarm()
			camera.close()	

		if returnFilename == True:
			return path + filename		

	def display(self, frame: Frame):

		"""
		Frame handler that displays frames.

		"""

		if not frame.data.receiveStatus == -1:

			image = frame.buffer_data_numpy()

			try:
				image = cv2.cvtColor(image, self.pixelFormatConversions[frame.pixel_format])

			except:
				pass

			msg = "Capturing from \'{}\'."
			im_resize = cv2.resize(image, (self.liveViewWidth, self.liveViewHeight))
			cv2.imshow(msg.format(self.cameraID), im_resize)

			key = cv2.waitKey(1)

		else:
			self.incompleteFrameErrorMsg()


	def export(self, frame: Frame):

		"""
		Frame handler that exports frames to a given path.

		"""

		if not frame.data.receiveStatus == -1:

			image = frame.buffer_data_numpy()

			try:
				image = cv2.cvtColor(image, self.pixelFormatConversions[frame.pixel_format])
			except:
			 	pass

			timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%Hh%Mm%Ss%fµs')
			filename = str(timestamp) + ".jpg"

			cv2.imwrite(self.path + filename, image)

		else:
			self.incompleteFrameErrorMsg()

	def stream(self, time, frame_buffer, callback, path=None):

		"""
		Stream frames with a given callback (Asynchronous).

		Arguments:
			- time: Numeric. Time to stream frames.
			- frame_buffer: Numeric. Size of frame buffer. 
			- callback: Class object. Callback for handling individual frames.
			- path: Character string. File path to save frames. Default is path specified for the current instance.

		"""

		if not path == None:
			self.path = path

		with Vimba() as vimba:
			camera = vimba.camera(self.cameraID)
			camera.open()

			camera.arm('Continuous', callback, frame_buffer_size=frame_buffer)
			camera.start_frame_acquisition()

			sleep(time)

			camera.stop_frame_acquisition()

			# Required to stop the session crashing
			sleep(0.01)

			camera.disarm()
			camera.close()


# Tests
cams = getCameraID()
cam = cams[0]
cam_1 = createInstance(cam)

# cam_1.setFeatureValue(feature="ExposureTime", value=200, verbose=True)
cam_1.stream(time=5, frame_buffer=10, callback=cam_1.display)
