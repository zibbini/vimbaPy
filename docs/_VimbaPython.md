# Documentation for VimbaPython functions

Here you'll find the documentation for all the helper/convenience methods written for the `VimbaPython` module, categorised by the function they fulfill. Each function contains example usage, arguments and some notes on the values returned. 

------------------------------------------------------------

## `features`

Collection of functions for retrieving summary information about a connected camera. 

#### `getCameraID()`

Retrieve the ID's of all connected cameras

##### Arguments

NaN

##### Example usage:

``` python

from vimbaPy import _VimbaPython

# Retrieve camera ID's and print the results
print(_VimbaPython.getCameraID())

```

#### `listFeatures()`

Retrieve all the features of a given camera. Note not all features will be mutable but will be returned nonetheless. 

##### Arguments

* cameraID: Character string or numeric. ID of camera you'd like to obtain features from. Can be index or string. 

##### Example usage:

``` python

from vimbaPy import _VimbaPython

# Use the first camera
cams = _VimbaPython.getCameraID()
cam = cams[0]

# Print all the features for the default camera device (usually your webcam)
featureList = _VimbaPython.listFeatures(cameraID=cam)
print(featureList)

```

#### `getCurrentFeatureValue()`

Retrieve the current value of a specified feature for a given camera.

##### Arguments

* cameraID: Character string or numeric. ID of camera.
* name: Character string. Name of feature.

##### Example usage

``` python

from vimbaPy import _VimbaPython

# Use the first camera
cams = _VimbaPython.getCameraID()
cam = cams[0]

# Retrieve feature info for the default camera device
exposure = _VimbaPython.getFeatureRanges(cameraID=cam, name='ExposureTime')

# Print current value
print(exposure)

```

#### `getFeatureRange()`

Retrieve the range of values available for a given numeric feature. Note that this method will not work with other feature types e.g. Boolean. 

##### Arguments

* cameraID: Character string or numeric. ID of camera. 
* name: Character string. Name of feature. 

##### Example usage

``` python

from vimbaPy import _VimbaPython

# Use the first camera
cams = _VimbaPython.getCameraID()
cam = cams[0]

# Retrieve detailed feature info for exposure for the default camera device
exposureInfo = _VimbaPython.getFeatureInfo(cameraID=cam, name='ExposureTime')

print(exposureInfo)

```

------------------------------------------------------------


## `set_features`

Convenience function for changing the default camera settings. 

#### `setFeatureValue()`

Generic function for setting a feature to a new value. 

##### Arguments

* cameraID: Character string or numeric. ID of camera. 
* feature: Character string. Name of feature to change. 
* value: Numeric or character string. Value to set the feature to.
* verbose: Boolean. Whether to print detailed information of the changes made. Default is False.

##### Example usage

``` python

from vimbaPy import _VimbaPython

# Use the first camera
cams = _VimbaPython.getCameraID()
cam = cams[0]

# Set the acquisition mode to SingleFrame for the default camera device
_VimbaPython.setFeatureValue(cameraID=cam, feature='AcquisitionMode', value='SingleFrame', verboes=True)

```

------------------------------------------------------------


## `acquire`

Functions for acquiring frames, either individually or in a stream. Note that single frame acquisition may return a blank image as the frame may be captured before the camera has been properly activated. 


#### `acquire_frame()`

Acquire an individual frame from a given camera and export the image as a JPEG file to a given path. 

##### Arguments

* cameraID: Character string or numeric. ID of camera to acquire frames from.
* path: Character string. File path to export the frame to. 
* filename: Character string. Default is None. Filename of image to export. 
* timeout_ms: Numeric. Default is 2000. Timeout in milliseconds of frame acquisition.

##### Example usage

``` python

from vimbaPy import _VimbaPython

# Use the first camera
cams = _VimbaPython.getCameraID()
cam = cams[0]

# Capture a single frame from the default camera device and export to desired path
_VimbaPython.acquire_frame(cameraID=cam, path = 'path/to/files')

```

#### `acquire_frame_raw()`

Acquire an individual frame from a given camera and return the raw image data as a matrix. 

##### Arguments

* cameraID: Character string or numeric. ID of camera to acquire frames from.
* timeout_ms: Numeric. Default is 2000. Timeout in milliseconds of frame acquisition.

##### Example usage

``` python

from vimbaPy import _VimbaPython

# Use the first camera
cams = _VimbaPython.getCameraID()
cam = cams[0]

# Capture a single frame from the default camera device 
image_dat = _VimbaPython.acquire_frame_raw(cameraID=cam)

```

#### `acquire_frame_temp()`

Acquire an individual frame from a given camera and write the image to a temporary file. The filename of the image is then returned to the local session for further use e.g. plotting the image in a different software environment. 

##### Arguments

* cameraID: Character string or numeric. ID of camera to acquire frames from. 
* filename: Filename of image to export. Should use a method for generating temporary filenames on the fly, see example below. 
* timeout_ms: Numeric. Default is 2000. Timeout in milliseconds of frame acquisition.

##### Example usage

``` R
# Example usage in R
library(reticulate)
source_python("/path/to/_VimbaPython.py")

cam <- getCameraID()

# Capture a single frame from the default camera device and export to temporary file
acquire_frame_temp(cameraID=cam, filename=tempfile())

```

#### `acquire_stream()`

Acquire a stream of frames and export to a given path as individual JPEG files. 

##### Arguments

* cameraID: Character string or numeric. ID of camera to acquire frames from. 
* buffer: Number of frames supplied as internal buffer.
* time: Time in seconds to stream/acquire frames.
* path: Path to export frames to.

##### Example usage

``` python

from vimbaPy import _VimbaPython

# Use the first camera
cams = _VimbaPython.getCameraID()
cam = cams[0]

# Stream and export frames from the default camera device for 5 seconds
_VimbaPython.acquire_stream(cameraID=cam, buffer=10, time=5, path='path/to/files')

```

------------------------------------------------------------