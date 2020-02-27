from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import re

#main, instancia el servidor y especifica que puerto va a escuchar

#handler, que codigo va a ejecutar dependiendo del HTTP reuqest enviado al servidor

class webserverHanlder (BaseHTTPRequestHandler):      
    
    engine = create_engine('sqlite:///restaurantmenu.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind = engine)
    ses = DBSession()

    #services
    #return path chunk selected as a string, if complete True return a list of splited path
    def pathChunk (self, num, complete=False, splitChar="/"):
        splitPath = self.path.split(splitChar)
        if complete:
            return splitPath
        else:
            return splitPath[num]

    #checks path len
    def checkPathLen (self, num,  splitChar="/"):
        if len(self.path.split(splitChar))==num:
            return True
        else:
            return False

    #check id in path to be in tableClass
    def checkIdChunk (self, chunkPosition, tableClass=Restaurant):
        idToCheck = self.pathChunk(chunkPosition)
        pattern= re.compile('^\d*$')
        if pattern.match(idToCheck):
            restoIdList = self.ses.query(tableClass.id).all()
            maxId = max(restoIdList)
            if int(idToCheck) <= maxId[0] and int(idToCheck) > 0 and ((int(idToCheck),) in restoIdList):
                return True
            else:
                return False
        else:
            return False
    
    
    def do_GET(self):

        try:

            #restaurant list
            if self.path.endswith("/restaurant") and self.checkPathLen(2):
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
                    output+="<a href='%s/delete'>Delete Restaurant</a>" % resto.id
                    output+="<br><br>"

                output+="</ul></div>"
                output+="</body></html>"
                self.wfile.write(output)
                print output

                return 

            #new reaturant entry
            if self.path.endswith("/restaurants/new") and self.checkPathLen(3):
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
            if self.checkPathLen(4) and self.checkIdChunk(2) and self.pathChunk(1)== ("restaurant") and self.path.endswith("/edit"):

                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()

                toModify = self.ses.query(Restaurant).filter_by(id= (int(self.pathChunk(2))) ).one()
 
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


            #delete restaurant
            if self.checkPathLen(3) and self.path.endswith("/delete") and self.checkIdChunk(1):

                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()

                toDelete = self.ses.query(Restaurant).filter_by(id= ( int(self.pathChunk(1)) ) ).one()
 
                output=""
                output+="<html><body>"
                output+="<h1>Delete Restaurant</h1>"
                output+="<h2>Are you sure you want to delete %s??</h2>" % toDelete.name
                output+="<div><form method='POST' enctype='multipart/form-data' action='/%s/delete'>" % toDelete.id
                output+="""
                        <button type='submit'>Delete</button>
                        """
                output+="</form></div>"
                output+="<a href='/restaurant'>Return to Restaurants List</a>"                        
                output+="</body></html>"
                self.wfile.write(output)
                print output
                return 
            
            raise IOError        

        except IOError:
            self.send_error(404, "File not Fount %s" % self.path)
            print("there was an error :(")

    
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
                return

            #UPDATE edit restaurant name
            if self.checkPathLen(4) and self.checkIdChunk(2) and self.pathChunk(1)== ("restaurant") and self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    oldRestoId = int(self.pathChunk(2))
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
                return

            #DELETE delete restaurant from restaurantmenu.db
            if self.checkPathLen(3) and self.path.endswith("/delete") and self.checkIdChunk(1):

                deleteRestoId = int(self.path.split("/")[1])

                deleteResto = self.ses.query(Restaurant).filter_by(id= deleteRestoId ).one()
                deleteRestoName = deleteResto.name
                self.ses.delete(deleteResto)
                self.ses.commit()

                output=""
                output+="<html><body>"
                output+="<h1>Done</h1>"
                output+="<h2>%s was deleted form database!!</h2>" % deleteRestoName
                output+="<a href='/restaurants/new'>Create a new Restaurant</a><br>"
                output+="<a href='/restaurant'>Return to Restaurants List</a><br>"
                output+="<a href='/restaurant/id/edit'>Edit Restaurant</a>"
                output+="</body></html>"

                self.wfile.write(output)
                print output
                return

            raise IOError        


        except IOError:
            self.send_error(404, "File not Fount %s" % self.path)
            print("there was an error :(")



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