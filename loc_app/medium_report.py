
from loc.report import LocReport
from sys import stdout
from tempfile import NamedTemporaryFile
from markdown import Markdown
from markdown.superscript import SuperscriptExtension

from genshi.template import TemplateLoader
from genshi import HTML

# -------------------------------------------------------------------------------
# Load the report template and generate the output
# -------------------------------------------------------------------------------
loader = TemplateLoader('.')
tmpl = loader.load('report-templates/medium.html')

md=Markdown(extensions=[SuperscriptExtension()])

class MediumReport(LocReport):
    
    def _markdown_convert(self, string):
        return HTML(md.convert(string))

    def generate(self, fh=None):
        if fh is None:
            fh = NamedTemporaryFile(delete=False)
        document = tmpl.generate(chemicals         = self.chemicals(),
                                 user              = self.users(),
                                 failures          = {'name_lookups':     self.failed_lookups(),
                                                      'unit_conversions': self.failed_conversions()},
                                 units_in          = self.units('in'),
                                 units_out         = self.units('out'),
                                 units_out_rep     = HTML(self.units('out_rep')),
                                 units_in_rep      = HTML(self.units('in_rep')),
                                 md                = md)

        print >>fh,document.render('html', doctype='html')
        fh.close()
        return fh.name

    def http_headers(self):
        return {"Content-type:", "text/html; charset=utf-8"}

