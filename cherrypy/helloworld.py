import cherrypy

class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        return "3"

if __name__ == '__main__':
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.quickstart(HelloWorld())


