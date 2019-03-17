import cherrypy

class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        with open ('/home/pi/cherrypy/va.txt', 'r') as myfile:
            value = myfile.read().replace('\n', '')
        #refresh = '<meta http-equiv="refresh" content="10">'
        print(value)
        return value

if __name__ == '__main__':
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.quickstart(HelloWorld())


