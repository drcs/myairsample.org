"""
LABB report (PDF format), following Gwen's "brief comparison" style
"""

from labb_brief import LabbBrief, LatexTemplate

not_above_template = LatexTemplate(r"""
\subsection*{\subst{name}}
Your reported value of \subst{level} \outunits\ %
is not above any levels of concern in the myairsample.org system
""")

class LabbSummary(LabbBrief):

    def _standards_from_form_data(self, form):
        if 'laonly' in form and form['laonly'] == 'on':
            return ['lastds']
        elif 'nconly' in form and form['nconly'] == 'on':
            return ['ncstds']
        else:
            return None   # In this case 'None' means 'all'.
    
    def _should_report_chemical(self, chemical):
        return any(map(lambda comparison: chemical['level'] > comparison['level'], chemical['comparisons']))

    def _should_report_comparison(self, chemical, comparison):
        if (chemical['level'] > comparison['level']):
            return True
        else:
            return False

    def _unreport_chemical(self, chemical):
        return not_above_template.substitute({'name': chemical['name'], 'level': chemical['level_rep']})


