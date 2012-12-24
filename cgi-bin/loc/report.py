from loc.synonyms import name2cas,cas2mw
from loc.standard import read_standards_directory
from loc.util     import describe_comparison,convert_units,fmt_sigfigs,represent_units

all_standards=read_standards_directory(['datatables','standards'])

class LocReport():
    """A levels of concern report.
    """

    def __init__(self,
                 chemicals=[],
                 standards=None,
                 units={'in':'ppb','out':'ppb'},
                 user={},     # can contain: first, second
                 sample={}):  # can contain: location, date, name
        """
        'chemicals': list of common names of chemicals to report on
        'criteria':  list of names of criterion sources
        """
        # Remember requested units, sample info, and user
        self._units = units;
        self._units['in_rep']  = represent_units(units['in'])
        self._units['out_rep'] = represent_units(units['out'])

        self._sample = {'name':      None,
                        'date':      None,
                        'location':  None}
        for k in sample.keys(): self._sample[k] = sample[k]

        self._user=user

        # Remember requested standards; if none specified, use all available
        if standards is None:
            self._standards=all_standards
        else:
            self._standards={}
            for name in standards:
                if name in all_standards:
                    self._standards[name]=all_standards[name]

        self._failed_lookups=[]
        self._failed_conversions=[]
        self._chemicals=[]

        # map input chemical names to chemical objects
        for chemical in chemicals:
            cas = name2cas(chemical['name'])
            if cas is None:
                self._failed_lookups.append(chemical['name'])
            else:
                mw = cas2mw(cas)
                try:
                    level=float(chemical['level'])
                    level_in_outunits = convert_units(level,units['in'],units['out'],mw)
                    entry={'name':        chemical['name'],
                           'cas':         cas,
                           'mw':          mw,
                           'level':       level_in_outunits,
                           'level_rep':   fmt_sigfigs(level_in_outunits),
                           'comparisons': []}
                    self._chemicals.append(entry)

                except TypeError:
                    self._failed_conversions.append(chemical['name'])
                except ValueError:
                    self._failed_conversions.append(chemical['name'])

        cas_list = map(lambda c: c['cas'], self._chemicals)
        for (name,standard) in zip(self._standards.keys(),self._standards.values()):
            standard.prefetch(cas_list)
            standard_units=standard.meta['units']
            for chemical in self._chemicals:
                # Unfold requested standards into individual criteria
                report_levels = standard.lookup(chemical['cas'])
                for criterion_name in report_levels.keys():
                    try:
                        criterion_level = convert_units(report_levels[criterion_name],standard.meta['units'],units['out'],chemical['mw'])
                        chemical['comparisons'].append({'level':         criterion_level,
                                                        'level_rep':     fmt_sigfigs(criterion_level),
                                                        'description':   describe_comparison(chemical['level'],criterion_level),
                                                        'criterion':     standard.criteria[criterion_name],
                                                        'source':        standard.meta['name']})
                    except TypeError:
                        self._failed_conversions.append(chemical['name'])

    def failed_lookups(self):
        return self._failed_lookups

    def failed_conversions(self):
        return self._failed_conversions

    def chemicals(self):
        return self._chemicals

    def standards(self):
        return self._standards

    def units(self):
        return self._units
        
    def sample(self):
        return self._sample

    def user(self, field='first'):
        if field in self._user:
            return self.user[field]
        else:
            return None
