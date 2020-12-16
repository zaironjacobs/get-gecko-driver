import sys
import argparse
from signal import signal, SIGINT

import colorama

from . import __version__
from . import arguments
from .get_driver import GetGeckoDriver
from .platforms import Platforms
from .exceptions import GetGeckoDriverError


def main():
    # noinspection PyUnusedLocal
    def signal_handler(signal_received, frame):
        """ Handles clean Ctrl+C exit """

        sys.stdout.write('\n')
        sys.exit(0)

    signal(SIGINT, signal_handler)
    App()


class App:

    def __init__(self):
        self.__c_fore = colorama.Fore
        self.__c_style = colorama.Style
        colorama.init()

        self.__platforms = Platforms()

        self.__msg_download_finished = 'download finished'
        self.__msg_required_choose_platform = (self.__c_fore.RED + 'required: choose one of the following platforms: '
                                               + str(self.__platforms.list) + self.__c_style.RESET_ALL)
        self.__msg_required_add_release = (self.__c_fore.RED + 'required: add a release version'
                                           + self.__c_style.RESET_ALL)
        self.__msg_optional_add_extract = 'optional: add --extract to extract the zip file'
        self.__msg_error_unrecognized_argument = (
                self.__c_fore.RED + 'error: unrecognized argument(s) detected' + self.__c_style.RESET_ALL
                + '\n' + 'tip: use --help to see all available arguments')
        self.__msg_download_error = (self.__c_fore.RED + 'error: an error occurred at downloading'
                                     + self.__c_style.RESET_ALL)
        self.__msg_release_url_error = (self.__c_fore.RED + 'error: could not find release url'
                                        + self.__c_style.RESET_ALL)

        self.__parser = argparse.ArgumentParser(add_help=False)
        for i, arg in enumerate(arguments.args_options):
            self.__parser.add_argument(arguments.args_options[i][0], nargs='*')
        self.__args, self.__unknown = self.__parser.parse_known_args()

        if self.__unknown:
            print(self.__msg_error_unrecognized_argument)
            sys.exit(0)

        ###################
        # DEFAULT NO ARGS #
        ###################
        if len(sys.argv) == 1:
            arguments.print_help()
            sys.exit(0)

        ########
        # HELP #
        ########
        self.__arg_help = self.__args.help
        if self.__arg_passed(self.__arg_help):
            arguments.print_help()
            sys.exit(0)

        ##################
        # LATEST VERSION #
        ##################
        self.__arg_latest_version = self.__args.latest_version
        if self.__arg_passed(self.__arg_latest_version):
            self.print_latest_version()
            sys.exit(0)

        ###############
        # LATEST URLS #
        ###############
        self.__arg_latest_urls = self.__args.latest_urls
        if self.__arg_passed(self.__arg_latest_urls):
            self.print_latest_urls()
            sys.exit(0)

        ###############
        # RELEASE URL #
        ###############
        self.__arg_release_url = self.__args.release_url
        if self.__arg_passed(self.__arg_release_url):
            custom_required_message = (self.__msg_required_choose_platform
                                       + '\n' + self.__msg_required_add_release)
            if not self.__arg_release_url:
                print(custom_required_message)
                sys.exit(0)
            if len(self.__arg_release_url) != 2:
                print(custom_required_message)
                sys.exit(0)

            platform = self.__arg_release_url[0]
            release = self.__arg_release_url[1]

            if self.__platforms.win_32_arch == platform:
                # noinspection PyBroadException
                try:
                    self.print_release_url(self.__platforms.win_32_arch, release)
                except Exception:
                    print(self.__msg_release_url_error)

            elif self.__platforms.win_64_arch == platform:
                # noinspection PyBroadException
                try:
                    self.print_release_url(self.__platforms.win_64_arch, release)
                except Exception:
                    print(self.__msg_release_url_error)

            elif self.__platforms.linux_32_arch == platform:
                # noinspection PyBroadException
                try:
                    self.print_release_url(self.__platforms.linux_32_arch, release)
                except Exception:
                    print(self.__msg_release_url_error)

            elif self.__platforms.linux_64_arch == platform:
                # noinspection PyBroadException
                try:
                    self.print_release_url(self.__platforms.linux_64_arch, release)
                except Exception:
                    print(self.__msg_release_url_error)

            elif self.__platforms.macos == platform:
                # noinspection PyBroadException
                try:
                    self.print_release_url(self.__platforms.macos, release)
                except Exception:
                    print(self.__msg_release_url_error)

            else:
                print(custom_required_message)
            sys.exit(0)

        ##############
        # LATEST URL #
        ##############
        self.__arg_latest_url = self.__args.latest_url
        if self.__arg_passed(self.__arg_latest_url):
            if not self.__arg_latest_url:
                print(self.__msg_required_choose_platform)
                sys.exit(0)
            if len(self.__arg_latest_url) != 1:
                print(self.__msg_required_choose_platform)
                sys.exit(0)

            self.__platform = self.__arg_latest_url[0]

            if self.__platforms.win_32_arch == self.__platform:
                # noinspection PyBroadException
                try:
                    self.print_latest_url(self.__platforms.win_32_arch)
                except Exception:
                    print(self.__msg_release_url_error)

            elif self.__platforms.win_64_arch == self.__platform:
                # noinspection PyBroadException
                try:
                    self.print_latest_url(self.__platforms.win_64_arch)
                except Exception:
                    print(self.__msg_release_url_error)

            elif self.__platforms.linux_32_arch == self.__platform:
                # noinspection PyBroadException
                try:
                    self.print_latest_url(self.__platforms.linux_32_arch)
                except Exception:
                    print(self.__msg_release_url_error)

            elif self.__platforms.linux_64_arch == self.__platform:
                # noinspection PyBroadException
                try:
                    self.print_latest_url(self.__platforms.linux_64_arch)
                except Exception:
                    print(self.__msg_release_url_error)

            elif self.__platforms.macos == self.__platform:
                # noinspection PyBroadException
                try:
                    self.print_latest_url(self.__platforms.macos)
                except Exception:
                    print(self.__msg_release_url_error)
            else:
                print(self.__msg_required_choose_platform)
            sys.exit(0)

        ###################
        # DOWNLOAD LATEST #
        ###################
        self.__arg_download_latest = self.__args.download_latest
        if self.__arg_passed(self.__arg_download_latest):
            if not self.__arg_download_latest:
                print(self.__msg_required_choose_platform)
                print(self.__msg_optional_add_extract)
                sys.exit(0)
            extract = False
            self.__arg_extract = self.__args.extract
            if self.__arg_passed(self.__arg_extract):
                extract = True
            platform = self.__arg_download_latest[0]
            if platform in self.__platforms.list:
                # noinspection PyBroadException
                try:
                    if not self.download_latest_release(platform, extract):
                        print(self.__msg_download_error)
                    else:
                        print(self.__msg_download_finished)
                except GetGeckoDriverError:
                    print(self.__msg_download_error)
            else:
                print(self.__msg_required_choose_platform)
                print(self.__msg_optional_add_extract)
            sys.exit(0)

        ####################
        # DOWNLOAD RELEASE #
        ####################
        self.__arg_download_release = self.__args.download_release
        if self.__arg_passed(self.__arg_download_release):
            custom_required_message = (self.__msg_required_choose_platform
                                       + '\n' + self.__msg_required_add_release)
            if not self.__arg_download_release:
                print(custom_required_message)
                print(self.__msg_optional_add_extract)
                sys.exit(0)
            if len(self.__arg_download_release) != 2:
                print(custom_required_message)
                print(self.__msg_optional_add_extract)
                sys.exit(0)
            extract = False
            self.__arg_extract = self.__args.extract
            if self.__arg_passed(self.__arg_extract):
                extract = True
            if len(self.__arg_download_release) != 2:
                print(custom_required_message)
                print(self.__msg_optional_add_extract)
                sys.exit(0)
            else:
                platform = self.__arg_download_release[0]
                if platform in self.__platforms.list:
                    release = self.__arg_download_release[1]
                    # noinspection PyBroadException
                    try:
                        self.download_release(platform, release, extract)
                        print(self.__msg_download_finished)
                    except GetGeckoDriverError:
                        print(self.__msg_download_error)
                else:
                    print(custom_required_message)
                    print(self.__msg_optional_add_extract)
            sys.exit(0)

        ###########
        # VERSION #
        ###########
        self.__arg_version = self.__args.version
        if self.__arg_passed(self.__arg_version):
            print('v' + __version__)
            sys.exit(0)

    def __arg_passed(self, arg):
        if isinstance(arg, list):
            return True
        return False

    def print_latest_urls(self):
        latest = 'Latest release for '

        get_driver = GetGeckoDriver(self.__platforms.win_32_arch)
        print(latest + 'Windows 32:')
        print(get_driver.latest_release_url())
        print('')

        get_driver = GetGeckoDriver(self.__platforms.win_64_arch)
        print(latest + 'Windows 64:')
        print(get_driver.latest_release_url())
        print('')

        get_driver = GetGeckoDriver(self.__platforms.linux_32_arch)
        print(latest + 'Linux 32:')
        print(get_driver.latest_release_url())
        print('')

        get_driver = GetGeckoDriver(self.__platforms.linux_64_arch)
        print(latest + 'Linux 64:')
        print(get_driver.latest_release_url())
        print('')

        get_driver = GetGeckoDriver(self.__platforms.macos)
        print(latest + 'macOS:')
        print(get_driver.latest_release_url())

    def print_latest_version(self):
        get_driver = GetGeckoDriver(self.__platforms.win_32_arch)
        release = get_driver.latest_release_version()
        if release is None:
            print(self.__c_fore.RED + 'error: could not find the latest release version' + self.__c_style.RESET_ALL)
        else:
            print(release)

    def print_latest_url(self, platform):
        get_driver = GetGeckoDriver(platform)
        print(get_driver.latest_release_url())

    def print_release_url(self, platform, release):
        get_driver = GetGeckoDriver(platform)
        print(get_driver.release_url(release))

    def download_latest_release(self, platform, extract):
        get_driver = GetGeckoDriver(platform)
        if get_driver.download_latest_release(extract=extract):
            return True
        return False

    def download_release(self, platform, release, extract):
        get_driver = GetGeckoDriver(platform)
        get_driver.download_release(release, extract=extract)
