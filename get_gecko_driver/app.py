import typer

from get_gecko_driver import __version__
from get_gecko_driver.enums import OsPlatform
from get_gecko_driver.exceptions import GetGeckoDriverError
from get_gecko_driver.get_driver import GetGeckoDriver

app = typer.Typer(name="Get GeckoDriver", add_completion=False)
get_driver = GetGeckoDriver()


@app.command()
def main(
    latest_version: bool = typer.Option(
        default=False, help="Print the latest version", show_default=False
    ),
    latest_urls: bool = typer.Option(
        default=False,
        help="Print latest version urls for all platforms",
        show_default=False,
    ),
    version_url: str = typer.Option(
        default=None, help="Print the version download url", show_default=False
    ),
    latest_url: bool = typer.Option(
        default=False,
        help="Print the latest version url for a platform",
        show_default=False,
    ),
    download_latest: bool = typer.Option(
        default=False,
        help="Download the latest version for a platform",
        show_default=False,
    ),
    download_version: str = typer.Option(
        default=None, help="Download a specific version", show_default=False
    ),
    extract: bool = typer.Option(
        default=False, help="Extract the compressed driver file", show_default=False
    ),
    driver_filename: bool = typer.Option(
        default=False, help="Driver filename", show_default=False
    ),
    version: bool = typer.Option(
        default=False, help="Application version", show_default=False
    ),
):
    """
    Main.
    """

    if latest_urls:
        __print_latest_urls()

    elif version_url:
        __print_version_url(version=version_url)

    elif download_latest:
        __download_latest_version(extract=extract)

    elif download_version:
        __download_version(version=download_version, extract=extract)

    elif latest_url:
        __print_latest_url()

    elif latest_version:
        __print_latest_version()

    elif driver_filename:
        print(get_driver.driver_filename())

    elif version:
        print(f"v{__version__}")


def __print_latest_urls():
    """
    Print the latest url version for all platforms.
    """

    get_driver_win = GetGeckoDriver(OsPlatform.win)
    get_driver_linux = GetGeckoDriver(OsPlatform.linux)
    get_driver_mac = GetGeckoDriver(OsPlatform.mac)
    get_drivers = {
        "Windows": get_driver_win,
        "Linux": get_driver_linux,
        "macOS": get_driver_mac,
    }

    result = ""
    for index, (key, value) in enumerate(get_drivers.items()):
        try:
            result += f"Latest version for {key}:"
            result += value.latest_version_url()
            if index < len(get_drivers) - 1:
                result += "\n"
        except GetGeckoDriverError:
            continue

    print(result)


def __print_latest_version():
    """
    Print the latest version.
    """

    error = ""

    try:
        print(get_driver.latest_version())
    except GetGeckoDriverError:
        print(error)


def __print_latest_url():
    """
    Print the url of the latest version.
    """

    error = "Could not find version url"

    try:
        print(get_driver.latest_version_url())
    except GetGeckoDriverError:
        print(error)


def __print_version_url(version: str):
    """
    Print the url for a given version.

    :param version: Geckodriver version.
    """

    error = "Could not find version url"

    try:
        print(get_driver.version_url(version))
    except GetGeckoDriverError:
        print(error)


def __download_latest_version(extract: bool):
    """
    Download the latest version.

    :param extract: Extract the downloaded driver or not.
    """

    error = "Could not download latest version"

    try:
        get_driver.download_latest_version(extract=extract)
    except GetGeckoDriverError:
        print(error)


def __download_version(version: str, extract: bool):
    """
    Download driver version.

    :param version: Geckodriver version.
    :param extract: Extract the downloaded driver or not.
    """

    error = "Could not download latest version"

    try:
        get_driver.download_version(version=version, extract=extract)
    except GetGeckoDriverError:
        print(error)
