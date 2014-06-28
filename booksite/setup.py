#!/usr/bin/env python
import os
import sys

from setuptools import setup, find_packages
from distutils.command.install_data import install_data
from distutils.command.install import INSTALL_SCHEMES


# Make sure we're actually in the directory containing setup.py.
root_dir = os.path.dirname(__file__)

if root_dir != "":
    os.chdir(root_dir)


# Tell distutils to put the data_files in platform-specific installation
# locations. See here for an explanation:
# http://groups.google.com/group/comp.lang.python/browse_thread/thread/35ec7b2fed36eaec/2105ee4d9e8042cb
for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']


class osx_install_data(install_data):
    # On MacOS, the platform-specific lib dir is
    # /System/Library/Framework/Python/.../
    # which is wrong. Python 2.5 supplied with MacOS 10.5 has an
    # Apple-specific fix for this in distutils.command.install_data#306. It
    # fixes install_lib but not install_data, which is why we roll our own
    # install_data class.

    def finalize_options(self):
        # By the time finalize_options is called, install.install_lib is
        # set to the fixed directory, so we set the installdir to install_lib.
        # The # install_data class uses ('install_data', 'install_dir') instead.
        self.set_undefined_options('install', ('install_lib', 'install_dir'))
        install_data.finalize_options(self)


if sys.platform == "darwin":
    cmdclasses = {'install_data': osx_install_data}
else:
    cmdclasses = {'install_data': install_data}


PACKAGE_NAME = 'booksite'


# Build the reviewboard package.
setup(name=PACKAGE_NAME,
      version='0.1',
      description="book spider site Project",
      author="Ronald Bai",
      author_email="ouyanghongyu@gmail.com",
      packages=find_packages(),
      cmdclass=cmdclasses,
      install_requires=[
          'Django',
          'simplejson',
      ],
      include_package_data=True,
      zip_safe=False,
)
