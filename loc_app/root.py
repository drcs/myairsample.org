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
from options      import TextOptions

from markdown import Markdown
from loc_markdown.superscript import SuperscriptExtension

md=Markdown(extensions=[SuperscriptExtension()])

class Root():
    def __init__(self):
        self.api = API()
        self.about = About()
        self.text_options = TextOptions()

    @cherrypy.expose
    def index(self):
        """Serves the landing page, including entry form"""
        tmpl = loader.load('index.html')
        page = tmpl.generate(all_standards  = all_standards,
                             text_options   = self.text_options.group_names(),
                             unit_keys      = units.units.keys(),
                             unit_represent = lambda key: HTML(md.convert(units.represent(key))))
        return page.render('html', doctype='html')
    
    @cherrypy.expose
    def contact(self):
        """Serves the "contact us" page"""
        tmpl = loader.load('contact.html')
        page = tmpl.generate()
        return page.render('html', doctype='html')

    @cherrypy.expose
    def report(self,
               report_type    = 'pdf',
               text_options   = None,
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
            self.text_options.select_group(text_options)
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
                text_options = self.text_options.selection(),
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
        cas = name2cas(chemical_name)
        if not cas: return "NA"
        has_standards = False
        for standard in all_standards.values():
            has_standards = has_standards or standard.lookup(cas)
        if has_standards:
            return cas
        else:
            return "NS"

class About():
    @cherrypy.expose
    def levels(self):
        """Serves the "About the levels of concern" page"""
        tmpl = loader.load('about-levels.html')
        page = tmpl.generate()
        return page.render('html', doctype='html')

    @cherrypy.expose
    def faq(self):
        """Serves the "About bucket samples and monitoring" page"""
        tmpl = loader.load('about-faq.html')
        page = tmpl.generate()
        return page.render('html', doctype='html')

    @cherrypy.expose
    def tool(self):
        """Serves the "About this tool" page"""
        tmpl = loader.load('about-tool.html')
        page = tmpl.generate()
        return page.render('html', doctype='html')

    @cherrypy.expose
    def implementation(self):
        """Serves the "Technical details" page"""
        tmpl = loader.load('about-implementation.html')
        page = tmpl.generate()
        return page.render('html', doctype='html')


