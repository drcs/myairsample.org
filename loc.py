from flup.server.fcgi import WSGIServer
import cherrypy
from loc_app.root import Root

cherrypy.config.update({'server.socket_file': '/tmp/levels-of-concern-ottinger.sock'})

app = cherrypy.tree.mount(Root(), "/loc.fcgi/")
cherrypy.engine.start()
try:
    WSGIServer(app).run()
finally:
    cherrypy.engine.stop()
    
