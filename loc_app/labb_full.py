"""
LABB report (PDF format), following Gwen's "brief comparison" style
"""

from labb_summary import LabbSummary

class LabbFull(LabbSummary):
    
    def _should_report_chemical(self, chemical):
        return True

    def _should_report_comparison(self, chemical, comparison):
        return True

    def _unreport_chemical(self, chemical):
        pass

