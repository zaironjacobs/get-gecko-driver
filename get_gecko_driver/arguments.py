descriptor = '  {:<30} {}'
message_help_required_version = descriptor.format('', 'required: add a version')
message_help_optional_extract = descriptor.format('', 'optional: use --extract to extract the zip file')

args_options = [
    ['--latest-version', 'print the latest version'],
    ['--latest-urls', 'print latest version urls for all platforms'],
    ['--version-url', 'print the version url' + '\n'
     + message_help_required_version],
    ['--latest-url', 'print the latest version url for a platform' + '\n'],
    ['--download-latest', 'download the latest version for a platform' + '\n'
     + message_help_optional_extract],
    ['--download-version', 'download a specific version' + '\n'
     + message_help_required_version + '\n'
     + message_help_optional_extract],
    ['--extract', 'extract the compressed driver file'],
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
    print('The downloaded driver can be found at: ')
    print('<current directory>/<geckodriver>/<version>/<bin>/<geckodriver>')
