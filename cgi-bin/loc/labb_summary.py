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
    
    def _reported_chemicals(self):

        def inc(chemical):
            return any(map(lambda comparison: chemical['level'] > comparison['level'], chemical['comparisons']))
        
        return filter(inc, self.chemicals())

    def _should_report_comparison(self, chemical, comparison):
        if (chemical['level'] > comparison['level']):
            return True
        else:
            return False

