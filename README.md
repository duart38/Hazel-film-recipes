# Hazel film recipes

Film-simulation recipes for Hazel, the film-look engine for the X1D-50c. The Hazel app on the Mac
and iPad reads this collection each time it starts: these are the recipes under "Included with
Hazel" in its Recipes tab. Edit a copy of one there to add it to your library, and from there to
the camera's recipe slots like any other recipe. A change merged here reaches the app the next
time it starts, with no app update; offline, the app keeps the copy it last read.

To put Hazel on the camera, see [Hazel-firmware](https://github.com/duart38/Hazel-firmware). It
also works without the app: copy a recipe file onto the memory card as `HAZEL/recipes/C1.txt`
(up to `C7.txt`, one per slot), and pick it on the camera under Settings › Extras.

There are no sample pictures here on purpose: try a recipe on your own photos in the app.

## The recipes

| Recipe | Look |
| --- | --- |
| Gold 200 | Warm, golden consumer-film colour with cyan-blue skies. Inspired by Kodak Gold 200 |
| Tungsten 800T | Night-time cinema colour: red halation around lights, teal shadows, rich reds. Inspired by CineStill 800T |
| Warm portrait | Warm, soft colour with golden skin. Inspired by Kodak Portra 400 |
| Faded chrome | Quiet colour, deep shadows, soft highlights |
| Soft pastel | Light, low-contrast and slightly soft |
| Neutral | The camera's own picture: a slot with no look |
| Silver screen | Deep, cinematic black and white with fine grain. Inspired by the black and white scenes of Oppenheimer |
| Gritty black and white | Hard black and white with coarse grain and strong local contrast |
| Red filter black and white | Dark skies and light skin, as with a red filter on the lens |

Gold 200, Silver screen and Tungsten 800T were matched against real pictures of the look they copy
(scans of the film, stills from the film), measuring tones, grain and colour object by object. Gold 200 and Warm
portrait started from Fuji X Weekly's recipes of the same inspiration, ported to Hazel's settings.

## A recipe file

Plain text, one setting per line. The first line is the name, the second a one-line description;
more `#` lines are notes, such as the white balance and exposure to use on the camera.

```
# Gold 200
# Warm, golden consumer-film colour ...
# On the camera: white balance Daylight, exposure 0 to +2/3.
dynamic_range = 1
highlights = -0.25
grade_highlights = 45, 0.35
mix_blue = -0.4, 0.45, 0
grain = 0.35
```

## Adding or changing a recipe

1. Put the file in `recipes/`, named after the recipe in lower case with dashes
   (`Gold 200` is `recipes/gold-200.txt`).
2. Run `python3 tools/build_index.py` and commit `index.json` with it.

The same script checks every pull request. It refuses a recipe whose name and settings don't fit
the 914 bytes the camera has for a recipe in the record it keeps with every photo, and a name with
a company name in it. Film stock names are fine; say "Inspired by ..." in a note for the rest.

`index.json` is what the app reads: each recipe's name, file and checksum, plus its description,
notes and the settings it uses. The app skips a recipe whose file doesn't match its checksum, whose
first line isn't its name, or that is too long for the camera, and keeps its last good copy. A
recipe using a setting the app doesn't know yet shows as "needs a newer Hazel" instead of looking
wrong.
