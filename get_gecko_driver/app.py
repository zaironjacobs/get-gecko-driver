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
        self.__msg_required_add_version = (self.__c_fore.RED + 'required: add a version'
                                           + self.__c_style.RESET_ALL)
        self.__msg_optional_add_extract = 'optional: add --extract to extract the zip file'
        self.__msg_error_unrecognized_argument = (
                self.__c_fore.RED + 'error: unrecognized argument(s) detected' + self.__c_style.RESET_ALL
                + '\n' + 'tip: use --help to see all available arguments')
        self.__msg_download_error = (self.__c_fore.RED + 'error: an error occurred at downloading'
                                     + self.__c_style.RESET_ALL)
        self.__msg_version_url_error = (self.__c_fore.RED + 'error: could not find version url'
                                        + self.__c_style.RESET_ALL)
        self.__msg_no_latest_version_url_error = (self.__c_fore.RED
                                                  + 'error: could not find the latest version'
                                                  + self.__c_style.RESET_ALL)
        self.__msg_not_found_error = (self.__c_fore.RED + 'not found'
                                      + self.__c_style.RESET_ALL)

        self.__parser = argparse.ArgumentParser(add_help=False)
        for i, arg in enumerate(arguments.args_options):
            self.__parser.add_argument(arguments.args_options[i][0], nargs='*')
        self.__args, self.__unknown = self.__parser.parse_known_args()

        self.__get_driver = GetGeckoDriver()

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
            self.__print_latest_version()
            sys.exit(0)

        ###############
        # LATEST URLS #
        ###############
        self.__arg_latest_urls = self.__args.latest_urls
        if self.__arg_passed(self.__arg_latest_urls):
            self.__print_latest_urls()
            sys.exit(0)

        ###############
        # VERSION URL #
        ###############
        self.__arg_version_url = self.__args.version_url
        if self.__arg_passed(self.__arg_version_url):
            if len(self.__arg_version_url) < 1:
                print(self.__msg_required_add_version)
            else:
                self.__print_version_url(self.__arg_version_url[0])
            sys.exit(0)

        ##############
        # LATEST URL #
        ##############
        self.__arg_latest_url = self.__args.latest_url
        if self.__arg_passed(self.__arg_latest_url):
            self.__print_latest_url()
            sys.exit(0)

        ###################
        # DOWNLOAD LATEST #
        ###################
        self.__arg_download_latest = self.__args.download_latest
        if self.__arg_passed(self.__arg_download_latest):
            extract = False
            self.__arg_extract = self.__args.extract
            if self.__arg_passed(self.__arg_extract):
                extract = True
            self.__download_latest_version(extract)
            sys.exit(0)

        ####################
        # DOWNLOAD VERSION #
        ####################
        self.__arg_download_version = self.__args.download_version
        if self.__arg_passed(self.__arg_download_version):
            extract = False
            self.__arg_extract = self.__args.extract
            if self.__arg_passed(self.__arg_extract):
                extract = True
            if len(self.__arg_download_version) < 1:
                print(self.__msg_required_add_version)
                print(self.__msg_optional_add_extract)
                sys.exit(0)
            else:
                version = self.__arg_download_version[0]
                self.__download_version(version, extract)
            sys.exit(0)

        ###########
        # VERSION #
        ###########
        self.__arg_version = self.__args.version
        if self.__arg_passed(self.__arg_version):
            print('v' + __version__)
            sys.exit(0)

    def __arg_passed(self, arg) -> bool:
        """ Check if the argument was passed """

        if isinstance(arg, list):
            return True
        return False

    def __print_latest_urls(self) -> None:
        """ Print the latest url version for all platforms """

        get_driver_win = GetGeckoDriver(self.__platforms.win)
        get_driver_linux = GetGeckoDriver(self.__platforms.linux)
        get_driver_macos = GetGeckoDriver(self.__platforms.macos)
        drivers = {'Windows': get_driver_win, 'Linux': get_driver_linux, 'macOS': get_driver_macos}

        for index, (key, value) in enumerate(drivers.items()):
            print('Latest version for ' + key + ': ')
            try:
                print('latest: ' + value.latest_version_url())
            except GetGeckoDriverError:
                print(self.__msg_no_latest_version_url_error)

            if index < len(drivers) - 1:
                print('')

    def __print_latest_version(self) -> None:
        """ Print the latest version """

        try:
            print(self.__get_driver.latest_version())
        except GetGeckoDriverError:
            print(self.__msg_no_latest_version_url_error)

    def __print_latest_url(self) -> None:
        """ Print the url of the latest version """

        try:
            print(self.__get_driver.latest_version_url())
        except GetGeckoDriverError:
            print(self.__msg_version_url_error)

    def __print_version_url(self, version) -> None:
        """ Print the url for a given version """

        try:
            print(self.__get_driver.version_url(version))
        except GetGeckoDriverError:
            print(self.__msg_version_url_error)

    def __download_latest_version(self, extract) -> None:
        """ Download the latest version """

        try:
            self.__get_driver.download_latest_version(extract=extract)
            print(self.__msg_download_finished)
        except GetGeckoDriverError:
            print(self.__msg_download_error)

    def __download_version(self, version, extract) -> None:
        """ Download the version of a given version """

        try:
            self.__get_driver.download_version(version, extract=extract)
            print(self.__msg_download_finished)
        except GetGeckoDriverError:
            print(self.__msg_download_error)
