"""Look up chemical CAS numbers by common name,
   and MW by CAS
"""
from os import path
import csv
from util import canonical_name

_fh=open(path.join('datatables','synonyms.txt'), 'r')
# FIXME check return value

_dialect = csv.Sniffer().sniff(_fh.read(1024))
_fh.seek(0)

_name_table={}
_mw_table={}

_reader = csv.DictReader(_fh, fieldnames=['name','cas','mw'], dialect=_dialect)
for row in _reader:
    if 'cas' in row:
        cas=canonical_name(row['cas'])
        if 'name' in row:
            name=canonical_name(row['name'])
            _name_table[name]=cas
        if 'mw' in row:
            try:
                _mw_table[cas] = float(row['mw'])
            except ValueError:
                pass
            except TypeError:
                pass

_fh.close()

def name2cas(name):
    name=canonical_name(name)
    if name in _name_table:
        return _name_table[name]
    else:
        return None

def cas2mw(cas):
    if cas in _mw_table:
        return _mw_table[cas]
    else:
        return None

