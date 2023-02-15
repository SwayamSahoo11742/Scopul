class InvalidFileFormatError(Exception):
    def __init__(self, value) -> None:
        self.value = value


class InvalidMusicElementError(Exception):
    def __init__(self, value) -> None:
        self.value = value
