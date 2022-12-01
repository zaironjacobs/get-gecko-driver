import os
import requests
import zipfile
import tarfile
import platform as pl
import struct

from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from requests.exceptions import HTTPError

from .enums import Platform
from . import downloader
from . import constants
from .exceptions import GetGeckoDriverError
from .exceptions import UnknownPlatformError
from .exceptions import VersionUrlError
from .exceptions import UnknownVersionError
from .exceptions import DownloadError


class GetGeckoDriver:
    def __init__(self, platform: Platform = None):
        if not platform:
            if pl.system() == 'Windows':
                self.__system_platform = self.__check_platform(Platform.win)
            elif pl.system() == 'Linux':
                self.__system_platform = self.__check_platform(Platform.linux)
            elif pl.system() == 'Darwin':
                self.__system_platform = self.__check_platform(Platform.macos)
        else:
            self.__system_platform = self.__check_platform(platform)

    def latest_version(self) -> str:
        """ Return the latest version """

        result = requests.get(constants.url_geckodriver_releases)
        if not result.ok:
            raise GetGeckoDriverError(f'Could not get {constants.url_geckodriver_releases}')
        soup = BeautifulSoup(result.content, 'html.parser')
        anchor = soup.select_one(constants.css_selector_latest_version)
        version = anchor.text.strip()
        self.__check_if_version_format_is_valid(version)
        return version

    def latest_version_url(self) -> str:
        """ Return the latest version url """

        return self.version_url(self.latest_version())

    def version_url(self, version: str) -> str:
        """
        Return the version download url

        :param version: Geckodriver version
        """

        self.__check_if_version_format_is_valid(version)
        arch = struct.calcsize('P') * 8
        zip_ext = '.zip'
        tar_gz_ext = '.tar.gz'

        if self.__system_platform == Platform.win:
            # 64bit
            if arch == 64:
                try:
                    url = constants.url_download.format(version, version, Platform.win64.value) + zip_ext
                    self.__check_if_url_is_valid(url)
                    return url
                except VersionUrlError:
                    # No 64 bit, get 32 bit
                    pass
            # 32bit
            url = constants.url_download.format(version, version, Platform.win32.value) + zip_ext
            self.__check_if_url_is_valid(url)
            return url

        elif self.__system_platform == Platform.linux:
            # 64bit
            if arch == 64:
                try:
                    url = constants.url_download.format(version, version, Platform.linux64.value) + tar_gz_ext
                    self.__check_if_url_is_valid(url)
                    return url
                except VersionUrlError:
                    # No 64 bit, get 32 bit
                    pass
            # 32bit
            url = constants.url_download.format(version, version, Platform.linux32.value) + tar_gz_ext
            self.__check_if_url_is_valid(url)
            return url

        elif self.__system_platform == Platform.macos:
            # 64bit
            if arch == 64:
                try:
                    url = constants.url_download.format(version, version,
                                                        Platform.macos.value) + '-aarch64' + tar_gz_ext
                    self.__check_if_url_is_valid(url)
                    return url
                except VersionUrlError:
                    # No 64 bit, get 32 bit
                    pass
            # 32bit
            url = constants.url_download.format(version, version, Platform.macos.value) + tar_gz_ext
            self.__check_if_url_is_valid(url)
            return url

    def download_latest_version(self, output_path: str = None, extract: bool = False):
        """
        Download the latest geckodriver version

        :param output_path: Path to download the driver to
        :param extract: Extract the downloaded driver or not
        """

        version = self.latest_version()
        self.download_version(version=version, output_path=output_path, extract=extract)

    def download_version(self, version: str, output_path: str = None, extract: bool = False) -> str:
        """
        Download a geckodriver version

        :param version: Geckodriver version
        :param output_path: Path to download the driver to
        :param extract: Extract the downloaded driver or not
        """

        self.__check_if_version_format_is_valid(version)

        if not output_path:
            # on path is None,
            # GeckoDriver will be downloaded at e.g. geckodriver/0.29.0/bin/geckodriver.exe
            output_path = self._output_path(version)

        def download(download_url: str, download_path: str) -> str:
            try:
                output_path_with_file_name, file_name = downloader.download(url=download_url, output_path=download_path)
            except (OSError, HTTPError, RequestException) as err:
                raise DownloadError(err)
            if extract:
                if self.__system_platform == Platform.win:
                    with zipfile.ZipFile(output_path_with_file_name, 'r') as zip_ref:
                        zip_ref.extractall(path=download_path)
                else:
                    with tarfile.open(output_path_with_file_name, 'r:gz') as tar_gz_ref:
                        tar_gz_ref.extractall(path=download_path)
                os.remove(output_path_with_file_name)
                if self.__system_platform == Platform.linux or self.__system_platform == Platform.macos:
                    os.chmod(download_path + '/' + 'geckodriver', 0o755)
            return download_path

        # Download the driver file and return the path of the driver file
        url = self.version_url(version)
        return download(download_url=url, download_path=output_path)

    def __check_if_url_is_valid(self, url: str):
        """
        Check if url is valid

        :param url: The driver download url
        """

        if requests.head(url).status_code != 302:
            raise VersionUrlError('Invalid url (Possible cause: non-existent version)')

    def __check_if_version_format_is_valid(self, version: str):
        """
        Check if version format is valid

        :param version: Geckodriver version
        """

        split_version = version.split('.')
        for number in split_version:
            if not number.isnumeric():
                raise UnknownVersionError('Invalid version format')

    def __check_platform(self, platform: Platform) -> Platform:
        """
        Check if platform is valid

        :param platform: OS
        """

        platforms_list = [platform for platform in Platform]

        if platform not in platforms_list:
            raise UnknownPlatformError(f'Unknown platform, choose a platform from: {str(platforms_list)}')
        return platform

    def install(self):
        """ Install the latest GeckoDriver version """

        output_path = self.download_version(self.latest_version(), extract=True)
        path = os.path.join(os.path.abspath(os.getcwd()), output_path)
        os.environ['PATH'] += os.pathsep + os.pathsep.join([path])

    def __get_all_geckodriver_versions(self) -> list:
        """ Return a list with all GeckoDriver versions """

        def find_versions(param=None):
            if not param:
                url = constants.url_github_geckodriver_tags
            else:
                url = constants.url_github_geckodriver_tags + param

            response = requests.get(url)
            if not response.ok:
                raise GetGeckoDriverError(f'Could not get {constants.url_github_geckodriver_tags}')
            soup = BeautifulSoup(response.content, 'html.parser')
            box = soup.select_one('div.Box:nth-child(2)')

            versions = []
            for element in box.select('.d-flex > h4 > a'):
                versions.append(element.text.strip())

            if len(versions) == 10:
                versions += find_versions('?after=' + versions[-1])
            return versions

        all_versions = find_versions()
        for index, version in enumerate(all_versions):
            if version[:1] == 'v':
                all_versions[index] = version[1:]
        return all_versions

    def _output_path(self, version: str) -> str:
        """
        Return the output path

        :param version: Geckodriver version
        """

        return f'geckodriver/{version}/bin'
