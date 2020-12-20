Get GeckoDriver
=================
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/get-gecko-driver?color=blue)](https://pypi.python.org/pypi/get-gecko-driver)
[![PyPI](https://img.shields.io/pypi/v/get-gecko-driver?color=blue)](https://pypi.python.org/pypi/get-gecko-driver)
[![PyPI - Status](https://img.shields.io/pypi/status/get-gecko-driver)](https://pypi.python.org/pypi/get-gecko-driver)
[![PyPI - License](https://img.shields.io/pypi/l/get-gecko-driver)](https://pypi.python.org/pypi/get-gecko-driver)

A tool to download and install GeckoDriver. Download the latest release or another specific release. You can use 
this tool as a package import or as a command-line application.

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

#### Install and use GeckoDriver with Selenium

```Python
import time
from get_gecko_driver import GetGeckoDriver
from selenium import webdriver

# Install the driver:
# Downloads the latest GeckoDriver release
# Adds the downloaded GeckoDriver to path
get_driver = GetGeckoDriver()
get_driver.auto_install()

# Use the installed GeckoDriver with Selenium
gecko_driver = webdriver.Firefox()
gecko_driver.get("https://google.com")
time.sleep(3)
gecko_driver.quit()
```

#### For downloading only

```Python
from get_gecko_driver import GetGeckoDriver

get_driver = GetGeckoDriver()

# Print the latest release version
print(get_driver.latest_release_version())

# Print the latest release download link
print(get_driver.latest_release_url())

# Print the download link of a specific release
print(get_driver.release_url('0.27.0'))

# Download the latest driver release
# Optional: use output_path= to specify where to download the driver
# Optional: use extract=True to extract the file
get_driver.download_latest_release(extract=True)

# Download a specific driver release
# Optional: use output_path= to specify where to download the driver
# Optional: use extract=True to extract the file
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

Print the latest release url:

```console
$ get-gecko-driver --latest-url
```

Download the latest release and extract the file:

```console
$ get-gecko-driver --download-latest --extract
```

Download a specific release and extract the file:

```console
$ get-gecko-driver --download-release 0.27.0 --extract
```

#### The downloaded driver can be found at:

*`<current directory>/<geckodriver>/<version>/<bin>/<geckodriver>`*

### Options

```
--help                      Show help.

--latest-version            Print the latest release version.

--latest-urls               Print the latest release urls for all platforms.

--release-url               Print the url of a release.

--latest-url                Print the latest release url.

--download-latest           Download the latest release.

--download-release          Download a specific release.

--extract                   Extract the compressed driver file.

--version                   Program version.
```
