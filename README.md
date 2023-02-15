![Scopul](https://user-images.githubusercontent.com/117121187/219178220-f0db6cef-ab90-406f-acfc-e14b6ff8677d.jpg)

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

## Link
Documentaion - [https://swayamsahoo11742.github.io/](https://swayamsahoo11742.github.io/)

Documentation Source Code - [https://github.com/SwayamSahoo11742/SwayamSahoo11742.github.io/](https://github.com/SwayamSahoo11742/SwayamSahoo11742.github.io/)

PyPi - [https://pypi.org/project/scopul/](https://pypi.org/project/scopul/)

GitHub - [https://github.com/SwayamSahoo11742/Scopul/](https://github.com/SwayamSahoo11742/Scopul/)


## Contact or Help us!
If you encounter any bugs, kindly send me an email at swayamsa01@gmail.com. If you have any suggestions or would like to contribute to the improvement of the code, including efficiency and best practices, feel free to reach out to me via email or create a pull request. I most likely won’t be actively adding and developing this project, but I will still implement any sugegstions that are fit.

Thank you very much!
