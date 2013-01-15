"""
LABB report (PDF format), following Gwen's "brief comparison" style
"""

from labb_report import LabbReport, ltx_tr, md

class LabbBrief(LabbReport):

    def _results_section(self, fh):
        print >>fh, r"""
        \newpage
        \section*{Sample Analysis}
"""
        for chemical in self.chemicals():
            # chemical.keys() == 'name','level','level_rep',
            #                    'mw','cas','comparisons'
            print >>fh,r'\subsection*{' + chemical['name'] + r"""}

% Chemical description would go here when implemented

\begin{tabular}{|c|c|p{3in}|}
\hline
The level in your bucket sample &                             & Comparison Level                                       \\
\hline
"""
            for comparison in chemical['comparisons']:
                # comparison.keys=='source','level_rep','level',
                #                  'criterion','description'
                # comparison['criterion']['description']['brief']
                if chemical['level'] > comparison['level']:
                    fc=r' \fc '
                else:
                    fc = ''
                print >>fh, ltx_tr([
                        fc + chemical['level_rep'] + '\ \outunits',
                        fc + md.convert(comparison['description']),
                        fc + md.convert(comparison['criterion']['description']['brief']) + ' ' + comparison['level_rep'] + '\ \outunits'
                        ])
                print >>fh, r'\hline '

            print >>fh, r"""
\hline
\end{tabular}
"""

        for name in self.failed_lookups():
            print >>fh, r'\subsection*{' + name + r"""}
\begin{tabular}{|c|c|p{3in}|}
\hline
The level in your bucket sample &                             & Comparison Level                                       \\
\hline
"""

            print >>fh, ltx_tr([
                    chemical['level_rep'] + '\ \outunits',
                    "",
                    r'Either a comparison level is not available for ' + name + ' or the spelling of the chemical name is incorrect.'
            ])
            print >>fh, r"""
\hline
\end{tabular}
"""

        for name in self.failed_conversions():
            print >>fh, r'\subsection*{' + name + r"""}

Unit conversions failed.  (Try ppb or ug/m3?)
"""


