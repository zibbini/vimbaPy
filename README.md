## vimbaPy

`vimbaPy` is a python package containing helper/convenience functions for interfacing with the two main python wrappers for the Vimba C API: `pymba` and `VimbaPython`. Differences in the implementations of either wrapper can mean that functions written in one may work better for your particular workflow, and so a combination of both wrappers may provide the most complete solution. As such, both have been included here to allow users to easily experiment with either wrapper through a simple declarative interface.

So far only USB cameras have been tested (specifically: monochrome Alvium 1800 u-500m), however all functions described in this package do not address a specific camera type so in theory should work with GigE cameras. Documentation for each sub-package can be found in the [`/docs`](https://github.com/zibbini/misc_embryoPhenomics/tree/master/python/vimbaPy/release/docs) folder. Example use cases of the package itself can be found below.

#### Important note

All functions developed for `VimbaPython` have only been tested with version 0.3.1. There is no guarantee that these functions will work for future versions of VimbaPython.

### Installation

To install the package, simply clone this repository to a suitable directory

``` shell
# Clone to desktop (for e.g.)
cd ~/Desktop

git clone https://github.com/EmbryoPhenomics/vimbaPy.git

```
and then install using pip:

``` shell

cd vimbaPy

# Uninstall any existing version of vimbaPy
pip uninstall vimbaPy 

# and install
pip install .

```

If you are on linux you may need to use root privileges:

``` shell

sudo pip install .

```

If you'd like to install `vimbaPy` for a specific python version, use the following:

``` shell
# For python 3.8
sudo -H python3.8 -m pip install .

```
##### Installing a specific module

For installing the pymba or VimbaPython module specifically, see the corresponding branches for further installation information. 

#### Known installation errors

Doing a normal pip installation may not work and so you may need to install `vimbaPy` for the version of python you intend to use (please see above). 

#### Installing pymba and VimbaPython

Please see the installation guide for installing VimbaPython [here](https://github.com/alliedvision/VimbaPython). You can install `pymba` using pip:

``` shell

pip install pymba

```

If you are on linux, you may need to use root privileges:

``` shell 

sudo pip install pymba

```

For installing vimba please see the installation guides for your OS [here](https://www.alliedvision.com/en/products/software.html#c6444).


### Example usage

All code below can be found in the `test.py` script above.

``` python

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

```

