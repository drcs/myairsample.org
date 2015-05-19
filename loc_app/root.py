import os
current_dir = os.path.dirname(os.path.abspath(__file__))

import subprocess
import re
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
        self.status = Status()
        self.text_options = TextOptions()

    @cherrypy.expose
    def index(self):
        """Serves the landing page, including entry form"""
        tmpl = loader.load('index.html')
        page = tmpl.generate(all_standards  = all_standards,
                             text_options   = self.text_options.group_names(),
                             unit_keys      = units.unit_keys(),
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
            try:
                (content_fname, headers) = report.reply()
                content=open(content_fname, 'r').read()
                for key,value in headers.items():
                    cherrypy.response.headers[key]=value
                return content
            except (IOError, TypeError):
                cherrypy.response.headers['Content-Type']='text/plain'
                return "Oops, internal error generating content.  Please try re-loading this page in a few minutes, or starting with a new report."

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

MIN_EXPECTED_PDF_SIZE = 100000

class Status():
 
    @cherrypy.expose
    def available(self):
        return "STATUS_OK"

    @cherrypy.expose
    def selfcheck(self):
        report = LabbFull(
            units  = { 'in' : 'ppb', 'out' : 'ppb'},
            sample = { 'name' : 'test sample', 'date' : '2014-01-01' },
            user   = { 'first' : 'self-check', 'second' : 'von self-checker' },
            form   = { 'chem1' : 'nitrous oxide', 'report1' : '666', 'chem2' : 'propane', 'report2' : '55' }
        )
        (content_fname, headers) = report.reply()
        pdfinfo = subprocess.check_output(["pdfinfo", content_fname])
        file_size = int(re.search('File size[^0-9]*(\d+)', pdfinfo).group(1))
        if (file_size > MIN_EXPECTED_PDF_SIZE):
            result = 'STATUS_OK'
        else:
            result = "ERROR: expected min PDF size {0} got {1}".format(MIN_EXPECTED_PDF_SIZE, file_size)
        os.remove(content_fname)
        return result

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


