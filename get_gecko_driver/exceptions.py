class GetGeckoDriverError(Exception):
    pass


class ReleaseUrlError(GetGeckoDriverError):
    pass


class UnknownPlatformError(GetGeckoDriverError):
    pass


class UnknownReleaseError(GetGeckoDriverError):
    pass


class DownloadError(GetGeckoDriverError):
    pass
