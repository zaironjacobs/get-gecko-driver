class GetGeckoDriverError(Exception):
    pass


class VersionUrlError(GetGeckoDriverError):
    pass


class UnknownPlatformError(GetGeckoDriverError):
    pass


class UnknownVersionError(GetGeckoDriverError):
    pass


class DownloadError(GetGeckoDriverError):
    pass
