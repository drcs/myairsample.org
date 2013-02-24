import os.path
current_dir = os.path.dirname(os.path.abspath(__file__))

import cherrypy
from genshi.template import TemplateLoader
loader = TemplateLoader(os.path.join(current_dir, 'templates'), auto_reload=True)

class Root():
    def index(self):
        tmpl = loader.load('index.html')
        page = tmpl.generate()
        return page.render('html', doctype='html')
    index.exposed = True

