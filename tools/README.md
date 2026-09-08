# Generator

```bash
cd tools
python parse_seed.py     # pulls the workbook from the iCloud share (or --local), writes seed.json
python build.py          # seed.json + template.html -> ../index.html
```

Needs Python 3 and `openpyxl`. Coordinates live in `parse_seed.py` (`COORDS`, WGS-84 -> GCJ-02).
