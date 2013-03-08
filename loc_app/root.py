import os
current_dir = os.path.dirname(os.path.abspath(__file__))

import cherrypy
from genshi.template import TemplateLoader
loader = TemplateLoader(os.path.join(current_dir, 'templates'), auto_reload=True)

from labb_full    import LabbFull
from labb_brief   import LabbBrief
from labb_summary import LabbSummary

from standard     import all_standards

class Root():
    def index(self):
        """Serves the landing page, including entry form"""
        tmpl = loader.load('index.html')
        page = tmpl.generate(all_standards=all_standards)
        return page.render('html', doctype='html')
    index.exposed = True

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
                sample = {'name': samplename,
                          'date': sampledate,
                          'location': samplelocation },
                user   = {'first':  username,
                          'second': username2 },
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

    report.exposed = True


