# GSheet [![Build Status](https://travis-ci.org/DKorytkin/gsheet.svg?branch=master)](https://travis-ci.org/DKorytkin/gsheet) [![cov](https://codecov.io/gh/DKorytkin/gsheet/branch/master/graph/badge.svg)](https://codecov.io/gh/DKorytkin/gsheet)

Simple library writing data to google sheets


## Quick start 

- Install GSheet
```bash
pip install git+https://github.com/DKorytkin/gsheet.git
```
- go to [google dev console](https://console.developers.google.com/apis/)
- create user profile
- add Google Drive API
- add Google Sheets API
- generate `secret_file.json`

## How to use?
Simple tutorial and examples:

### Create first document
```python
import os

from gsheet import Sheet


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SECRET_FILE_PATH = os.path.join(BASE_DIR, 'secret_key.json')


sheet = Sheet(SECRET_FILE_PATH)
sheet.create('My first document', 'My first sheet name')

```

### Get exist document by id

Shared this document only read by default
```python
from gsheet import Sheet

sheet = Sheet(SECRET_FILE_PATH)
sheet.get_spreadsheet('jhf99788dfshdkfhsdhfdgjhsdg')
```

### Get exist sheet in spreadsheet
```python
from gsheet import Sheet

sheet = Sheet(SECRET_FILE_PATH)
sheet.get_sheet('My first sheet name')
```

### Get document url
```python
from gsheet import Sheet

sheet = Sheet(SECRET_FILE_PATH)
sheet.get_spreadsheet('jhf99788dfshdkfhsdhfdgjhsdg')
sheet.get_url()
```

### Add data to created document
```python
from gsheet import Sheet

sheet = Sheet(SECRET_FILE_PATH)
sheet.get_spreadsheet('jhf99788dfshdkfhsdhfdgjhsdg')
v = sheet.value()

# add title to table
v.add_row(row_number=1, values=['ids', 'keys', 'values'])

# add row to table
v.add_row(row_number=2, values=['1', 'key1', 'value1'])
v.apply()
```

### Format document
```python
from gsheet import Sheet

sheet = Sheet(SECRET_FILE_PATH)
sheet.get_spreadsheet('jhf99788dfshdkfhsdhfdgjhsdg')
f = sheet.format()

# text position center by default
f.format_cell(cell_range='A1:C1', b_color='#000', f_color='#fff')

# if you want use format
from helpers import get_color
my_format = {
    'horizontalAlignment': 'CENTER',
    'verticalAlignment': 'MIDDLE',
    'backgroundColor': {
        'red': 1.0,
        'green': 1.0,
        'blue': 1.0
    },
    'textFormat': {
        'bold': True,
        'foregroundColor': get_color('#666')
    }
}
f.format(cell_range='A1:C1', user_format=my_format)
f.apply()
```

### Marge table cell
```python
from gsheet import Sheet

sheet = Sheet(SECRET_FILE_PATH)
sheet.get_spreadsheet('jhf99788dfshdkfhsdhfdgjhsdg')
f = sheet.format()

f.merge('A2:A10')
f.apply()
```