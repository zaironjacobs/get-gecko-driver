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

latest_release = config('LATEST_RELEASE')
random_release = config('RANDOM_RELEASE')

if pl.system() == 'Windows':
    file_end = 'geckodriver.exe'
    file_end_compressed = 'win64.zip'
    latest_release_url = constants.GECKODRIVER_DOWNLOAD_URL.format(latest_release, latest_release, platforms.win_64
                                                                   + '.zip')
    random_release_url = constants.GECKODRIVER_DOWNLOAD_URL.format(random_release, random_release, platforms.win_64
                                                                   + '.zip')
elif pl.system() == 'Linux':
    file_end = 'geckodriver'
    file_end_compressed = 'linux64.tar.gz'
    latest_release_url = constants.GECKODRIVER_DOWNLOAD_URL.format(latest_release, latest_release, platforms.linux_64
                                                                   + '.tar.gz')
    random_release_url = constants.GECKODRIVER_DOWNLOAD_URL.format(random_release, random_release, platforms.linux_64
                                                                   + '.tar.gz')
elif pl.system() == 'Darwin':
    file_end = 'geckodriver'
    file_end_compressed = 'macos.tar.gz'
    latest_release_url = constants.GECKODRIVER_DOWNLOAD_URL.format(latest_release, latest_release, platforms.macos
                                                                   + '.tar.gz')
    random_release_url = constants.GECKODRIVER_DOWNLOAD_URL.format(random_release, random_release, platforms.macos
                                                                   + '.tar.gz')

# Change to the current test directory
os.chdir(os.path.dirname(__file__))


class TestApp:

    ##################
    # LATEST VERSION #
    ##################
    def test_latest_latest_release_version(self):
        out = subprocess.run(args=[name, '--latest-version'],
                             universal_newlines=True,
                             stdout=subprocess.PIPE)
        actual = out.stdout.split()[0]
        assert latest_release == str(actual)

    ######################
    # RANDOM RELEASE URL #
    ######################
    def test_random_release_url(self):
        url = random_release_url
        out = subprocess.run(args=[name, '--release-url', random_release],
                             universal_newlines=True,
                             stdout=subprocess.PIPE)
        actual = out.stdout.split()[0]
        assert url, str(actual)

    ######################
    # LATEST RELEASE URL #
    ######################
    def test_latest_release_url(self):
        url = latest_release_url
        out = subprocess.run(args=[name, '--latest-url'],
                             universal_newlines=True,
                             stdout=subprocess.PIPE)
        actual = out.stdout.split()[0]
        assert url == str(actual)

    ########################################
    # DOWNLOAD LATEST RELEASE - NO EXTRACT #
    ########################################
    def test_download_latest_release_no_extract(self):
        get_driver = GetGeckoDriver()
        release = latest_release
        subprocess.run(args=[name, '--download-latest'], stdout=subprocess.PIPE)
        file_path = (get_driver._create_output_path_str(release) + '/' + 'geckodriver-v' + release + '-'
                     + file_end_compressed)
        result = path.exists(file_path)
        assert result

    #######################################
    # DOWNLOAD LATEST RELEASE - EXTRACTED #
    #######################################
    def test_download_latest_release_extract(self):
        get_driver = GetGeckoDriver()
        release = latest_release
        subprocess.run(args=[name, '--download-latest', '--extract'], stdout=subprocess.PIPE)
        file_path_extracted = (get_driver._create_output_path_str(release) + '/' + file_end)
        result = path.exists(file_path_extracted)
        assert result

    ########################################
    # DOWNLOAD RANDOM RELEASE - NO EXTRACT #
    ########################################
    def test_download_random_release_no_extract(self):
        get_driver = GetGeckoDriver()
        release = random_release
        subprocess.run(args=[name, '--download-release', release], stdout=subprocess.PIPE)
        file_path = (get_driver._create_output_path_str(release) + '/' + 'geckodriver-v' + release + '-'
                     + file_end_compressed)
        result = path.exists(file_path)
        assert result

    #######################################
    # DOWNLOAD RANDOM RELEASE - EXTRACTED #
    #######################################
    def test_download_random_release_extract(self):
        get_driver = GetGeckoDriver()
        release = random_release
        subprocess.run(args=[name, '--download-release', release, '--extract'], stdout=subprocess.PIPE)
        file_path_extracted = (get_driver._create_output_path_str(release) + '/' + file_end)
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
