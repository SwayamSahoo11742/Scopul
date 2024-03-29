class InvalidFileFormatError(Exception):
    def __init__(self, value) -> None:
        self.value = value


class InvalidMusicElementError(Exception):
    def __init__(self, value) -> None:
        self.value = value


class NoMusePathError(Exception):
    def __init__(self, value) -> None:
        self.value = value


class MeasureNotFoundException(Exception):
    def __init__(self, value) -> None:
        self.value = value

class PercussionChordifyError(Exception):
    def __init__(self, value) -> None:
        self.value = value