from .platforms import Platforms

platforms = Platforms()

descriptor = '  {:<30} {}'
message_help_required_platform = descriptor.format('', 'required: add one of the following platforms '
                                                   + str(platforms.list))
message_help_required_release = descriptor.format('', 'required: add a release version')
message_help_optional_extract = descriptor.format('', 'optional: use --extract to extract the zip file')

args_options = [
    ['--latest-version', 'print the latest release version'],
    ['--latest-release-urls', 'print latest release urls for all platforms'],
    ['--release-url', 'print the url of a release for a platform' + '\n'
     + message_help_required_platform + '\n'
     + message_help_required_release],
    ['--latest-url', 'print the latest release url for a platform' + '\n'
     + message_help_required_platform],
    ['--download-latest', 'download the latest release for a platform' + '\n'
     + message_help_required_platform + '\n'
     + message_help_optional_extract],
    ['--download-release', 'download a release' + '\n'
     + message_help_required_platform + '\n'
     + message_help_required_release + '\n'
     + message_help_optional_extract],
    ['--extract', 'option to extract the zip file'],
    ['--version', 'program version'],
    ['--help', 'show help']
]


def print_help():
    print('usage: ' + 'get-gecko-driver' + ' [options]')
    print('')
    print('options: ')
    for i, argument in enumerate(args_options):
        print(descriptor.format(argument[0], argument[1]))
    print('')
    print('Find the downloaded drivers at: ')
    print('<current directory>/<get-gecko-driver_downloads>/<release version>/<platform>/<geckodriver>')
