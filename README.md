![Scopul](https://user-images.githubusercontent.com/117121187/219178220-f0db6cef-ab90-406f-acfc-e14b6ff8677d.jpg)

![PyPI - Status](https://img.shields.io/pypi/status/Scopul)
![PyPI](https://img.shields.io/pypi/v/scopul)
![PyPI - Downloads](https://img.shields.io/pypi/dm/scopul)

`Scopul` is a python package to extract data from MIDI files!

![scopul-rep](https://user-images.githubusercontent.com/117121187/219198671-72a73a16-b168-4b4c-abe5-e384c9624e3c.gif)

Scopul can also do additional functionality such as generating PDFs or tempo conversions.


## Installation
```cmd
$ pip install scopul
```

## Simple Example

```python
from Scopul import Scopul, config_musescore

scop = Scopul("test.mid")


# Get tempo
print(scop.tempo.ratio)


# Sample output
>>> "3/4"

```
## Future Plans
### Things to look forward in the next release, any suggestions will be appreciated
- Time signature conversions
- Tempo conversions
- Extract a specific rhythm
- Altering MIDI (adding/Deleting measures or notes)

### Things for the distant future, any suggestions will be appreciated
- Chord extraction: Allow the extraction of chord progressions from the MIDI file.
- Key detection: Implement a function to detect the key of the MIDI file.
- Melody extraction: Allow the extraction of the melody from the MIDI file.
- Harmonic analysis: Provide harmonic analysis of the MIDI file by identifying chords and their progressions.
- Drum track extraction: Allow the extraction of the drum track from the MIDI file.
- Time signature detection: Implement a function to detect the time signature of the MIDI file.
- Quantization: Implement a function to quantize the notes in the MIDI file to a particular grid size.
- Instrument recognition: Provide functionality to recognize the instruments used in the MIDI file.
- MIDI file validation: Implement a function to validate the structure of the MIDI file and detect any errors.
- Export to other formats: Allow the export of the MIDI data to other formats such as CSV, JSON, or XML.

## Links
Documentaion - [https://swayamsahoo11742.github.io/](https://swayamsahoo11742.github.io/)

Documentation Source Code - [https://github.com/SwayamSahoo11742/SwayamSahoo11742.github.io/](https://github.com/SwayamSahoo11742/SwayamSahoo11742.github.io/)

PyPi - [https://pypi.org/project/scopul/](https://pypi.org/project/scopul/)

GitHub - [https://github.com/SwayamSahoo11742/Scopul/](https://github.com/SwayamSahoo11742/Scopul/)

## Credits
Thanks to [Music21](https://web.mit.edu/music21/doc/) and [MuseScore](https://musescore.org/en/download) for making this possible

## Contact or Help us!
If you encounter any bugs, kindly send me an email at swayamsa01@gmail.com. If you have any suggestions or would like to contribute to the improvement of the code, including efficiency and best practices, feel free to reach out to me via email or create a pull request. I most likely won’t be actively adding and developing this project, but I will still implement any sugegstions that are fit.

Thank you very much!
