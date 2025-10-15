# Get GeckoDriver

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/get-gecko-driver?color=blue)](https://pypi.python.org/pypi/get-gecko-driver)
[![PyPI](https://img.shields.io/pypi/v/get-gecko-driver?color=blue)](https://pypi.python.org/pypi/get-gecko-driver)
[![PyPI - License](https://img.shields.io/pypi/l/get-gecko-driver)](https://pypi.python.org/pypi/get-gecko-driver)

[![tests](https://github.com/zaironjacobs/get-gecko-driver/actions/workflows/test.yml/badge.svg)](https://github.com/zaironjacobs/get-gecko-driver/actions/workflows/test.yml)

A tool to download and install GeckoDriver. Download the latest version or another specific version. You can use this
tool as a package import or as a command-line application.

## Install

To install:

```console
pip install get-gecko-driver
```

To upgrade:

```console
pip install get-gecko-driver --upgrade
```

## Usage

#### Install and use GeckoDriver with Selenium

```Python
import time
from get_gecko_driver import GetGeckoDriver
from selenium import webdriver

# Install the driver:
# Downloads the latest GeckoDriver version
# Adds the downloaded GeckoDriver to path
get_driver = GetGeckoDriver()
get_driver.install()

# Use the installed GeckoDriver with Selenium
driver = webdriver.Firefox()
driver.get("https://google.com")
time.sleep(3)
driver.quit()
```

#### For downloading only

```Python
from get_gecko_driver import GetGeckoDriver

get_driver = GetGeckoDriver()

# Print the latest version
print(get_driver.latest_version())

# Print the latest version download link
print(get_driver.latest_version_url())

# Print the download link of a specific version
print(get_driver.version_url('0.27.0'))

# Download the latest driver version
# Optional: use output_path= to specify where to download the driver
# Optional: use extract=True to extract the file
get_driver.download_latest_version(extract=True)

# Download a specific driver version
# Optional: use output_path= to specify where to download the driver
# Optional: use extract=True to extract the file
get_driver.download_version('0.27.0', extract=True)
```

#### Command-line

Print the latest version url of all platforms:

```console
get-gecko-driver --latest-urls
```

Print the latest version:

```console
get-gecko-driver --latest-version
```

Print the latest version url:

```console
get-gecko-driver --latest-url
```

Download the latest version and extract the file:

```console
get-gecko-driver --download-latest --extract
```

Download a specific version and extract the file:

```console
get-gecko-driver --download-version 0.27.0 --extract
```

#### The downloaded driver can be found at:

*`<current directory>/<geckodriver>/<version>/<bin>/<geckodriver>`*

### Options

```
--help                      Show help.

--latest-version            Print the latest version.

--latest-urls               Print the latest version urls for all platforms.

--version-url               Print the version url.

--latest-url                Print the latest version url.

--download-latest           Download the latest version.

--download-version          Download a specific version.

--extract                   Extract the compressed driver file.

--driver-filename           Print the driver filename.

--version                   App version.
```
