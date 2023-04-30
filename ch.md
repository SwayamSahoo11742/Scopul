# Changes

- No more `remove_defects` in `Scopul.generate_pdf` and `Scopul.generate_musicxml` methods
- PDFs now generated using **MuseScore** directly
- no more `Scopul.add_tempo`, `Scopul.add_note`, and `Scopul.add_timeSig` methods. Directly change the part with `Part.insert` method
- Ability to create custom `Part` objects
- New `key` property added to Scopul
- Part.ChordProgression
- Note, Rest and Chord moved to MusicalElements.py
- Part.delete(index)
- Scopul.append_part()


### Chord Progressions!

- New class just dropped -- ChordProgression
- properties:
    - length
    - roman_chords
    - chords
    - key
    - music21

- methods
    - transpose
    - append
    - insert
    - delete

