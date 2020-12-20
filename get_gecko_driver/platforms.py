class Platforms:

    def __init__(self):
        self.win = self.__win()
        self.linux = self.__linux()
        self.macos = self.__macos()

        self.list = self.__list()

        self.win_32 = self.__win_32()
        self.win_64 = self.__win_64()
        self.linux_32 = self.__linux_32()
        self.linux_64 = self.__linux_64()

    def __win(self):
        return 'win'

    def __linux(self):
        return 'linux'

    def __macos(self):
        return 'macos'

    def __win_32(self):
        return 'win32'

    def __win_64(self):
        return 'win64'

    def __linux_32(self):
        return 'linux32'

    def __linux_64(self):
        return 'linux64'

    def __list(self):
        return [self.__win(), self.__linux(), self.__macos()]
