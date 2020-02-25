from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

#main, instancia el servidor y especifica que puerto va a escuchar

#handler, que codigo va a ejecutar dependiendo del HTTP reuqest enviado al servidor

class webserverHanlder (BaseHTTPRequestHandler):      
    
    engine = create_engine('sqlite:///restaurantmenu.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind = engine)
    ses = DBSession()
 
    def do_GET(self):

        try:

            #restoList = self.ses.query(Restaurant.name).all()

            #restaurant list
            if self.path.endswith("/restaurant"):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                
                restoList = self.ses.query(Restaurant).all()

                output=""
                output+="<html><body>"
                output+="<h1>Restaurant list</h1>"
                output+="<a href='/restaurants/new'>Create a new Restaurant</a>"
                output+="<div><ul>"

                for resto in restoList:
                    output+="<li>%s</li>" % resto.name
                    output+="<a href='restaurant/%s/edit'>Edit Restaurant</a>" % resto.id
                    output+="<br>"
                    output+="<a href=#>Delete Restaurant</a>"
                    output+="<br><br>"

                output+="</ul></div>"
                output+="</body></html>"
                self.wfile.write(output)
                print output
                return 

            #new reaturant entry
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()

                output=""
                output+="<html><body>"
                output+="<h1>Create new Restaurants!!</h1>"
                output+= """
                    <div>
                    <form method='POST' enctype='multipart/form-data' action='/restaurants/new'>
                        <label for="name">Restaurant Name</label>
                        <input type="text" id="name" name="name">
                        <button type='submit'>Upload</button>
                    </form>
                    </div> 
                    """
                output+="<a href='/restaurant'>Return to Restaurants List</a>"                        
                output+="</body></html>"
                self.wfile.write(output)
                print output
                return


            #modify restaurant
            if len(self.path.split("/")) == 4 and self.path.split("/")[1] == ("restaurant") and self.path.endswith("/edit") and ( int(self.path.split("/")[2]) <= self.ses.query(Restaurant).count() ) and ( int(self.path.split("/")[2]) > 0 ):
                
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()

                toModify = self.ses.query(Restaurant).filter_by(id= ( int(self.path.split("/")[2]) ) ).one()
 
                output=""
                output+="<html><body>"
                output+="<h1>Edit Restaurant</h1>"
                output+="<h2>%s</h2>" % toModify.name
                output+="<div><form method='POST' enctype='multipart/form-data' action='/restaurant/%s/edit'>" % toModify.id
                output+="""
                        <label for="rename-restaurant">New Name</label>
                        <input type="text" id="rename-restaurant" name="reName">
                        <button type='submit'>Upload</button>
                        """
                output+="</form></div>"
                output+="<a href='/restaurant'>Return to Restaurants List</a>"                        
                output+="</body></html>"
                self.wfile.write(output)
                print output
                return            

        except IOError:
            self.send_error(404, "File not Fount %s" % self.path)
    
    def do_POST(self):
        try:
            self.send_response(301)
            self.end_headers()

            #CREATE new restaurabd post
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    restoName = fields.get('name')

                newResto = Restaurant(name = restoName[0])
                self.ses.add(newResto)
                self.ses.commit()

                output=""
                output+="<html><body>"
                output+="<h1>Geat!!!!</h1>"
                output+="<h2>%s was uploaded succesfully!!</h2>" % restoName[0]
                output+="<a href='/restaurants/new'>Create a new Restaurant</a><br>"
                output+="<a href='/restaurant'>Return to Restaurants List</a>"
                output+="</body></html>"

                self.wfile.write(output)
                print output

            #UPDATE edit restaurant name
            if len(self.path.split("/")) == 4 and self.path.split("/")[1] == ("restaurant") and self.path.endswith("/edit") and ( int(self.path.split("/")[2]) <= self.ses.query(Restaurant).count() ) and ( int(self.path.split("/")[2]) > 0 ):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    oldRestoId = int(self.path.split("/")[2])
                    newName = fields.get('reName')

                modifyResto = self.ses.query(Restaurant).filter_by(id= oldRestoId ).one()
                oldRestoName = modifyResto.name
                modifyResto.name = newName[0]
                self.ses.add(modifyResto)
                self.ses.commit()

                checkChange = self.ses.query(Restaurant).filter_by(name=newName[0]).one()

                output=""
                output+="<html><body>"
                output+="<h1>Awesome!!!!</h1>"
                output+="<h2>%s was renamed to %s!!</h2>" % (oldRestoName, checkChange.name)
                output+="<a href='/restaurants/new'>Create a new Restaurant</a><br>"
                output+="<a href='/restaurant'>Return to Restaurants List</a><br>"
                output+="<a href='/restaurant/id/edit'>Edit Restaurant</a>"
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