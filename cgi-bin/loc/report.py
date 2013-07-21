from loc.synonyms import name2cas,cas2mw
from loc.standard import read_standards_directory
from loc.util     import describe_comparison,convert_units,fmt_sigfigs
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
                 form       = None,     # a form containing cgi input
                 chemicals  = None,
                 standards  = None,
                 units      = None,
                 user       = None,     # can contain: first, second
                 sample     = None):    # can contain: location, date, name
        """
        'chemicals': list of common names of chemicals to report on
        'criteria':  list of names of criterion sources
        """
        if form:
            cgi_pars  = self._pull_from_cgi(form)
            
            chemicals = cgi_pars['chemicals']
            user      = cgi_pars['user']
            units     = cgi_pars['units']
            sample    = cgi_pars['sample']
            standards = self._standards_from_cgi(form)

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
                    entry={'name':        chemical['name'],
                           'cas':         cas,
                           'mw':          mw,
                           'level_inunits_rep': chemical['level'],
                           'level_inunits':     float(chemical['level']),
                           'comparisons': []}

                    if (units['in'] == units['out']):
                        entry.update({'level_rep': entry['level_inunits_rep'],
                                      'level':     entry['level_inunits']})
                    else:
                        level_outunits = convert_units(entry['level_inunits'],units['in'],units['out'],mw)
                        entry.update({'level':     level_outunits,
                                      'level_rep': fmt_sigfigs(level_outunits)})

                    self._chemicals.append(entry)

                except TypeError:
                    self._failed_conversions.append(chemical)
                except ValueError:
                    self._failed_conversions.append(chemical)

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
                            entry = {'source':     standard.meta['name'],
                                     'criterion':  standard.criteria[criterion_name]}
                            if (standard.meta['units'] == units['out']):
                                entry.update({'level_rep':   report_levels[criterion_name],
                                              'level':       float(report_levels[criterion_name])})
                            else:
                                criterion_level = convert_units(float(report_levels[criterion_name]),
                                                                standard.meta['units'],
                                                                units['out'],
                                                                chemical['mw'])
                                entry.update({'level':     criterion_level,
                                              'level_rep': fmt_sigfigs(criterion_level)})
                            entry['description'] = describe_comparison(chemical['level'], entry['level'])
                            chemical['comparisons'].append(entry)
                            if (chemical['level'] > entry['level']):
                                chemical['has_overages'] = True
                        except TypeError:
                            self._failed_conversions.append(chemical['name'])
        self._chemicals.sort(key=lambda c: ['aaaa' + c['name'], c['name']]['has_overages' in c])

    def _standards_from_cgi(self, form):
        """
        report base class just uses all available standards.
        """
        return all_standards.keys()

    def _pull_from_cgi(self, form):
        """PUll the report parameters from expected locations in an HTML form.
        """
        result = {}

        # look for all 'chem*' parameters that have a corresponding 'report*' parameter
        chem_pattern = re.compile('^chem(\d+)$')
        
        def chem_lookup(chem_par):
            n = chem_pattern.findall(chem_par)[0]
            report_par = 'report' + n
            return { 'name'  : form[chem_par].value.lower(),
                     'level' : form[report_par].value if report_par in form else 'NA' }

        result['chemicals'] = map (chem_lookup, filter (chem_pattern.match, form.keys()))
        result['chemicals'].sort(key=lambda c:c['name'])
        result['units']     = {'in'  : form.getvalue('inunits'),
                               'out' : form.getvalue('outunits')}

        result['user']      = {'first':  form.getvalue('tablename')  or '',
                               'second': form.getvalue('tablename2') or ''}

        result['sample']    = {'name':   form.getvalue('samplename'),
                               'date':   form.getvalue('sampledate'),
                               'location': form.getvalue('samplelocation')
                              }

        return result

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

    def http_reply(self):
        content_fname=self.generate()

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
        



