
import csv
import json

class Standard():
    
    def __init__(self, dir):
        metafile=open(dir + '/meta', 'r')
        # FIXME check return value
        self.meta=(json.load(metafile))
        # FIXME check return value
        metafile.close()
        self.datafile=dir + '/data'
        self._cache = {}
        self._csv_dialect = None
        self._fh_data     = None
        self._csv_reader  = None

    def lookup(self, cas):
        if not cas in self._cache:
            self.prefetch([cas])
        if cas in self._cache:
            return self._cache[cas]
        else:
            return None

    def prefetch(self, l_cas):
        reader = self._f_csv_reader()
        for row in reader:
            if 'CAS' in row:
                cas = row['CAS']
                if cas in l_cas:
                    self._cache[cas] = row
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

