import requests
import zipfile
import tarfile
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


class GetGeckoDriver:
    def __init__(self, platform):
        self.__available_platforms = Platforms()
        self.__current_set_platform = self.__check_platform(platform)

    def latest_release_version(self):
        """ Return the latest release version """

        result = requests.get(constants.GITHUB_GECKODRIVER_RELEASES)
        soup = BeautifulSoup(result.content, 'html.parser')
        anchor = soup.select_one(constants.GITHUB_GECKODRIVER_LATEST_RELEASE_ANCHOR)
        release = anchor.text

        self.__check_release(release)
        return release

    def latest_release_url(self):
        """ Return the latest release url """

        return self.release_url(self.latest_release_version())

    def release_url(self, release):
        """ Return the release download url """

        self.__check_release(release)

        url = ''
        if self.__current_set_platform == self.__available_platforms.win_32_arch:
            url = constants.GECKODRIVER_DOWNLOAD_URL.format(release, release, self.__available_platforms.win_32_arch) \
                  + constants.ZIP_TYPE
        elif self.__current_set_platform == self.__available_platforms.win_64_arch:
            url = constants.GECKODRIVER_DOWNLOAD_URL.format(release, release, self.__available_platforms.win_64_arch) \
                  + constants.ZIP_TYPE
        elif self.__current_set_platform == self.__available_platforms.linux_32_arch:
            url = constants.GECKODRIVER_DOWNLOAD_URL.format(release, release, self.__available_platforms.linux_32_arch) \
                  + constants.TAR_GZ_TYPE
        elif self.__current_set_platform == self.__available_platforms.linux_64_arch:
            url = constants.GECKODRIVER_DOWNLOAD_URL.format(release, release, self.__available_platforms.linux_64_arch) \
                  + constants.TAR_GZ_TYPE
        elif self.__current_set_platform == self.__available_platforms.macos:
            url = constants.GECKODRIVER_DOWNLOAD_URL.format(release, release, self.__available_platforms.macos) \
                  + constants.TAR_GZ_TYPE

        self.__check_url(url)
        return url

    def download_latest_release(self, output_path=None, extract=False):
        """ Download the latest geckodriver release """

        release = self.latest_release_version()
        if release is None:
            return False

        self.download_release(release, output_path, extract)
        return True

    def download_release(self, release, output_path=None, extract=False):
        """ Download a geckodriver release """

        self.__check_release(release)
        url = self.release_url(release)

        def download(platform_arch, extract_type):
            if output_path is None:
                output_path_no_file_name = constants.DIR_DOWNLOADS + '/' + release + '/' + platform_arch
            else:
                output_path_no_file_name = output_path

            try:
                output_path_with_file_name, file_name = retriever.download(url=url,
                                                                           output_path=output_path_no_file_name)
            except (OSError, HTTPError, RequestException) as err:
                raise GetGeckoDriverError(err)

            if extract:
                if extract_type == constants.ZIP_TYPE:
                    with zipfile.ZipFile(output_path_with_file_name, 'r') as zip_ref:
                        zip_ref.extractall(path=output_path_no_file_name)
                elif extract_type == constants.TAR_GZ_TYPE:
                    with tarfile.open(output_path_with_file_name, "r:gz") as tar_gz_ref:
                        tar_gz_ref.extractall(path=output_path_no_file_name)

        if self.__current_set_platform == self.__available_platforms.win_32_arch:
            download(self.__available_platforms.win_32_arch, constants.ZIP_TYPE)
        elif self.__current_set_platform == self.__available_platforms.win_64_arch:
            download(self.__available_platforms.win_64_arch, constants.ZIP_TYPE)
        elif self.__current_set_platform == self.__available_platforms.linux_32_arch:
            download(self.__available_platforms.linux_32_arch, constants.TAR_GZ_TYPE)
        elif self.__current_set_platform == self.__available_platforms.linux_64_arch:
            download(self.__available_platforms.linux_64_arch, constants.TAR_GZ_TYPE)
        elif self.__current_set_platform == self.__available_platforms.macos:
            download(self.__available_platforms.macos, constants.TAR_GZ_TYPE)

    def __check_url(self, url):
        """ Check if url is valid """

        if requests.head(url).status_code != 302:
            raise ReleaseUrlError('Error: Invalid url (Possible cause: non-existent release version)')

    def __check_release(self, release):
        """ Check if release format is valid """

        split_release = release.split('.')

        for number in split_release:
            if not number.isnumeric():
                raise UnknownReleaseError('Error: Invalid release format')

    def __check_platform(self, platform):
        """ Check if platform is valid """

        if platform not in self.__available_platforms.list:
            raise UnknownPlatformError('Error: Platform not recognized, choose a platform from: '
                                       + str(self.__available_platforms.list))
        return platform
