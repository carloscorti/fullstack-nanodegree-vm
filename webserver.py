from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

#main, instancia el servidor y especifica que puerto va a escuchar

#handler, que codigo va a ejecutar dependiendo del HTTP reuqest enviado al servidor

class webserverHanlder (BaseHTTPRequestHandler):
    def do_GET(self):

        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()

                output=""
                output+="<html><body>"
                output+="<h1>Hello!</h1>"
                output+= """
                    <form method='POST' enctype='multipart/form-data' action='/hello'
                        <h2>What would you like me to say?</h2>
                        <input name='message' type='text'>
                        <input type='submit' value='submit'>
                    </form>
                        """
                output+="</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                output=""
                output+="<html><body>"
                output+="""    
                            <h1>&#161Hola!</h1>
                            <a href='/hello'>Back to Hello</a>   
                        """
                output+= """
                    <form method='POST' enctype='multipart/form-data' action='/hello'
                        <h2>What would you like me to say?</h2>
                        <input name='message' type='text'>
                        <input type='submit' value='submit'>
                    </form>
                        """
                output+="</html></body>"

                self.wfile.write(output)
                print output
                return
            
            
        except IOError:
            self.send_error(404, "File not Fount %s" % self.path)
    
    def do_POST(self):
        try:
            self.send_response(301)
            self.end_headers()

            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')

            output=""
            output+="<html><body>"
            output+= "<h2>Ok how about this</h2>"
            output+= "<h1>%s</h1>" % messagecontent[0]

            output+= """
                        <form method='POST' enctype='multipart/form-data' action='/hello'
                            <h2>What would you like me to say <strong>now</strong>?</h2>
                            <input name='message' type='text'>
                            <input type='submit' value='submit'>
                        </form>
                            """
            output+="</html></body>"

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