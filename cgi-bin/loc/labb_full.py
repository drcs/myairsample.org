"""
LABB report (PDF format), following Gwen's "brief comparison" style
"""

from labb_summary import LabbSummary

class LabbFull(LabbSummary):
    
    def _reported_chemicals(self):
        return self.chemicals()

    def _should_report_comparison(self, chemical, comparison):
        return True

