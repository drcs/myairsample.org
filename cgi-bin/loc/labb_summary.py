"""
LABB report (PDF format), following Gwen's "brief comparison" style
"""

from labb_report import LabbReport, ltx_tr, md

class LabbSummary(LabbReport):
    
    def _results_section(self, fh):
        print >>fh, r"""
\newpage
\section*{Sample Analysis}
"""
        for chemical in self.chemicals():
            if any(map(lambda comparison: chemical['level'] > comparison['level'], chemical['comparisons'])):
                print >>fh, r'\subsection*{' + chemical['name'] + r'} '
                print >>fh, "Your reported level of " + chemical['level_rep'] + '\ \outunits' \
                            + r"\ is ABOVE the following levels of concern:"
                print >>fh, r"""

\begin{tabular}{|p{4in}|l|}
\hline
"""
                for comparison in chemical['comparisons']:
                    if chemical['level'] > comparison['level']:
                        print >>fh, ltx_tr([
                                r'{\large ' + md.convert(comparison['criterion']['description']['brief']) + r'} \newline ' \
                                    + md.convert(comparison['criterion']['description']['long']),
                                md.convert(comparison['level_rep'] + r'\ \outunits')
                                ])
                        print >>fh, r"\hline "
                print >>fh, r"""
\end{tabular}

"""

