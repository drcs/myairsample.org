import json

from os.path import splitext

def basename(fname):
    return splitext(fname)[0]

infile=open('criteria.json','r')
criteria=json.load(infile)
infile.close()

bySource = {}

for c in criteria:
    if (not (c['source'] in bySource)):
        bySource[c['source']] = []
    bySource[c['source']].append(c)

def xformStd(std):
    return { 'description':
                 { 'short': std['description'],
                   'brief': std['brief_description'],
                   'long':  std['long_description'] },
             'name': std['column'],
             'use':  True }

def xformSrc(src):
    initial_columns  = [{'name': 'pollutant', 'use': False},
                        {'name': 'CAS', 'use': False}]
    standard_columns = map(xformStd, src)
    return { 'name':    basename(src[0]['source']),
             'units':   src[0]['units'],
             'columns': initial_columns + standard_columns}

for k in bySource.keys():
    outfile=open(k + '.json', 'w')
    json.dump(xformSrc(bySource[k]), outfile, indent=4)
    outfile.close()

pass



