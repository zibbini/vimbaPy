# vimbaPy

`vimbaPy` is a python package containing helper/convenience functions for interfacing with the two main python wrappers for the Vimba C API: `pymba` and `VimbaPython`. Differences in the implementations of either wrapper can mean that functions written in one may work better for your particular workflow, and so a combination of both wrappers may provide the most complete solution. As such, both have been included here to allow users to easily experiment with either wrapper through a simple declarative interface.

So far only USB cameras have been tested (specifically: monochrome Alvium 1800 u-500m), however all functions described in this package do not address a specific camera type so in theory should work with GigE cameras. Documentation for each sub-package can be found in the [`/docs`](https://github.com/EmbryoPhenomics/vimbaPy/tree/master/docs) folder. Example use cases of the package itself can be found below.

The majority of the functionality from the previous release has been incorporated here. The only differences are in how a user addresses specific functions:

``` python
from vimbaPy import _pymba

cams = _pymba.getCameraID()
cam = _pymba.createInstance(cams[0]) 

# Display a live view for 5 seconds (first camera)
cam.stream(time=5, frame_buffer=10, callback=cam.display)

```

### Important note

All functions developed for `VimbaPython` have only been tested with version 0.3.1. There is no guarantee that these functions will work for future versions of VimbaPython.

## Installation

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
### Installing a specific module

For installing the pymba or VimbaPython module specifically, see the corresponding branches for further installation information. 

### Known installation errors

Doing a normal pip installation may not work and so you may need to install `vimbaPy` for the version of python you intend to use (please see above). 

### Installing pymba and VimbaPython

Please see the installation guide for installing VimbaPython [here](https://github.com/alliedvision/VimbaPython). You can install `pymba` using pip:

``` shell

pip install pymba

```

If you are on linux, you may need to use root privileges:

``` shell 

sudo pip install pymba

```

For installing vimba please see the installation guides for your OS [here](https://www.alliedvision.com/en/products/software.html#c6444).
