import pytest
import os
import shutil
import subprocess
from os import path

from decouple import config

from .. import constants
from .. import __version__
from ..platforms import Platforms

name = 'get-gecko-driver'
geckodriver = 'geckodriver'

platforms = Platforms()

latest_release = config('LATEST_RELEASE')
random_release = config('RANDOM_RELEASE')

latest_release_win_32_url = constants.GECKODRIVER_DOWNLOAD_URL.format(latest_release, latest_release,
                                                                      platforms.win_32_arch + constants.ZIP_TYPE)
latest_release_win_64_url = constants.GECKODRIVER_DOWNLOAD_URL.format(latest_release, latest_release,
                                                                      platforms.win_64_arch + constants.ZIP_TYPE)
latest_release_linux_32_url = constants.GECKODRIVER_DOWNLOAD_URL.format(latest_release, latest_release,
                                                                        platforms.linux_32_arch + constants.TAR_GZ_TYPE)
latest_release_linux_64_url = constants.GECKODRIVER_DOWNLOAD_URL.format(latest_release, latest_release,
                                                                        platforms.linux_64_arch + constants.TAR_GZ_TYPE)
latest_release_macos_url = constants.GECKODRIVER_DOWNLOAD_URL.format(latest_release, latest_release,
                                                                     platforms.macos + constants.TAR_GZ_TYPE)

random_release_win_64_url = constants.GECKODRIVER_DOWNLOAD_URL.format(random_release, random_release,
                                                                      platforms.win_64_arch + constants.ZIP_TYPE)
random_release_linux_64_url = constants.GECKODRIVER_DOWNLOAD_URL.format(random_release, random_release,
                                                                        platforms.linux_64_arch + constants.TAR_GZ_TYPE)
