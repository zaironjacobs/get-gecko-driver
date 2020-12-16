class Platforms:

    def __init__(self):
        self.list = self.__list()

        self.win_32_arch = self.__win_arch_32()
        self.win_64_arch = self.__win_arch_64()
        self.linux_32_arch = self.__linux_arch_32()
        self.linux_64_arch = self.__linux_arch_64()
        self.macos = self.__macos()

    def __win_arch_32(self):
        return 'win32'

    def __win_arch_64(self):
        return 'win64'

    def __linux_arch_32(self):
        return 'linux32'

    def __linux_arch_64(self):
        return 'linux64'

    def __macos(self):
        return 'macos'

    def __list(self):
        return [self.__win_arch_32(), self.__win_arch_64(), self.__linux_arch_32(), self.__linux_arch_64(),
                self.__macos()]
