from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.5'
DESCRIPTION = 'A MIDI file analyzer with a few additional functionality'
LONG_DESCRIPTION = 'A MIDI file analyzer which allows you to go through components of a MIDI file and extract data. Also has functionality such as generating pdfs <br><br> For documentation, go to [swayamsahoo11742.github.io](https://swayamsahoo11742.github.io/) <br><br> For Github page, go to [https://github.com/SwayamSahoo11742/Scopul](https://github.com/SwayamSahoo11742/Scopul) '

# Setting up
setup(
    name="scopul",
    version=VERSION,
    author="SwayamSahoo11742",
    author_email="<swayamsa01@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['music21', 'mido'],
    keywords=['python', 'scopul', 'MIDI', 'sheet music', 'midi anazyler', 'music'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)