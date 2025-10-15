import os
import platform as pl
import struct
import tarfile
import zipfile

import requests
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError
from requests.exceptions import RequestException

from get_gecko_driver import constants
from get_gecko_driver import downloader
from get_gecko_driver.enums import Platform, OsPlatform
from get_gecko_driver.exceptions import DownloadError, VersionUrlError
from get_gecko_driver.exceptions import GetGeckoDriverError
from get_gecko_driver.exceptions import UnknownPlatformError
from get_gecko_driver.exceptions import UnknownVersionError


class GetGeckoDriver:
    def __init__(self, os_platform: OsPlatform = None):
        self.__os_platforms_list = [os_platform for os_platform in OsPlatform]

        if not os_platform:
            if pl.system() == "Windows":
                self.__os_platform = OsPlatform.win
            elif pl.system() == "Linux":
                self.__os_platform = OsPlatform.linux
            elif pl.system() == "Darwin":
                self.__os_platform = OsPlatform.mac
        else:
            if self.__check_if_os_platform_is_valid(os_platform):
                self.__os_platform = os_platform
        if not self.__os_platform:
            raise UnknownPlatformError("Unknown OS platform.")

        self.__arch = struct.calcsize("P") * 8
        self.__zip_ext = ".zip"
        self.__tar_gz_ext = ".tar.gz"

    def driver_filename(self) -> str:
        """
        Driver filename.
        """

        if self.__os_platform == OsPlatform.win:
            return "geckodriver.exe"
        elif self.__os_platform == OsPlatform.linux:
            return "geckodriver"
        elif self.__os_platform == OsPlatform.mac:
            return "geckodriver"

        raise UnknownPlatformError("Unknown OS platform.")

    def latest_version(self) -> str:
        """
        Return the latest version.
        """

        result = requests.get(constants.GECKODRIVER_RELEASES_URL)
        if not result.ok:
            raise GetGeckoDriverError(
                f"Could not fetch from {constants.GECKODRIVER_RELEASES_URL}."
            )

        soup = BeautifulSoup(result.content, "html.parser")
        anchor = soup.select_one(constants.CSS_SELECTOR_LATEST_VERSION)
        version = anchor.text.strip()

        if self.__check_if_version_format_is_valid(version):
            return version

        raise UnknownVersionError("Could not find version.")

    def latest_version_url(self) -> str:
        """
        Return the latest version url.
        """

        return self.version_url(self.latest_version())

    def version_url(self, version: str) -> str:
        """
        Return the version download url.

        :param version: Geckodriver version.
        """

        if not self.__check_if_version_format_is_valid(version):
            raise UnknownVersionError("Invalid version format.")

        if self.__os_platform == OsPlatform.win:
            # 64bit
            if self.__arch == 64:
                try:
                    url = f"{constants.DOWNLOAD_URL.format(version, version, Platform.win64.value)}{self.__zip_ext}"
                    if self.__check_if_url_is_valid(url):
                        return url
                except (Exception,):
                    # No 64 bit, get 32 bit
                    pass

            # 32bit
            url = f"{constants.DOWNLOAD_URL.format(version, version, Platform.win32.value)}{self.__zip_ext}"
            if self.__check_if_url_is_valid(url):
                return url

        elif self.__os_platform == OsPlatform.linux:
            # 64bit
            if self.__arch == 64:
                try:
                    url = f"{constants.DOWNLOAD_URL.format(version, version, Platform.linux64.value)}{self.__tar_gz_ext}"
                    if self.__check_if_url_is_valid(url):
                        return url
                except (Exception,):
                    # No 64 bit, get 32 bit
                    pass

            # 32bit
            url = f"{constants.DOWNLOAD_URL.format(version, version, Platform.linux32.value)}{self.__tar_gz_ext}"
            if self.__check_if_url_is_valid(url):
                return url

        elif self.__os_platform == OsPlatform.mac:
            # 64bit
            if self.__arch == 64:
                try:
                    url = f"{constants.DOWNLOAD_URL.format(version, version, Platform.macos.value)}-aarch64{self.__tar_gz_ext}"
                    if self.__check_if_url_is_valid(url):
                        return url
                except (Exception,):
                    # No 64 bit, get 32 bit
                    pass

            # 32bit
            url = f"{constants.DOWNLOAD_URL.format(version, version, Platform.macos.value)}{self.__tar_gz_ext}"
            if self.__check_if_url_is_valid(url):
                return url

        raise VersionUrlError(f"Could not find download url for version {version}.")

    def download_latest_version(
        self, output_path: str = None, extract: bool = False
    ) -> str:
        """
        Download the latest geckodriver version.

        :param output_path: Path to download the driver to.
        :param extract: Extract the downloaded driver or not.
        """

        version = self.latest_version()
        output_path = self.download_version(
            version=version, output_path=output_path, extract=extract
        )

        return output_path

    def download_version(
        self, version: str, output_path: str = None, extract: bool = False
    ) -> str:
        """
        Download a geckodriver version.

        :param version: Geckodriver version.
        :param output_path: Path to download the driver to.
        :param extract: Extract the downloaded driver or not.
        """

        if not self.__check_if_version_format_is_valid(version):
            raise UnknownVersionError("Invalid version format.")

        if not output_path:
            # on path is None, the driver will be downloaded at e.g. geckodriver/0.29.0/bin/geckodriver.exe
            output_path = self._output_path(version)

        def download(download_url: str):
            # Download
            try:
                output_path_with_file_name, file_name = downloader.download(
                    url=download_url, output_path=output_path
                )
            except (OSError, HTTPError, RequestException) as err:
                raise DownloadError(err)

            # Extract
            if extract:
                if self.__os_platform == OsPlatform.win:
                    with zipfile.ZipFile(output_path_with_file_name, "r") as zip_ref:
                        zip_ref.extractall(path=output_path)
                else:
                    with tarfile.open(output_path_with_file_name, "r:gz") as tar_gz_ref:
                        tar_gz_ref.extractall(path=output_path)
                os.remove(output_path_with_file_name)
                if (
                    self.__os_platform == OsPlatform.linux
                    or self.__os_platform == OsPlatform.mac
                ):
                    os.chmod(output_path + "/" + "geckodriver", 0o755)

        url = self.version_url(version)
        download(download_url=url)

        return output_path

    def __check_if_url_is_valid(self, url: str) -> bool:
        """
        Check if url is valid.

        :param url: The driver download url.
        """

        status_code = requests.head(url).status_code
        if status_code == 302 or status_code == 200:
            return True

        return False

    def __check_if_version_format_is_valid(self, version: str) -> bool:
        """
        Check if version format is valid.

        :param version: Geckodriver version.
        """

        split_version = version.split(".")
        for number in split_version:
            if not number.isnumeric():
                return False

        return True

    def __check_if_os_platform_is_valid(self, os_platform: OsPlatform) -> bool:
        """
        Check if platform is valid.

        :param os_platform: OS.
        """

        if os_platform not in self.__os_platforms_list:
            return False

        return True

    def install(self, output_path: str = None) -> str:
        """
        Install the latest GeckoDriver version.
        """

        if output_path:
            self.download_version(
                self.latest_version(), output_path=output_path, extract=True
            )
        else:
            output_path = self.download_version(self.latest_version(), extract=True)

        os.environ["PATH"] += os.pathsep + output_path

        if not os.path.isabs(output_path):
            output_path = os.path.join(os.path.abspath(os.getcwd()), output_path)

        output_path = output_path.replace(os.sep, "/")

        return output_path

    def __get_all_geckodriver_versions(self) -> list:
        """
        Return a list with all GeckoDriver versions.
        """

        def find_versions(param=None):
            if not param:
                url = constants.GITHUB_GECKODRIVER_TAGS_URL
            else:
                url = constants.GITHUB_GECKODRIVER_TAGS_URL + param

            response = requests.get(url)
            if not response.ok:
                raise GetGeckoDriverError(
                    f"Could not get {constants.GITHUB_GECKODRIVER_TAGS_URL}."
                )
            soup = BeautifulSoup(response.content, "html.parser")
            box = soup.select_one("div.Box:nth-child(2)")

            versions = []
            for element in box.select(".d-flex > h4 > a"):
                versions.append(element.text.strip())

            if len(versions) == 10:
                versions += find_versions("?after=" + versions[-1])

            return versions

        all_versions = find_versions()
        for index, version in enumerate(all_versions):
            if version[:1] == "v":
                all_versions[index] = version[1:]

        return all_versions

    def _output_path(self, version: str) -> str:
        """
        Get the output path.

        :param version: Geckodriver version.
        """

        return f"geckodriver/{version}/bin"
