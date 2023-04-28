import os


def config_musescore(path):
    os.environ["MUSESCORE_PATH"] = f"{path}"
