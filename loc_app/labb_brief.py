"""
LABB report (PDF format), following Gwen's "brief comparison" style
"""

from labb_report import LabbReport, LatexTemplate, ltx_tr, md
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

class LabbBrief(LabbReport):

    def _standards_from_form_data(self, form):
        # return [ 'ncstds' ]
        requested = form.getvalue('reflevel')
        return [ requested ]

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

    def _results_section(self):
        def _report_chemical(chemical):
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

        result = join(map(_report_chemical, self.chemicals()))

        for chemical in self.failed_lookups():
            result += r'\subsection*{' + chemical['name'] + r"""}
\begin{tabular}{|c|c|p{3in}|}
\hline
The level in your bucket sample &                             & Comparison Level                                       \\
\hline
"""

            result += ltx_tr([
                    chemical['level'] + '\ \inunits',
                    "",
                    r'Either a comparison level is not available for ' + chemical['name'] + ' or the spelling of the chemical name is incorrect.'
            ])
            result += r"""
\hline
\end{tabular}
"""

        for name in self.failed_conversions():
            result += r'\subsection*{' + name + r"""}

Unit conversions failed.  (Try ppb or ug/m3?)
"""

        return result_section_template.substitute({'results': result})
