from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

#main, instancia el servidor y especifica que puerto va a escuchar

#handler, que codigo va a ejecutar dependiendo del HTTP reuqest enviado al servidor

class webserverHanlder (BaseHTTPRequestHandler):
    def do_GET(self):

        try:
            engine = create_engine('sqlite:///restaurantmenu.db')
            Base.metadata.bind = engine
            DBSession = sessionmaker(bind = engine)
            ses = DBSession()

            restoList = ses.query(Restaurant).all()

            if self.path.endswith("/restaurant"):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()

                output=""
                output+="<html><body>"
                output+="<h1>Restaurant list</h1>"
                output+="<a href='/restaurants/new'>Create a new Restaurant</a>"
                output+="<div><ul>"

                output+="<li>%s</li>" % ses.query(Restaurant).count()

                for resto in restoList:
                    output+="<li>%s</li>" % resto.name
                    output+="<a href=#>Edit Restaurant</a>"
                    output+="<br>"
                    output+="<a href=#>Delete Restaurant</a>"
                    output+="<br><br>"

                output+="</ul></div>"
                output+="</body></html>"
                self.wfile.write(output)
                print output
                return 


            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()

                output=""
                output+="<html><body>"
                output+="<h1>Create new Restaurants!!</h1>"
                output+= """
                    <form method='POST' enctype='multipart/form-data' action='/restaurants/new'>
                        <label for="name">Restaurant Name</label>
                        <input type="text" id="name" name="name">
                        <button type='submit'>Upload</button>
                    </form> 
                    """
                output+="<a href='/restaurant'>Return to Restaurants List</a>"                        
                output+="</body></html>"
                self.wfile.write(output)
                print output
                return     

        except IOError:
            self.send_error(404, "File not Fount %s" % self.path)
            server.socket.close()
    
    def do_POST(self):
        try:
            self.send_response(301)
            self.end_headers()


            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                restoName = fields.get('name')
            
            engine = create_engine('sqlite:///restaurantmenu.db')
            Base.metadata.bind = engine
            DBSession = sessionmaker(bind = engine)
            ses = DBSession()

            newResto = Restaurant(name = restoName[0])
            ses.add(newResto)
            ses.commit()

            output=""
            output+="<html><body>"
            output+="<h1>Geat!!!!</h1>"
            output+="<h2>%s was uploaded succesfully!!</h2>" % restoName[0]
            output+="<a href='/restaurants/new'>Create a new Restaurant</a><br>"
            output+="<a href='/restaurant'>Return to Restaurants List</a>"
            output+="</body></html>"

            self.wfile.write(output)
            print output

        except:
            pass



def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHanlder)
        print "Web server running on port %s" % port
        server.serve_forever()


        
    except KeyboardInterrupt: #se lanza cuand el usuario mantiene Ctrl+C
        print "Ctrl+C entered, stopping web server..."
        server.socket.close()
    
    
#al final para ejecutar inmediatamente main cuando el python interpreter ejecute el script
if __name__ == '__main__':
    main()