import os
import requests
import zipfile
import tarfile
import platform as pl
import struct
from bs4 import BeautifulSoup

from requests.exceptions import RequestException
from requests.exceptions import HTTPError

from .platforms import Platforms
from . import retriever
from .exceptions import GetGeckoDriverError
from .exceptions import UnknownPlatformError
from .exceptions import VersionUrlError
from .exceptions import UnknownVersionError
from .exceptions import DownloadError


class GetGeckoDriver:
    def __init__(self, platform=None):
        self.__platforms = Platforms()

        if not platform:
            if pl.system() == 'Windows':
                self.__system_platform = self.__check_platform(self.__platforms.win)
            elif pl.system() == 'Linux':
                self.__system_platform = self.__check_platform(self.__platforms.linux)
            elif pl.system() == 'Darwin':
                self.__system_platform = self.__check_platform(self.__platforms.macos)
        else:
            self.__system_platform = self.__check_platform(platform)

    def latest_version(self) -> str:
        """ Return the latest version """

        url_geckodriver_releases = 'https://github.com/mozilla/geckodriver/releases'
        result = requests.get(url_geckodriver_releases)
        if not result.ok:
            raise GetGeckoDriverError('error: could not get ' + url_geckodriver_releases)
        soup = BeautifulSoup(result.content, 'html.parser')
        css_selector_latest_version = 'div.flex-md-row:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > h1:nth-child(1) > a:nth-child(1)'
        anchor = soup.select_one(css_selector_latest_version)
        version = anchor.text.strip()
        self.__check_version(version)
        return version

    def latest_version_url(self) -> str:
        """ Return the latest version url """

        return self.version_url(self.latest_version())

    def version_url(self, version) -> str:
        """
        Return the version download url

        :param version: Geckodriver version
        """

        self.__check_version(version)
        arch = struct.calcsize('P') * 8
        url_download = 'https://github.com/mozilla/geckodriver/releases/download/v{}/geckodriver-v{}-{}'
        zip_ext = '.zip'
        tar_gz_ext = '.tar.gz'

        if self.__system_platform == self.__platforms.win:
            # 64bit
            if arch == 64:
                try:
                    url = url_download.format(version, version, self.__platforms.win_64) + zip_ext
                    self.__check_url(url)
                    return url
                except VersionUrlError:
                    # No 64 bit, get 32 bit
                    pass
            # 32bit
            url = url_download.format(version, version, self.__platforms.win_32) + zip_ext
            self.__check_url(url)
            return url

        elif self.__system_platform == self.__platforms.linux:
            # 64bit
            if arch == 64:
                try:
                    url = url_download.format(version, version, self.__platforms.linux_64) + tar_gz_ext
                    self.__check_url(url)
                    return url
                except VersionUrlError:
                    # No 64 bit, get 32 bit
                    pass
            # 32bit
            url = url_download.format(version, version, self.__platforms.linux_32) + tar_gz_ext
            self.__check_url(url)
            return url

        elif self.__system_platform == self.__platforms.macos:
            # 64bit
            if arch == 64:
                try:
                    url = url_download.format(version, version, self.__platforms.macos) + '-aarch64' + tar_gz_ext
                    self.__check_url(url)
                    return url
                except VersionUrlError:
                    # No 64 bit, get 32 bit
                    pass
            # 32bit
            url = url_download.format(version, version, self.__platforms.macos) + tar_gz_ext
            self.__check_url(url)
            return url

    def download_latest_version(self, output_path=None, extract=False):
        """
        Download the latest geckodriver version

        :param output_path: Path to download the driver to
        :param extract: Extract the downloaded driver or not
        """

        version = self.latest_version()
        self.download_version(version, output_path, extract)

    def download_version(self, version, output_path=None, extract=False) -> str:
        """
        Download a geckodriver version

        :param version: Geckodriver version
        :param output_path: Path to download the driver to
        :param extract: Extract the downloaded driver or not
        """

        self.__check_version(version)

        if not output_path:
            # on path is None,
            # GeckoDriver will be downloaded at e.g. geckodriver/0.29.0/bin/geckodriver.exe
            output_path = self._default_output_path(version)

        def download(download_url, download_path) -> str:
            try:
                output_path_with_file_name, file_name = retriever.download(url=download_url, output_path=download_path)
            except (OSError, HTTPError, RequestException) as err:
                raise DownloadError(err)
            if extract:
                if self.__system_platform == self.__platforms.win:
                    with zipfile.ZipFile(output_path_with_file_name, 'r') as zip_ref:
                        zip_ref.extractall(path=download_path)
                else:
                    with tarfile.open(output_path_with_file_name, 'r:gz') as tar_gz_ref:
                        tar_gz_ref.extractall(path=download_path)
                os.remove(output_path_with_file_name)
                if self.__system_platform == self.__platforms.linux or self.__system_platform == self.__platforms.macos:
                    os.chmod(download_path + '/' + 'geckodriver', 0o755)
            return download_path

        # Download the driver file and return the path of the driver file
        url = self.version_url(version)
        return download(url, output_path)

    def __check_url(self, url):
        """ Check if url is valid """

        if requests.head(url).status_code != 302:
            raise VersionUrlError('Error: Invalid url (Possible cause: non-existent version)')

    def __check_version(self, version):
        """
        Check if version format is valid

        :param version: Geckodriver version
        """

        split_version = version.split('.')
        for number in split_version:
            if not number.isnumeric():
                raise UnknownVersionError('Error: Invalid version format')

    def __check_platform(self, platform) -> str:
        """
        Check if platform is valid

        :param platform: OS
        """

        if platform not in self.__platforms.list:
            raise UnknownPlatformError(
                f'error: platform not recognized, choose a platform from: {str(self.__platforms.list)}')
        return platform

    def install(self) -> None:
        """ Install the latest GeckoDriver version """

        output_path = self.download_version(self.latest_version(), extract=True)
        path = os.path.join(os.path.abspath(os.getcwd()), output_path)
        os.environ['PATH'] += os.pathsep + os.pathsep.join([path])

    def __get_all_geckodriver_versions(self) -> list:
        """ Return a list with all GeckoDriver versions """

        url_github_geckodriver_tags = 'https://github.com/mozilla/geckodriver/tags'

        def find_versions(param=None):
            if not param:
                url = url_github_geckodriver_tags
            else:
                url = url_github_geckodriver_tags + param

            response = requests.get(url)
            if not response.ok:
                raise GetGeckoDriverError('error: could not get ' + url_github_geckodriver_tags)
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

    def _default_output_path(self, version) -> str:
        """
        Return the default output path

        :param version: Geckodriver version
        """

        return f'geckodriver/{version}/bin'
