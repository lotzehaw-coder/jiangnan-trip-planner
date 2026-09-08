# Generator

`index.html` is built from the workbook:

```bash
cd tools
python parse_seed.py          # itinerary.xlsx -> seed.json
python -c "t=open('template.html',encoding='utf-8').read();s=open('seed.json',encoding='utf-8').read();open('../index.html','w',encoding='utf-8').write(t.replace('__SEED__',s.replace('</script','<\/script')))"
```

Needs Python 3 and `openpyxl`.
