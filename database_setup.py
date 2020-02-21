"""
con este formato genero el setup para crear la base de datos, generara un archivo "restaurantmenu.db"
"""


import sys #1cpara manipular python run-time environment

from sqlalchemy import Column, ForeignKey, Integer, String #2 para el mapper

from sqlalchemy.ext.declarative import declarative_base #3 para configuracion y class code

from sqlalchemy.orm import relationship #4 para foreing key relations

from sqlalchemy import create_engine #5 para la configuracion al final
##3 y 4 para escribir el mapper

####esto siemore al principio para pasarle a las clases y que el motor sepa que esas clases son clases especiales SQLalchemy que reprecentan tablas
Base = declarative_base()

class Restaurant (Base): #creo la tabla
    __tablename__ = 'restaurant' #nombre de la tabla
    
    name = Column ( #creo una columna de la tabla
        String(80), #type de la entrada
        nullable = False #quiere decir que si no tiene valor no se crea la fila
        )
    
    id = Column (
        Integer,
        primary_key = True # es primary key
        )

    
    
class MenuItem(Base): 
    __tablename__ = 'menu_item'
    
    name = Column (
        String(80),
        nullable = False
        )
    id = Column (
        Integer,
        primary_key = True # es primary key
        )
    
    course = Column (
        String(250),
        )
    
    description = Column (
        String(250),
        )
    
    price = Column (
        String(80),
        )
    
    restaurant_id = Column (
        Integer,
        ForeignKey('restaurant.id') # es foreign key, mirar que es con "." apunta a la columna id de la tabla restaurant para relacionarla con esta
        )
    
    restaurant = relationship(Restaurant) #referencia la relacion entre tablas, depende si es uno a uno, uno a muchos, muchos a uno o muchos a muchos y si es en un sentido o ambos (bidireccional es back_populates)

    
###### esto siempre al final 
engine = create_engine('sqlite:///restaurantmenu.db') #el motor apunta a la base de datos que vamos a usar, usa SQlite3 en este caso, generara el archivo restaurantmenu.db
Base.metadata.create_all (engine) #va a la base de dato y agrega las clases que creamos como nuevas tablas en la base de datos