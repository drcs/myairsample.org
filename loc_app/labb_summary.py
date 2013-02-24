"""
LABB report (PDF format), following Gwen's "brief comparison" style
"""

from labb_brief import LabbBrief

class LabbSummary(LabbBrief):

    def _standards_from_cgi(self, form):
        if form.getvalue('laonly') == 'on':
            return ['lastds']
        elif form.getvalue('nconly') == 'on':
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

    def _unreport_chemical(self, chemical, fh):
        print >>fh,r'\subsection*{' + chemical['name'] + r"""}
Your reported value of """ + chemical['level_rep'] + '\ \outunits\ '
        print >>fh, r'is not above any levels of concern in the myairsample.org system'

