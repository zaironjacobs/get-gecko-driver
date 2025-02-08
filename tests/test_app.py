import os
import platform as pl
import shutil
import subprocess
from os import path

import requests
import pytest
from dotenv import load_dotenv

from get_gecko_driver import GetGeckoDriver
from get_gecko_driver import __version__
from get_gecko_driver import constants
from get_gecko_driver.enums import Platform

load_dotenv()

name = "get-gecko-driver"
geckodriver = "geckodriver"

LATEST_VERSION: str | None = os.getenv("LATEST_VERSION")
RANDOM_VERSION: str | None = os.getenv("RANDOM_VERSION")

# If STABLE_VERSION is not defined in .env, then find it using the JSON API endpoint
if not LATEST_VERSION:
    res_releases_latest = requests.get(
        "https://api.github.com/repos/mozilla/geckodriver/releases/latest"
    )
    LATEST_VERSION: str = res_releases_latest.json()["name"]
if not RANDOM_VERSION:
    RANDOM_VERSION = "0.32.0"

if pl.system() == "Windows":
    file_name = "geckodriver.exe"
    file_name_compressed = "win64.zip"
    latest_version_url = constants.DOWNLOAD_URL.format(
        LATEST_VERSION, LATEST_VERSION, Platform.win64.value + ".zip"
    )
    random_version_url = constants.DOWNLOAD_URL.format(
        RANDOM_VERSION, RANDOM_VERSION, Platform.win64.value + ".zip"
    )
elif pl.system() == "Linux":
    file_name = "geckodriver"
    file_name_compressed = "linux64.tar.gz"
    latest_version_url = constants.DOWNLOAD_URL.format(
        LATEST_VERSION, LATEST_VERSION, Platform.linux64.value + ".tar.gz"
    )
    random_version_url = constants.DOWNLOAD_URL.format(
        RANDOM_VERSION, RANDOM_VERSION, Platform.linux64.value + ".tar.gz"
    )
elif pl.system() == "Darwin":
    file_name = "geckodriver"
    file_name_compressed = "macos.tar.gz"
    latest_version_url = constants.DOWNLOAD_URL.format(
        LATEST_VERSION, LATEST_VERSION, Platform.macos.value + ".tar.gz"
    )
    random_version_url = constants.DOWNLOAD_URL.format(
        RANDOM_VERSION, RANDOM_VERSION, Platform.macos.value + ".tar.gz"
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

        assert LATEST_VERSION == str(actual)

    def test_random_version_url(self):
        url = random_version_url
        out = subprocess.run(
            args=[name, "--version-url", RANDOM_VERSION],
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
        version = LATEST_VERSION
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
        version = LATEST_VERSION
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
        version = RANDOM_VERSION
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
        version = RANDOM_VERSION
        subprocess.run(
            args=[name, "--download-version", version, "--extract"],
            stdout=subprocess.PIPE,
        )
        file_path_extracted = get_driver._output_path(version) + "/" + file_name
        result = path.exists(file_path_extracted)

        assert result

    def test_download_random_version_extract_custom_path(self):
        get_driver = GetGeckoDriver()
        version = RANDOM_VERSION
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
