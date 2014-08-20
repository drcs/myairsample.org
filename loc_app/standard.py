import csv, json, os
from util import canonical_name

def read_standards_directory(dir_path):
    """
    'dir_path' is a path to standards directories e.g. ['datatables','standards']

    Each standards directory is expected to contain two files:
    1) 'data'  -- tab-delimited standards
    2) 'meta'  -- JSON description of the columns

    Returns a dict of Standard objects keyed by standard directory name
    """
    result={}
    for std in os.listdir(apply (os.path.join, dir_path)):
        result[std]=Standard(apply (os.path.join, dir_path + [std]))
    return result

class Standard():
    """A set of standards from one source.
       
       Standard.lookup(CAS)
       Standard.prefetch([cas1, cas2])
    """
    
    def __init__(self, dir):
        metafile=open(os.path.join(dir, 'meta'), 'r')
        # FIXME check return value
        self.meta=(json.load(metafile))
        # FIXME check return value
        metafile.close()
        self.datafile=os.path.join(dir, 'data')
        self._std_types = []
        self.criteria={}
        for c in self.meta['columns']:
            if c['use']:
                self._std_types.append(c['name'])
                self.criteria[c['name']]=c
        self._cache = {}
        self._csv_dialect = None
        self._fh_data     = None
        self._csv_reader  = None
        try:
            fh=open(os.path.join(dir, 'description'), 'r')
            self._description = fh.read()
            fh.close()
        except IOError:
            self._description = None

    def lookup(self, cas):
        if not cas in self._cache:
            self.prefetch([cas])
        if cas in self._cache:
            return self._cache[cas]
        else:
            return None

    def description(self):
        return self._description

    def oneline_description(self):
        if 'oneline_description' in self.meta:
            return self.meta['oneline_description']
        else:
            return self._description.split("\n")[0]

    def prefetch(self, l_cas):
        reader = self._f_csv_reader()
        for row in reader:
            if 'CAS' in row:
                cas = canonical_name(row['CAS'])
                if cas in l_cas:
                    this_entry = {}
                    for k in row:
                        if k in self._std_types:
                            try:
                                float(canonical_name(row[k]))
                                this_entry[k] = canonical_name(row[k])
                            except ValueError:
                                pass
                    self._cache[cas] = this_entry
        return self

    def _pull_from_cache(self, cas):
        if cas in self._cache:
            return self._cache['cas']
        else:
            return None

    def _f_csv_reader(self):
        if self._csv_reader is None:
            assert (self._fh_data is None)
            fieldnames = map(lambda c: c['name'], self.meta['columns'])
            self._fh_data=open(self.datafile, 'r')
            if self._csv_dialect is None:
                self._csv_dialect = csv.Sniffer().sniff(self._fh_data.read(1024))
                self._fh_data.seek(0)
            self._csv_reader = csv.DictReader(self._fh_data,
                                             fieldnames,
                                             dialect=self._csv_dialect)
        self._fh_data.seek(0)
        return self._csv_reader

all_standards=read_standards_directory(['datatables','standards'])

