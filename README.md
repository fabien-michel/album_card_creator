# album_card_creator
Create a printable little card from folder containing a music album

# Usage

Consider a music album :
**/path/to/folder**
```
01 - Title.mp3
02 - Title.mp3
03 - Title.mp3
...
```

"01 - Title.mp3" cover art will be used

Run pdf generation :

```bash
python create_card.py /path/to/folder
```

# Combining pdf
You can use [pdfautonup!](https://framagit.org/spalax/pdfautonup)

<code>pdfautonup *.pdf</code>