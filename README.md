# About

This is a script that converts markdown notes into a flashcards game.
Run via `python game.py /path/to/notes.md`.


Input notes must contain lines in a certain format to be turned into flashcards.

# Notes format

This section contains examples of valid portions of notes that will result in flashcard questions.

## Text question

    - draw full adder: anything here

### Latex only answer

    - draw full adder: has dollar signs, $x\oplus y$, but no markdown image

### Image answer

    - draw full adder: this is $D\in I$ additional text that will be displayed ![full adder](photos/full-adder.png) this additional text is displayed too

### Text only answer

    - draw full adder: no dollar signs or markdown image