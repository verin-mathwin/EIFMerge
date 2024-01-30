Takes a folder and merges all EIF files (RIEGL image event timestamps) into one dataframe, then gives the length (i.e. timestamp count) of the dataframe.
This number can then be compared against the image file count, to ensure no bonus images or timestamps are present (or rather, to check for them.)

Provided without guarantee, whipped up pretty quickly. Has some commentary. 
If you add geopandas, you could very easily use it to convert the eif to shp for another process, but most GIS tools can do this already.

REQUIRES: py 3.7+, pandas, os, itertools.

TODO - disclaimer, may never actually be done: 
- modularise this script further
- argv, to make editign script to set path unnecessary.
- simplify and improve the readability of the dataCheck and checkLooksRight - the "business end" of these could be written as a oneliner lambda, but not today!
