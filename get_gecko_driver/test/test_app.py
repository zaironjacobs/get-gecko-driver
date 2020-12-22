import pytest
import os
import shutil
import subprocess
import platform as pl
from os import path

from decouple import config

from .. import GetGeckoDriver
from .. import constants
from .. import __version__
from ..platforms import Platforms

name = 'get-gecko-driver'
geckodriver = 'geckodriver'

platforms = Platforms()

latest_version = config('LATEST_VERSION')
random_version = config('RANDOM_VERSION')

if pl.system() == 'Windows':
    file_end = 'geckodriver.exe'
    file_end_compressed = 'win64.zip'
    latest_version_url = constants.GECKODRIVER_DOWNLOAD_URL.format(latest_version, latest_version, platforms.win_64
                                                                   + '.zip')
    random_version_url = constants.GECKODRIVER_DOWNLOAD_URL.format(random_version, random_version, platforms.win_64
                                                                   + '.zip')
elif pl.system() == 'Linux':
    file_end = 'geckodriver'
    file_end_compressed = 'linux64.tar.gz'
    latest_version_url = constants.GECKODRIVER_DOWNLOAD_URL.format(latest_version, latest_version, platforms.linux_64
                                                                   + '.tar.gz')
    random_version_url = constants.GECKODRIVER_DOWNLOAD_URL.format(random_version, random_version, platforms.linux_64
                                                                   + '.tar.gz')
elif pl.system() == 'Darwin':
    file_end = 'geckodriver'
    file_end_compressed = 'macos.tar.gz'
    latest_version_url = constants.GECKODRIVER_DOWNLOAD_URL.format(latest_version, latest_version, platforms.macos
                                                                   + '.tar.gz')
    random_version_url = constants.GECKODRIVER_DOWNLOAD_URL.format(random_version, random_version, platforms.macos
                                                                   + '.tar.gz')

# Change to the current test directory
os.chdir(os.path.dirname(__file__))


class TestApp:

    ##################
    # LATEST VERSION #
    ##################
    def test_latest_latest_version(self):
        out = subprocess.run(args=[name, '--latest-version'],
                             universal_newlines=True,
                             stdout=subprocess.PIPE)
        actual = out.stdout.split()[0]
        assert latest_version == str(actual)

    ######################
    # RANDOM VERSION URL #
    ######################
    def test_random_version_url(self):
        url = random_version_url
        out = subprocess.run(args=[name, '--version-url', random_version],
                             universal_newlines=True,
                             stdout=subprocess.PIPE)
        actual = out.stdout.split()[0]
        assert url, str(actual)

    ######################
    # LATEST VERSION URL #
    ######################
    def test_latest_version_url(self):
        url = latest_version_url
        out = subprocess.run(args=[name, '--latest-url'],
                             universal_newlines=True,
                             stdout=subprocess.PIPE)
        actual = out.stdout.split()[0]
        assert url == str(actual)

    ########################################
    # DOWNLOAD LATEST VERSION - NO EXTRACT #
    ########################################
    def test_download_latest_version_no_extract(self):
        get_driver = GetGeckoDriver()
        version = latest_version
        subprocess.run(args=[name, '--download-latest'], stdout=subprocess.PIPE)
        file_path = (get_driver._default_output_path_str(version) + '/' + 'geckodriver-v' + version + '-'
                     + file_end_compressed)
        result = path.exists(file_path)
        assert result

    #######################################
    # DOWNLOAD LATEST VERSION - EXTRACTED #
    #######################################
    def test_download_latest_version_extract(self):
        get_driver = GetGeckoDriver()
        version = latest_version
        subprocess.run(args=[name, '--download-latest', '--extract'], stdout=subprocess.PIPE)
        file_path_extracted = (get_driver._default_output_path_str(version) + '/' + file_end)
        result = path.exists(file_path_extracted)
        assert result

    ########################################
    # DOWNLOAD RANDOM VERSION - NO EXTRACT #
    ########################################
    def test_download_random_version_no_extract(self):
        get_driver = GetGeckoDriver()
        version = random_version
        subprocess.run(args=[name, '--download-version', version], stdout=subprocess.PIPE)
        file_path = (get_driver._default_output_path_str(version) + '/' + 'geckodriver-v' + version + '-'
                     + file_end_compressed)
        result = path.exists(file_path)
        assert result

    #######################################
    # DOWNLOAD RANDOM VERSION - EXTRACTED #
    #######################################
    def test_download_random_version_extract(self):
        get_driver = GetGeckoDriver()
        version = random_version
        subprocess.run(args=[name, '--download-version', version, '--extract'], stdout=subprocess.PIPE)
        file_path_extracted = (get_driver._default_output_path_str(version) + '/' + file_end)
        result = path.exists(file_path_extracted)
        assert result

    ###########
    # VERSION #
    ###########
    def test_version(self):
        out = subprocess.run(args=[name, '--version'], universal_newlines=True, stdout=subprocess.PIPE)
        actual = out.stdout.split()[0]
        assert 'v' + __version__ == str(actual)

    ###########
    # CLEANUP #
    ###########
    @pytest.fixture(scope='session', autouse=True)
    def cleanup(self):
        yield
        try:
            shutil.rmtree(constants.GECKODRIVER)
        except FileNotFoundError:
            pass
