Get GeckoDriver
=================
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/get-gecko-driver?color=blue)](https://pypi.python.org/pypi/get-gecko-driver)
[![PyPI](https://img.shields.io/pypi/v/get-gecko-driver?color=blue)](https://pypi.python.org/pypi/get-gecko-driver)
[![PyPI - Status](https://img.shields.io/pypi/status/get-gecko-driver)](https://pypi.python.org/pypi/get-gecko-driver)
[![PyPI - License](https://img.shields.io/pypi/l/get-gecko-driver)](https://pypi.python.org/pypi/get-gecko-driver)

A tool to download GeckoDriver. You can use this tool as a package import or as a command-line application.

## Install

To install:

```console
$ pip install get-gecko-driver
```

To upgrade:

```console
$ pip install get-gecko-driver --upgrade
```

## Usage

#### Package import

```Python
from get_gecko_driver import GetGeckoDriver

# Platforms to choose from: 'win32', 'win64', 'linux32', linux64', or 'macos'
get_driver = GetGeckoDriver(platform='win64')

# Print the latest release version
print(get_driver.latest_release_version())

# Print the latest release download link
print(get_driver.latest_release_url())

# Print the download link of a specific release
print(get_driver.release_url('0.27.0'))

# Download the latest driver release
# Optional: use output_path='' to specify where to download the driver
# Optional: use extract=True to extract the zip file
get_driver.download_latest_release(output_path='webdriver', extract=True)

# Download a specific driver release
# Optional: use output_path='' to specify where to download the driver
# Optional: use extract=True to extract the zip file
get_driver.download_release('0.27.0', extract=True)
```

#### Command-line

Print the latest release url of all platforms:

```console
$ get-gecko-driver --latest-urls
```

Print the latest release version:

```console
$ get-gecko-driver --latest-version
```

Print the latest release url of a specific platform:

```console
$ get-gecko-driver --latest-url linux64
```

Download the latest release of a specific platform:

```console
$ get-gecko-driver --download-latest win64
```

Download a specific release for a specific platform and extract the zip/tar file:

```console
$ get-gecko-driver --download-release macos 0.27.0 --extract
```

#### Downloaded drivers will be downloaded by default at:

*`<current directory>/<gecko_driver_downloads>/<release version>/<platform>/<geckodriver>`*

### Options

```
--help                      Show help.

--latest-version            Print the latest release version.

--latest-urls               Print the latest release urls for all platforms.

--release-url               Print the url of a release for a platform.

--latest-url                Print the latest release url for a platform.

--download-latest           Download the latest release for a platform.

--download-release          Download a release.

--extract                   Option to extract the file.

--version                   Program version.
```
