# Documentation for pymba functions

Here you'll find the documentation for all the helper/convenience methods written for the `pymba` module, categorised by the function they fulfill. Each function contains example usage, arguments and some notes on the values returned. 

------------------------------------------------------------

## `features`

Collection of functions for retrieving summary information about a connected camera. 

#### `getCameraID()`

Retrieve the ID's of all connected cameras

##### Arguments

NaN

##### Example usage:

``` python

from vimbaPy import _pymba

# Retrieve camera ID's and print the results
print(_pymba.getCameraID())

```

#### `listFeatures()`

Retrieve all the features of a given camera. Note not all features will be mutable but will be displayed nonetheless. 

##### Arguments

* cameraID: Character string or numeric. ID of camera you'd like to obtain features from. Can be index or string. 

##### Example usage:

``` python

from vimbaPy import _pymba

# Print all the features for the default camera device (usually your webcam)
featureList = _pymba.listFeatures(cameraID=0)
print(featureList)

```

#### `getFeatureRanges()`

Retrieve both the current value and range of values for a given feature. 

##### Arguments

* cameraID: Character string or numeric. ID of camera to obtain feature info from. 
* name: Character string. Name of feature to obtain summary information from.

##### Example usage

``` python

from vimbaPy import _pymba

# Retrieve feature info for the default camera device
exposure = _pymba.getFeatureRanges(cameraID=0, name='ExposureTime')

# Print current value
print(exposure[0])

# Print the range of values
print(exposure[1])
print(exposure[1][0]) # print the min value
print(exposure[1][1]) # print the max value 

```

#### `getFeatureInfo()`

Retrieve all detailed information for a specific feature. Note that the output is a raw string and will need to parsed with regex to be readable. 

##### Arguments

* cameraID: Character string or numeric. ID of camera to obtain feature info from. 
* name: Character string. Name of feature to obtain detailed information from.

##### Example usage

``` python

from vimbaPy import _pymba

# Retrieve detailed feature info for exposure for the default camera device
exposureInfo = _pymba.getFeatureInfo(cameraID=0, name='ExposureTime')

print(exposureInfo)

```

------------------------------------------------------------


## `config`

Several convenience functions for changing the default camera settings. 

#### `setFeatureValue()`

Generic function for setting a feature to a new value. 

##### Arguments

* cameraID: Character string or numeric. ID of camera. 
* feature: Character string. Name of feature to change. 
* value: Numeric or character string. Value to set the feature to.
* verbose: Boolean. Whether to print detailed information of the changes made. Default is False.

##### Example usage

``` python

from vimbaPy import _pymba

# Set the acquisition mode to SingleFrame for the default camera device
_pymba.setFeatureValue(cameraID=0, feature='AcquisitionMode', value='SingleFrame', verboes=True)

```

#### `setExposure()`

Same as above except specifically for exposure.

##### Arguments

* cameraID: Character string or numeric. ID of camera. 
* value: Numeric or character string. Value to set the feature to.
* verbose: Boolean. Whether to print detailed information of the changes made. Default is False.


#### `setFrameRate()`

Same as above except specifically for frame rate.

##### Arguments

* cameraID: Character string or numeric. ID of camera. 
* value: Numeric or character string. Value to set the feature to.
* verbose: Boolean. Whether to print detailed information of the changes made. Default is False.

#### `setAcquisitionMode()`

Same as above except specifically for acquisition mode.

##### Arguments

* cameraID: Character string or numeric. ID of camera. 
* value: Numeric or character string. Value to set the feature to.
* verbose: Boolean. Whether to print detailed information of the changes made. Default is False.

------------------------------------------------------------

## `acquire`

Functions for acquiring frames, either individually or in a stream. Note that only `SingleFrame` and `Continous` frame acquisition formats are currently supported. Lastly, single frame acquisition may return a blank image as the frame may be captured before the camera has been properly activated. 


#### `acquire_frame()`

Acquire an individual frame from a given camera and export the image as a JPEG file to a given path. 

##### Arguments

* cameraID: Character string or numeric. ID of camera to acquire frames from.
* filename: Character string. Filename of image to export.
* path: Character string. File path to export the frame to. 

##### Example usage

``` python

from vimbaPy import _pymba

# Capture a single frame from the default camera device and export to desired path
_pymba.acquire_frame(cameraID=0, path = 'path/to/files')

```

#### `acquire_frame_raw()`

Acquire an individual frame from a given camera and return the raw image data as a matrix. 

##### Arguments

* cameraID: Character string or numeric. ID of camera to acquire frames from.

##### Example usage

``` python

from vimbaPy import _pymba

# Capture a single frame from the default camera device 
image_dat = _pymba.acquire_frame_raw(cameraID=0)

```

#### `acquire_frame_temp()`

Acquire an individual frame from a given camera and write the image to a temporary file. The filename of the image is then returned to the local session for further use e.g. plotting the image in a different software environment. 

##### Arguments

* cameraID: Character string or numeric. ID of camera to acquire frames from. 
* filename: Filename of image to export. Should use a method for generating temporary filenames on the fly, see example below. 

##### Example usage

``` R
# Example usage in R
library(reticulate)
source_python("/path/to/acquire.py")

# Capture a single frame from the default camera device and export to temporary file
acquire_frame_temp(cameraID=0, filename=tempfile())

```

#### `acquire_stream()`

Acquire a stream of frames and export to a given path as individual JPEG files. Note that this method is single-threaded and does not yet support batch acquisition, so will likely hinder the frame-rate for high-framerate acquisition projects.

##### Arguments

* cameraID: Character string or numeric. ID of camera to acquire frames from. 
* time: Time in seconds to stream/acquire frames.
* path: Path to export frames to.

##### Example usage

``` python

from vimbaPy import _pymba

# Stream and export frames from the default camera device for 5 seconds
_pymba.acquire_stream(cameraID=0, time=5, path='path/to/files')

```

------------------------------------------------------------