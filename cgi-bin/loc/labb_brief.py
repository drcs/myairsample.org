"""
LABB report (PDF format), following Gwen's "brief comparison" style
"""

from labb_report import LabbReport, LatexTemplate, md
from string import join

result_section_template = LatexTemplate(r"""
\newpage
\section*{Sample Analysis}
\subst{results}
""")

result_template = LatexTemplate(r"""
\subsection*{\subst{name}}

% Chemical description would go here when implemented

\begin{tabular}{|c|c|p{3in}|}
\hline
The level in your bucket sample &                             & Comparison Level                                       \\
\hline
\subst{comparisons}
\end{tabular}
""")

comparison_template = LatexTemplate(r"""
 \subst{fc} \subst{level}\ \outunits
 &  \subst{fc} \subst{comparison_description}
 &  \subst{fc} \subst{criterion_description} \subst{comparison_level}\ \outunits\\
\hline 
""")

failed_lookup_template = LatexTemplate(r"""
\subsection{\subst{name}}
\begin{tabular}{|c|p{3in}|}
\hline
The level in your bucket sample  & Comparison Level     \\
\hline
\subst{level} \inunits &
Either a comparison level is not available for \subst{name} or the spelling of the chemical name is incorrect. \\
\hline
\end{tabular}
""")

conversion_failed_template = LatexTemplate(r"""
\subsection*{\subst{name}}
Our system cannot handle units of ppbv for \subst{name}.
Please try units of ppb or \micro g/m\cubed.
""")

from pprint import pformat
logfile=open('/tmp/labb.log','w')

class LabbBrief(LabbReport):

    def _standards_from_form_data(self, form):
#        print >>logfile, "reflevel: " + pformat(form['reflevel'].value)
        requested = [ 'ncstds' ]
        if 'reflevel' in form:
            requested = [ form['reflevel'].value ]
        return requested

    def _should_report_comparison(self, chemical, comparison):
        return True

    def _should_report_chemical(self, chemical):
        """
        Should this chemical be included in the report?
        """
        return True

    def _unreport_chemical(self, chemical):
        """
        Alternative action to take for chemicals that are "not reported".
        Return result as a string.
        """
        pass

    def _report_chemical(self, chemical):
        """
        Generate a member of the "results section" for this chemical
        """
        if self._should_report_chemical(chemical):
            def _comp(comparison):
                values = ({'level':                  chemical['level_rep'],
                           'comparison_description': md.convert(comparison['description']),
                           'criterion_description':  md.convert(comparison['criterion']['description']['brief']),
                           'comparison_level':       comparison['level_rep'],
                           'fc': r' \fc ' if chemical['level'] > comparison['level'] else r' \nfc '})
                return comparison_template.substitute(values)

            included_comparisons = filter(lambda comparison: self._should_report_comparison(chemical, comparison), chemical['comparisons'])
            comparison_txt = join(map(_comp, included_comparisons))
            return result_template.substitute({'name':        chemical['name'],
                                               'comparisons': comparison_txt})
        else:
            return self._unreport_chemical(chemical)

    def _results_section(self):

        reports            = map(self._report_chemical, self.chemicals())
        failed_lookups     = map(failed_lookup_template.substitute, self.failed_lookups())
        failed_conversions = map(conversion_failed_template.substitute, self.failed_conversions())

        return result_section_template.substitute({'results': join(reports + failed_lookups + failed_conversions)})

