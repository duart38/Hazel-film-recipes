# Hazel film recipes

Film-simulation recipes for Hazel, the film-look engine for the X1D-50c. The plan is for the Hazel
app on the Mac and iPad to list these and add the ones you pick to your library, from where they
go to the camera's recipe slots like any other recipe. Until then, copy a file into the app.

There are no sample pictures here on purpose: try a recipe on your own photos in the app.

## The recipes

| Recipe | Look |
| --- | --- |
| Gold 200 | Warm, golden consumer-film colour with cyan-blue skies. Inspired by Kodak Gold 200 |
| Warm portrait | Warm, soft colour with golden skin. Inspired by Kodak Portra 400 |
| Faded chrome | Quiet colour, deep shadows, soft highlights |
| Soft pastel | Light, low-contrast and slightly soft |
| Silver screen | Deep, cinematic black and white with fine grain. Inspired by the black and white scenes of Oppenheimer |
| Gritty black and white | Hard black and white with coarse grain and strong local contrast |
| Red filter black and white | Dark skies and light skin, as with a red filter on the lens |

Gold 200 and Silver screen were matched against real pictures of the look they copy (scans of the
film, stills from the film), measuring tones, grain and colour object by object. Gold 200 and Warm
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

The same script checks every pull request. It refuses a recipe whose settings don't fit the
1024 bytes the camera keeps with every photo, and a name with a company name in it. Film stock
names are fine; say "Inspired by ..." in a note for the rest.

`index.json` is what the app reads: each recipe's name, description, notes, file, and the settings
it uses, so an older app can tell when a recipe needs a newer version.
