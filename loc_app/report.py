from synonyms     import name2cas,cas2mw
from standard     import read_standards_directory
from util         import describe_comparison,convert_units,fmt_sigfigs
from sys          import stdout
from locale       import getlocale,setlocale,LC_ALL

import re, os

all_standards=read_standards_directory(['datatables','standards'])

if (getlocale() == (None, None)):
    setlocale(LC_ALL, 'en_US.UTF8')

class LocReport():
    """A levels of concern report.
    """

    def __init__(self,
                 units      = None,
                 sample     = None,
                 user       = None,
                 form       = {}):  # any remaing form data; contains i.e. chemicals
        """
        'chemicals': list of common names of chemicals to report on
        'criteria':  list of names of criterion sources
        """
        chemicals = self._chemicals_from_form_data(form)
        
        # Default parameters
        if chemicals is None: chemicals = []
        if sample    is None: sample    = {}
        if user      is None: user      = {}
        if units     is None: units     = {'in':'ppb', 'out':'ppb'}

        # Remember requested units, sample info, and user
        self._units = units;
        self._units['in_rep']   = self._represent_units(units['in'])
        self._units['out_rep']  = self._represent_units(units['out'])
        self._units['in_long']  = self._describe_units(units['in'])
        self._units['out_long'] = self._describe_units(units['out'])

        self._sample = {'name':      None,
                        'date':      None,
                        'location':  None}
        for k in sample.keys(): self._sample[k] = sample[k]

        self._user=user

        standards = self._standards_from_form_data(form)

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
            chemical['name']=chemical['name'].title()
            cas = name2cas(chemical['name'])
            if cas is None:
                self._failed_lookups.append(chemical)
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
                           'level_inunits_rep': fmt_sigfigs(level),
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
                if report_levels:
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

    def _standards_from_form_data(self, form):
        """
        report base class just uses all available standards.
        """
        return all_standards.keys()

    def _chemicals_from_form_data(self, form):
        # look for all 'chem*' parameters that have a corresponding 'report*' parameter
        chem_pattern = re.compile('^chem(\d+)$')

        chem_all_keys  = filter (chem_pattern.match, form.keys())
        chem_used_keys = filter (lambda k: form[k], chem_all_keys)
        chem_used_keys.sort()

        def chem_lookup(chem_par):
            n = chem_pattern.findall(chem_par)[0]
            report_par = 'report' + n
            return { 'name'  : form[chem_par].lower(),
                     'level' : form[report_par] if report_par in form else 'NA' }

        return map (chem_lookup, chem_used_keys)
        
    def _represent_units(self, name):
        """Given a key 'name', return a markdown representation of how that
        unit should be represented in the output
        """
        unit_representations = self._unit_representations()

        if name in unit_representations:
            return (unit_representations[name])
        else:
            return (name)

    def _describe_units(self, name):
        """Given a key 'name', return a markdown description of those units
        """
        unit_descriptions = self._unit_descriptions()
        if name in unit_descriptions:
            return (unit_descriptions[name])
        else:
            return (name)

    def _unit_representations(self):
        return {}
    
    def _unit_descriptions(self):
        return {}

    def failed_lookups(self):
        return self._failed_lookups

    def failed_conversions(self):
        return self._failed_conversions

    def chemicals(self):
        return self._chemicals

    def standards(self):
        return self._standards

    def units(self, key):
        return self._units[key]
        
    def sample(self):
        return self._sample

    def users(self):
        return self._user

    def user(self, field='first'):
        if field in self._user:
            return self._user[field]
        else:
            return None

    def reply(self):
        content_fname = self.generate()
        headers       = self.http_headers()

        return (content_fname, headers)

        try:
            fh = open(content_fname)

            for hdr in self.http_headers():
                print hdr
            print
            stdout.flush()
        
            content = fh.read()
            stdout.write(content)
            fh.close()
            os.remove(content_fname)

        except (IOError, TypeError):
            print """Content-type: text/plain

Something went wrong generating content.  That's all I know.
"""
        



