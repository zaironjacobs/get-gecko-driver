import os
import platform as pl
import shutil
import subprocess
from os import path

import pytest
from decouple import config

from get_gecko_driver import GetGeckoDriver
from get_gecko_driver import __version__
from get_gecko_driver import constants
from get_gecko_driver.enums import Platform

name = "get-gecko-driver"
geckodriver = "geckodriver"

latest_version = config("LATEST_VERSION")
random_version = config("RANDOM_VERSION")

if pl.system() == "Windows":
    file_name = "geckodriver.exe"
    file_name_compressed = "win64.zip"
    latest_version_url = constants.DOWNLOAD_URL.format(
        latest_version, latest_version, Platform.win64.value + ".zip"
    )
    random_version_url = constants.DOWNLOAD_URL.format(
        random_version, random_version, Platform.win64.value + ".zip"
    )
elif pl.system() == "Linux":
    file_name = "geckodriver"
    file_name_compressed = "linux64.tar.gz"
    latest_version_url = constants.DOWNLOAD_URL.format(
        latest_version, latest_version, Platform.linux64.value + ".tar.gz"
    )
    random_version_url = constants.DOWNLOAD_URL.format(
        random_version, random_version, Platform.linux64.value + ".tar.gz"
    )
elif pl.system() == "Darwin":
    file_name = "geckodriver"
    file_name_compressed = "macos.tar.gz"
    latest_version_url = constants.DOWNLOAD_URL.format(
        latest_version, latest_version, Platform.macos.value + ".tar.gz"
    )
    random_version_url = constants.DOWNLOAD_URL.format(
        random_version, random_version, Platform.macos.value + ".tar.gz"
    )

# Change to the current test directory
os.chdir(os.path.dirname(__file__))


class TestApp:
    def test_latest_latest_version(self):
        out = subprocess.run(
            args=[name, "--latest-version"],
            universal_newlines=True,
            stdout=subprocess.PIPE,
        )
        actual = out.stdout.split()[0]

        assert latest_version == str(actual)

    def test_random_version_url(self):
        url = random_version_url
        out = subprocess.run(
            args=[name, "--version-url", random_version],
            universal_newlines=True,
            stdout=subprocess.PIPE,
        )
        actual = out.stdout.split()[0]

        assert url, str(actual)

    def test_latest_version_url(self):
        url = latest_version_url
        out = subprocess.run(
            args=[name, "--latest-url"], universal_newlines=True, stdout=subprocess.PIPE
        )
        actual = out.stdout.split()[0]

        assert url == str(actual)

    def test_download_latest_version_no_extract(self):
        get_driver = GetGeckoDriver()
        version = latest_version
        subprocess.run(args=[name, "--download-latest"], stdout=subprocess.PIPE)
        file_path = (
            get_driver._output_path(version)
            + "/"
            + "geckodriver-v"
            + version
            + "-"
            + file_name_compressed
        )
        result = path.exists(file_path)

        assert result

    def test_download_latest_version_extract(self):
        get_driver = GetGeckoDriver()
        version = latest_version
        subprocess.run(
            args=[name, "--download-latest", "--extract"], stdout=subprocess.PIPE
        )
        file_path_extracted = get_driver._output_path(version) + "/" + file_name
        result = path.exists(file_path_extracted)

        assert result

    def test_download_latest_version_extract_custom_path(self):
        get_driver = GetGeckoDriver()
        get_driver.download_latest_version(
            output_path="webdriver/bin/geckodriver", extract=True
        )
        result = path.exists("webdriver/bin/geckodriver/" + file_name)

        assert result

    def test_download_random_version_no_extract(self):
        get_driver = GetGeckoDriver()
        version = random_version
        subprocess.run(
            args=[name, "--download-version", version], stdout=subprocess.PIPE
        )
        file_path = (
            get_driver._output_path(version)
            + "/"
            + "geckodriver-v"
            + version
            + "-"
            + file_name_compressed
        )
        result = path.exists(file_path)

        assert result

    def test_download_random_version_extract(self):
        get_driver = GetGeckoDriver()
        version = random_version
        subprocess.run(
            args=[name, "--download-version", version, "--extract"],
            stdout=subprocess.PIPE,
        )
        file_path_extracted = get_driver._output_path(version) + "/" + file_name
        result = path.exists(file_path_extracted)

        assert result

    def test_download_random_version_extract_custom_path(self):
        get_driver = GetGeckoDriver()
        version = random_version
        get_driver.download_version(
            version, output_path="webdriver/bin/geckodriver", extract=True
        )
        result = path.exists("webdriver/bin/geckodriver/" + file_name)

        assert result

    def test_install(self):
        get_driver = GetGeckoDriver()
        output_path = get_driver.install()

        found = False
        if os.path.isfile(f"{output_path}/{file_name}"):
            found = True

        assert found

    def test_install_custom_path(self):
        get_driver = GetGeckoDriver()
        output_path = get_driver.install("my_dir_1/my_dir_2")

        found = False
        if os.path.isfile(f"{output_path}/{file_name}"):
            found = True

        assert found

    def test_version(self):
        out = subprocess.run(
            args=[name, "--version"], universal_newlines=True, stdout=subprocess.PIPE
        )
        actual = out.stdout.split()[0]

        assert "v" + __version__ == str(actual)

    @pytest.fixture(scope="session", autouse=True)
    def cleanup(self):
        yield
        try:
            shutil.rmtree("geckodriver")
        except (FileNotFoundError, PermissionError):
            pass
        try:
            shutil.rmtree("webdriver")
        except (FileNotFoundError, PermissionError):
            pass
        try:
            shutil.rmtree("my_dir_1")
        except (FileNotFoundError, PermissionError):
            pass
