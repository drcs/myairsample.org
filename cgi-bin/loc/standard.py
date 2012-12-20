
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
        self.csv_dialect = None
        self.fh_data     = None
        self.csv_reader  = None

    def lookup(self, cas):
        # check cache
        # open filehandle
        # FIXME
        pass

    def _pull_from_cache(self, cas):
        if cas in self._cache:
            return self._cache['cas']
        else:
            return None

    def prefetch(self, l_cas):
        if self.csv_reader is None:
            assert (self.fh_data is None)
            fieldnames = map(lambda c: c['name'], self.meta['columns'])
            self.fh_data=open(self.datafile, 'r')
            if self.csv_dialect is None:
                self.csv_dialect = csv.Sniffer().sniff(self.fh_data.read(1024))
                self.fh_data.seek(0)
            self.csv_reader = csv.DictReader(self.fh_data,
                                             fieldnames,
                                             dialect=self.csv_dialect)

