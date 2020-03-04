from flask import Flask

#creo un objeto Flask con la aplicacion
app = Flask(__name__)

#los decoradores modifican la funcion basica debajo, 
#en este caso .route se apliaca a app e incluye HelloWorlo dentro de app.route
#setean la url del argumento del decorador y luego se ejecuta "def HelloWorld()"
#entonces cada vez que la url es "host port 5000/" o "host port 5000/hello"
#se ejecuta def HelloWorld() y devuelve el string "Hello World" en pantalla
#ademas no hace falta que ejecute la respuesta del servidor al cliente
@app.route('/')
@app.route('/hello')
def HelloWorld():
    return "Hello World"

#si esta aplicacion es invocada por el interperete de python ejecuta app.run
#si es importada como modulo de otra aplicacion no (__name__ != __main__)
if __name__ == '__main__': 
    
    #el servidor se refresca cada vez que hay un cambio de codigo
    #no hace falta reiniciar el servidor cada vez que hago un cambio en el codigo
    #y provee un debugger en el navegador
    app.debug = True
    
    #corre el local server, por default solo es accesible desde host machine
    #host = '0.0.0.0' explicita que puedo escuchar cualquier ip, osea es de acceso publico
    #port = 5000 es el puerto en la maquina host en que se va a
    app.run(host = '0.0.0.0', port= 5000) 