random_release_macos_url = constants.GECKODRIVER_DOWNLOAD_URL.format(random_release, random_release,
                                                                     platforms.macos + constants.TAR_GZ_TYPE)

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
    def test_random_win_release_url(self):
        url = random_release_win_64_url
        out = subprocess.run(args=[name, '--release-url', 'win64', random_release],
                             universal_newlines=True,
                             stdout=subprocess.PIPE)
        actual = out.stdout.split()[0]
        assert url, str(actual)

    def test_random_linux_release_url(self):
        url = random_release_linux_64_url
        out = subprocess.run(args=[name, '--release-url', 'linux64', random_release],
                             universal_newlines=True,
                             stdout=subprocess.PIPE)
        actual = out.stdout.split()[0]
        assert url == str(actual)

    def test_random_mac_release_url(self):
        url = random_release_macos_url
        out = subprocess.run(args=[name, '--release-url', 'macos', random_release],
                             universal_newlines=True,
                             stdout=subprocess.PIPE)
        actual = out.stdout.split()[0]
        assert url == str(actual)

    ######################
    # LATEST RELEASE URL #
    ######################
    def test_latest_win_release_url(self):
        url = latest_release_win_64_url
        out = subprocess.run(args=[name, '--latest-url', 'win64'],
                             universal_newlines=True,
                             stdout=subprocess.PIPE)
        actual = out.stdout.split()[0]
        assert url == str(actual)

    def test_latest_linux_release_url(self):
        url = latest_release_linux_64_url
        out = subprocess.run(args=[name, '--latest-url', 'linux64'],
                             universal_newlines=True,
                             stdout=subprocess.PIPE)
        actual = out.stdout.split()[0]
        assert url == str(actual)

    def test_latest_mac_release_url(self):
        url = latest_release_macos_url
        out = subprocess.run(args=[name, '--latest-url', 'macos'],
                             universal_newlines=True,
                             stdout=subprocess.PIPE)
        actual = out.stdout.split()[0]
        assert url == str(actual)

    ########################################
    # DOWNLOAD LATEST RELEASE - NO EXTRACT #
    ########################################
    def test_download_latest_win_release_no_extract(self):
        release = latest_release
        subprocess.run(args=[name, '--download-latest', 'win64'], stdout=subprocess.PIPE)
        file_path = (constants.DIR_DOWNLOADS + '/' + release + '/'
                     + platforms.win_64_arch + '/' + geckodriver + '-v' + release + '-'
                     + platforms.win_64_arch + constants.ZIP_TYPE)
        result = path.exists(file_path)
        assert result

    def test_download_latest_linux_release_no_extract(self):
        release = latest_release
        subprocess.run(args=[name, '--download-latest', 'linux64'], stdout=subprocess.PIPE)
        file_path = (constants.DIR_DOWNLOADS + '/' + release + '/'
                     + platforms.linux_64_arch + '/' + geckodriver + '-v' + release + '-'
                     + platforms.linux_64_arch + constants.TAR_GZ_TYPE)
        result = path.exists(file_path)
        assert result

    def test_download_latest_mac_release_no_extract(self):
        release = latest_release
        subprocess.run(args=[name, '--download-latest', 'macos'], stdout=subprocess.PIPE)
        file_path = (constants.DIR_DOWNLOADS + '/' + release + '/'
                     + platforms.macos + '/' + geckodriver + '-v' + release + '-' + platforms.macos
                     + constants.TAR_GZ_TYPE)
        result = path.exists(file_path)
        assert result

    #######################################
    # DOWNLOAD LATEST RELEASE - EXTRACTED #
    #######################################
    def test_download_latest_win_release_extract(self):
        release = latest_release
        subprocess.run(args=[name, '--download-latest', 'win64', '--extract'], stdout=subprocess.PIPE)
        file_path_extracted = (constants.DIR_DOWNLOADS + '/' + release + '/'
                               + platforms.win_64_arch + '/' + geckodriver + '-v' + release + '-'
                               + platforms.win_64_arch + constants.ZIP_TYPE)
        result = path.exists(file_path_extracted)
        assert result

    def test_download_latest_linux_release_extract(self):
        release = latest_release
        subprocess.run(args=[name, '--download-latest', 'linux64', '--extract'], stdout=subprocess.PIPE)
        file_path_extracted = (constants.DIR_DOWNLOADS + '/' + release + '/'
                               + platforms.linux_64_arch + '/' + geckodriver + '-v' + release + '-'
                               + platforms.linux_64_arch + constants.TAR_GZ_TYPE)
        result = path.exists(file_path_extracted)
        assert result

    def test_download_latest_mac_release_extract(self):
        release = latest_release
        subprocess.run(args=[name, '--download-latest', 'macos', '--extract'], stdout=subprocess.PIPE)
        file_path_extracted = (constants.DIR_DOWNLOADS + '/' + release + '/'
                               + platforms.macos + '/' + geckodriver + '-v' + release + '-'
                               + platforms.macos + constants.TAR_GZ_TYPE)
        result = path.exists(file_path_extracted)
        assert result

    ########################################
    # DOWNLOAD RANDOM RELEASE - NO EXTRACT #
    ########################################
    def test_download_random_win_release_no_extract(self):
        release = random_release
        subprocess.run(args=[name, '--download-release', 'win64', release], stdout=subprocess.PIPE)
        file_path = (constants.DIR_DOWNLOADS + '/' + release + '/'
                     + platforms.win_64_arch + '/' + geckodriver + '-v' + release + '-'
                     + platforms.win_64_arch + constants.ZIP_TYPE)
        result = path.exists(file_path)
        assert result

    def test_download_random_linux_release_no_extract(self):
        release = random_release
        subprocess.run(args=[name, '--download-release', 'linux64', release], stdout=subprocess.PIPE)
        file_path = (constants.DIR_DOWNLOADS + '/' + release + '/'
                     + platforms.linux_64_arch + '/' + geckodriver + '-v' + release + '-'
                     + platforms.linux_64_arch + constants.TAR_GZ_TYPE)
        result = path.exists(file_path)
        assert result

    def test_download_random_mac_release_no_extract(self):
        release = random_release
        subprocess.run(args=[name, '--download-release', 'macos', release], stdout=subprocess.PIPE)
        file_path = (constants.DIR_DOWNLOADS + '/' + release + '/'
                     + platforms.macos + '/' + geckodriver + '-v' + release + '-' + platforms.macos
                     + constants.TAR_GZ_TYPE)
        result = path.exists(file_path)
        assert result

    #######################################
    # DOWNLOAD RANDOM RELEASE - EXTRACTED #
    #######################################
    def test_download_random_win_release_extract(self):
        release = random_release
        subprocess.run(args=[name, '--download-release', 'win64', release, '--extract'],
                       stdout=subprocess.PIPE)
        file_path_extracted = (constants.DIR_DOWNLOADS + '/' + release + '/'
                               + platforms.win_64_arch + '/' + geckodriver + '-v' + release + '-'
                               + platforms.win_64_arch)
        result = path.exists(file_path_extracted + constants.ZIP_TYPE)
        assert result

    def test_download_random_linux_release_extract(self):
        release = random_release
        subprocess.run(args=[name, '--download-release', 'linux64', release, '--extract'],
                       stdout=subprocess.PIPE)
        file_path_extracted = (constants.DIR_DOWNLOADS + '/' + release + '/'
                               + platforms.linux_64_arch + '/' + geckodriver + '-v' + release + '-'
                               + platforms.linux_64_arch)
        result = path.exists(file_path_extracted + constants.TAR_GZ_TYPE)
        assert result

    def test_download_random_mac_release_extract(self):
        release = random_release
        subprocess.run(args=[name, '--download-release', 'macos', release, '--extract'],
                       stdout=subprocess.PIPE)
        file_path_extracted = (constants.DIR_DOWNLOADS + '/' + release + '/'
                               + platforms.macos + '/' + geckodriver + '-v' + release + '-'
                               + platforms.macos + constants.TAR_GZ_TYPE)
        result = path.exists(file_path_extracted)
        assert result

    ###########
    # VERSION #
    ###########
    def test_version(self):
        out = subprocess.run(args=[name, '--version'],
                             universal_newlines=True,
                             stdout=subprocess.PIPE)
        actual = out.stdout.split()[0]
        assert 'v' + __version__ == str(actual)

    ###########
    # CLEANUP #
    ###########
    @pytest.fixture(scope='session', autouse=True)
    def cleanup(self):
        yield
        try:
            shutil.rmtree(constants.DIR_DOWNLOADS)
        except FileNotFoundError:
            pass
