#AutoLog

## Install
####### https://tutorial.sochack.eu/en/how-to-soc/?fbclid=IwAR2nbEw_ZGRkT4yvIUGbUO_EAB9dZCUD6djgo3aBdsH0LkP4W8z1TUjqQoA
### Dependencies

#### Linux
GNU/Linux Dependencies
""""""""""""""""""""""

- Python 2.7 or more recent version
- Python distutils (standard in most Python distros, separate package python-dev in Debian)
    1) sudo apt-get install bluetooth libbluetooth-dev
- BlueZ libraries and header files

#### Windows

Windows Dependencies
""""""""""""""""""""

- Windows 7/8/8.1/10
- Python 3.5 or more recent version

PyBluez requires a C++ compiler installed on your system to build CPython modules.

For Python 3.5 or higher

- Microsoft Visual C++ 14.0 standalone: Build Tools for Visual Studio 2017 (x86, x64, ARM, ARM64)
- Microsoft Visual C++ 14.0 with Visual Studio 2017 (x86, x64, ARM, ARM64)
- Microsoft Visual C++ 14.0 standalone: Visual C++ Build Tools 2015 (x86, x64, ARM)
- Microsoft Visual C++ 14.0 with Visual Studio 2015 (x86, x64, ARM)

.. note:: Windows 10 users need to download and install the `Windows 10 SDK <https://developer.microsoft.com/en-us/windows/downloads/windows-10-sdk>`_


`More details here <https://wiki.python.org/moin/WindowsCompilers>`_

- Widcomm BTW development kit 5.0 or later (Optional)

#### macOS
macOS Dependencies
"""""""""""""""""" 
- Xcode
- PyObjc 3.1b or later (https://pythonhosted.org/pyobjc/install.html#manual-installation)