"""
LABB report (PDF format), following Gwen's "brief comparison" style
"""

from labb_brief import LabbBrief

class LabbSummary(LabbBrief):

    def _standards_from_cgi(self, form):
        return None   # In this case 'None' means 'all'.
    
    def _reported_chemicals(self):

        def inc(chemical):
            return any(map(lambda comparison: chemical['level'] > comparison['level'], chemical['comparisons']))
        
        return filter(inc, self.chemicals())
    

