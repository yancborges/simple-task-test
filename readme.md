### CSV Reader

# About:
I've tried to code this how i imagine that Pandas works with csv reading.
So There is a class that recieves a path or url and read a file from there.

# Running:
```
from reader import Reader
r = Reader('my_file.csv')

or

from reader import Reader
r = Reader('https://www.website.com/my_file.csv)
```

# Files:
The Reader class accepts csv, txt, there is also a support for zipped files.
But nested files must be csv or txt.

# Dependencies:
copy
requests
json
urllib
io
zipfile

* I know some of them are not builtin libs, but
i used them for making some things quicker,
like reading files from web (and also because i have no idea
how to do this without from scratch)

# Output:
A list of documents is outputed for each inputed file line, s the following format:
```
{'fields': {'ASSESSMENT_CODE\r': '2\r', 'ENERGY_PRODUCT': 'LNG', 'FLOW_BREAKDOWN': 'EXPLNG', 'OBS_VALUE': '756.976', 'REF_AREA': 'AE', 'UNIT_MEASURE': 'M3', '_ENERGY_PRODUCT': 'Liquefied Natural Gas', '_FLOW_BREAKDOWN': 'Exported LNG', '_REF_AREA': 'United Arab Emirates'}, 'points': ['2015-01'], 'series_id': 'jodi-data//AE//EXPL...//2015-01'}
```

# Important:
For some reasing this code is absolutly slow.
I've tried to decrease it, but couldn't reach a 'waitable' process time.
(It needs up to 60 minutes to run all lines from jodi-data file)
I'm going to keep working at this, but the main task is done.