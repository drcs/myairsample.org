import os
current_dir = os.path.dirname(os.path.abspath(__file__))

import cherrypy
import units
from genshi.template import TemplateLoader
from genshi import HTML
loader = TemplateLoader(os.path.join(current_dir, 'templates'), auto_reload=True)

from labb_full    import LabbFull
from labb_brief   import LabbBrief
from labb_summary import LabbSummary

from standard     import all_standards
from synonyms     import name2cas

from markdown import Markdown
from loc_markdown.superscript import SuperscriptExtension

md=Markdown(extensions=[SuperscriptExtension()])

class Root():
    def __init__(self):
        self.api = API()

    @cherrypy.expose
    def index(self):
        """Serves the landing page, including entry form"""
        tmpl = loader.load('index.html')
        page = tmpl.generate(all_standards  = all_standards,
                             unit_keys      = units.units.keys(),
                             unit_represent = lambda key: HTML(md.convert(units.represent(key))))
        return page.render('html', doctype='html')

    @cherrypy.expose
    def report(self,
               report_type    = 'pdf',
               inunits        = 'ppb',
               outunits       = 'ppb',
               username       = '',
               username2      = '',
               samplename     = '',
               sampledate     = '',
               samplelocation = '',
               **kwargs):
        """Handles "submit" actions from the main entry form"""
        if (report_type == 'html'):
            return "HTML report... coming soon!"
        else:
            report_class = LabbSummary
            report_map = {'single': LabbBrief,
                          'above':  LabbSummary,
                          'all':    LabbFull}
            if 'standards_source' in kwargs and kwargs['standards_source'] in report_map:
                report_class=report_map[kwargs['standards_source']]
            report=report_class(
                units  = {'in'  : inunits,
                          'out' : outunits},
                sample = {'name'    : samplename,
                          'date'    : sampledate,
                          'location': samplelocation },
                user   = {'first'   : username,
                          'second'  : username2 },
                form   = kwargs)
            (content_fname, headers) = report.reply()
            try:
                content=open(content_fname, 'r').read()
                for key,value in headers.items():
                    cherrypy.response.headers[key]=value
                return content
            except (IOError, TypeError):
                cherrypy.response.headers['Content-Type']='text/plain'
                return "Something went wrong generating content.  That's all I know."

class API():
    @cherrypy.expose
    def index(self):
        cherrypy.response.headers['Content-Type']='text/plain'
        return "Which function do you want to call?"

    @cherrypy.expose
    def validate(self, chemical_name):
        cherrypy.response.headers['Content-Type']='text/plain'
        return name2cas(chemical_name) or "NA"
