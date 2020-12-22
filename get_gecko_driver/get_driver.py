import os
import requests
import zipfile
import tarfile
import platform as pl
import subprocess
import struct
from bs4 import BeautifulSoup

from requests.exceptions import RequestException
from requests.exceptions import HTTPError

from . import constants
from .platforms import Platforms
from . import retriever
from .exceptions import GetGeckoDriverError
from .exceptions import UnknownPlatformError
from .exceptions import ReleaseUrlError
from .exceptions import UnknownReleaseError
from .exceptions import DownloadError


class GetGeckoDriver:
    def __init__(self, platform=None) -> None:
        self.__platforms = Platforms()

        if not platform:
            if pl.system() == 'Windows':
                self.__platform = self.__check_platform(self.__platforms.win)
            elif pl.system() == 'Linux':
                self.__platform = self.__check_platform(self.__platforms.linux)
            elif pl.system() == 'Darwin':
                self.__platform = self.__check_platform(self.__platforms.macos)
        else:
            self.__platform = self.__check_platform(platform)

    def latest_release_version(self) -> str:
        """ Return the latest release version """

        result = requests.get(constants.GITHUB_GECKODRIVER_RELEASES_URL)

        if result.status_code != 200:
            raise GetGeckoDriverError('error: could not connect to ' + constants.GITHUB_GECKODRIVER_RELEASES_URL)

        soup = BeautifulSoup(result.content, 'html.parser')
        anchor = soup.select_one(constants.GITHUB_GECKODRIVER_LATEST_RELEASE_ANCHOR)
        release = anchor.text

        self.__check_release(release)
        return release

    def latest_release_url(self) -> str:
        """ Return the latest release url """

        return self.release_url(self.latest_release_version())

    def release_url(self, release) -> str:
        """ Return the release download url """

        self.__check_release(release)

        arch = struct.calcsize('P') * 8
        arch_64 = 64

        if self.__platform == self.__platforms.win:

            # 64bit
            if arch == arch_64:
                try:
                    url = (constants.GECKODRIVER_DOWNLOAD_URL.format(release, release, self.__platforms.win_64)
                           + constants.ZIP_TYPE)
                    self.__check_url(url)
                    return url
                except ReleaseUrlError:
                    pass
            # 32bit
            url = (constants.GECKODRIVER_DOWNLOAD_URL.format(release, release, self.__platforms.win_32)
                   + constants.ZIP_TYPE)
            self.__check_url(url)
            return url

        elif self.__platform == self.__platforms.linux:

            # 64bit
            if arch == arch_64:
                try:
                    url = (constants.GECKODRIVER_DOWNLOAD_URL.format(release, release, self.__platforms.linux_64)
                           + constants.TAR_GZ_TYPE)
                    self.__check_url(url)
                    return url
                except ReleaseUrlError:
                    pass
            # 32bit
            url = (constants.GECKODRIVER_DOWNLOAD_URL.format(release, release, self.__platforms.linux_32)
                   + constants.TAR_GZ_TYPE)
            self.__check_url(url)
            return url

        elif self.__platform == self.__platforms.macos:

            url = (constants.GECKODRIVER_DOWNLOAD_URL.format(release, release, self.__platforms.macos)
                   + constants.TAR_GZ_TYPE)
            self.__check_url(url)
            return url

    def download_latest_release(self, output_path=None, extract=False) -> None:
        """ Download the latest geckodriver release """

        release = self.latest_release_version()
        self.download_release(release, output_path, extract)

    def download_release(self, release, output_path=None, extract=False) -> str:
        """ Download a geckodriver release """

        self.__check_release(release)

        if not output_path:
            path = self._create_output_path_str(release)
        else:
            path = output_path

        for root, dirs, files in os.walk(path):
            for file in files:
                if (file.lower() == constants.GECKODRIVER.lower() or
                        file.lower() == constants.GECKODRIVER.lower() + '.exe'):
                    return path

        def download(download_url, download_path, extract_type) -> str:
            try:
                output_path_with_file_name, file_name = retriever.download(url=download_url, output_path=download_path)
            except (OSError, HTTPError, RequestException) as err:
                raise DownloadError(err)

            if extract:
                if extract_type == constants.ZIP_TYPE:
                    with zipfile.ZipFile(output_path_with_file_name, 'r') as zip_ref:
                        zip_ref.extractall(path=download_path)
                elif extract_type == constants.TAR_GZ_TYPE:
                    with tarfile.open(output_path_with_file_name, "r:gz") as tar_gz_ref:
                        tar_gz_ref.extractall(path=download_path)

                os.remove(output_path_with_file_name)

                if self.__platform == self.__platforms.linux or self.__platform == self.__platforms.macos:
                    os.chmod(download_path + '/' + constants.GECKODRIVER, 0o755)

            return download_path

        url = self.release_url(release)

        # Download the driver file and return the dir path of the driver file
        if self.__platform == self.__platforms.win:
            return download(url, path, constants.ZIP_TYPE)
        else:
            return download(url, path, constants.TAR_GZ_TYPE)

    def __check_url(self, url) -> None:
        """ Check if url is valid """

        if requests.head(url).status_code != 302:
            raise ReleaseUrlError('Error: Invalid url (Possible cause: non-existent release version)')

    def __check_release(self, release) -> None:
        """ Check if release format is valid """

        split_release = release.split('.')

        for number in split_release:
            if not number.isnumeric():
                raise UnknownReleaseError('Error: Invalid release format')

    def __check_platform(self, platform) -> str:
        """ Check if platform is valid """

        if platform not in self.__platforms.list:
            raise UnknownPlatformError('error: platform not recognized, choose a platform from: '
                                       + str(self.__platforms.list))
        return platform

    def install(self) -> None:
        """ Install the latest GeckoDriver release """

        output_path = self.download_release(self.latest_release_version(), extract=True)
        path = os.path.join(os.path.abspath(os.getcwd()), output_path)
        os.environ['PATH'] += os.pathsep + os.pathsep.join([path])

    def __get_all_geckodriver_versions(self) -> list:
        """ Return a list with all GeckoDriver versions """

        def find_versions(param=None) -> list:
            if not param:
                url = constants.GITHUB_GECKODRIVER_TAGS_URL
            else:
                url = constants.GITHUB_GECKODRIVER_TAGS_URL + param

            res = requests.get(url)

            if res.status_code != 200:
                raise GetGeckoDriverError('error: could not connect to ' + constants.GITHUB_GECKODRIVER_TAGS_URL)

            soup = BeautifulSoup(res.content, 'html.parser')
            box_el = soup.select_one('div.Box:nth-child(2)')

            count = 0
            versions = []
            for element in box_el.select('.d-flex > h4 > a'):
                versions.append(element.text.strip())
                count += 1

            if len(versions) == 10:
                versions += find_versions('?after=' + versions[-1])

            return versions

        all_versions = find_versions()
        for index, version in enumerate(all_versions):
            if version[:1] == 'v':
                all_versions[index] = version[1:]
        return all_versions

    def _create_output_path_str(self, release) -> str:
        """ Return the default output path """

        return constants.GECKODRIVER + '/' + release + '/' + 'bin'
