
from loc.report import LocReport
from markdown import Markdown
from sys import stdout

from genshi.template import TemplateLoader
from genshi import HTML

# -------------------------------------------------------------------------------
# Load the report template and generate the output
# -------------------------------------------------------------------------------
loader = TemplateLoader('.')
tmpl = loader.load('report-templates/medium.html')

md_converter=Markdown()

def md(str):
    return HTML(md_converter.convert(str))

class MediumReport(LocReport):
    
    def generate(self, fh=stdout):
        document = tmpl.generate(chemicals         = self.chemicals(),
                                 user              = self.users(),
                                 failures          = {'name_lookups':     self.failed_lookups(),
                                                      'unit_conversions': self.failed_conversions()},
                                 units             = self.units(),
                                 md                = md)

        print >>fh,document.render('html', doctype='html')
        fh.flush()
