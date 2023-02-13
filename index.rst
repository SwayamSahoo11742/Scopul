# Scopul Class
The Scopul class is a class for manipulating and generating music files.

## Class Properties
- Tempo (tempo)
  - The tempo property returns the Tempo object.
  - Example:
    ```python
    scopul_object = Scopul(audio)
    tempo_object = scopul_object.tempo
    ```
- Time Signature (time_sig)
  - The time_sig property returns the TimeSignature object.
  - Example:
    ```python
    scopul_object = Scopul(audio)
    time_sig_object = scopul_object.time_sig
    ```
- Midi File (midi)
  - The midi property returns the midi file.
  - Example:
    ```python
    scopul_object = Scopul(audio)
    midi_file = scopul_object.midi
    ```
  - The midi property can also be set, which will reconstruct the object to change accordingly to a new midi.
  - Example:
    ```python
    scopul_object = Scopul(audio)
    scopul_object.midi = new_audio
    ```
- Parts
  - The parts property returns a list of Part objects.
  - Example:
    ```python
    scopul_object = Scopul(audio)
    part_list = scopul_object.parts
    ```

## Class Methods
- Get Audio Length
  - The `get_audio_lenght()` method returns the length of the audio in seconds.
  - Example:
    ```python
    scopul_object = Scopul(audio)
    audio_length = scopul_object.get_audio_lenght()
    ```
- Generate PDF
  - The `generate_pdf()` method generates a pdf of the midi. It creates a pdf by turning it into musicxml then to pdf.
  - Args:
    - output: a str that represents the name of the file
    - fp: a str that represents the file path as to where to save the pdf. Default is '', which will save to the current working directory
    - overwrite: a boolean, indicates whether to overwrite files or not
  - Returns:
    - None, just generates a pdf in the path specified with the name specified
  - Raises:
    - FileExistsError: if overwrite is False and there is a file at the same path
  - Example:
    ```python
    scopul_object = Scopul(audio)
    scopul_object.generate_pdf("example.pdf")
    ```
- Method generate_musicxml
  - The `generate_musicxml` method generates a musicxml of the midi file.
  - Parameters
    - output: a string that represents the name of the file
    - fp: a string that represents the file path as to where to save the musicxml. Default is '', which will save to the current working directory
    - overwrite: a boolean, indicates whether to overwrite files or not
  - Returns
    - This method returns None, it just generates a musicxml in the path specified with the name specified.
  - Raises
   

## Class Method: `midi_tempo2bpm`
Converts a midi tempo value to bpm

### Parameters
- `tempo`: an int, the midi tempo value to be converted

### Returns
- A float or a list of floats, depending on the input
  - If `tempo` is an int, returns a float
  - If `tempo` is a list, returns a list of floats

### Example
```python
# int input
>>> midi_tempo2bpm(65)
100.0

# list input
>>> midi_tempo2bpm([125, 50, 65])
[200.0, 80.0, 100.0]


## midi_tempo2bpm

Converts a midi tempo value to bpm.

### Args
- `tempo`: An int or a list of ints.

### Returns
A float or a list of floats, depending on the input.

#### Examples

- int input: `midi_tempo2bpm(65)` returns `x` where x is the equivalent bpm value
- list input: `midi_tempo2bpm([125,50,65])` returns `[x1, x2, x3]` where `x1`, `x2`, and `x3` are the equivalent bpm values for each midi tempo value in the list.
```

# bpm2midi_tempo

Converts a bpm value to midi tempo

## Parameters

- tempo (int or list): An int value representing the bpm to be converted to midi tempo.

## Returns

- float or list: Depending on the input, returns either a float value representing the converted midi tempo or a list of float values representing the midi tempo values for each bpm value in the list.

## Example
```
Input (int input):
10000
Output (int output):
500000
```

```
Input (list input):
[10000, 896534, 23334]
Output (list output):
[500000, 4504480, 115197]
```


## Note

This method only accepts an int or list input. If any other type of object is passed as t
