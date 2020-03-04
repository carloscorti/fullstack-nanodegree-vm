from flask import Flask
app = Flask(__name__)

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/')
@app.route('/restaurant/<int:restaurant_id>/')
def RestoItem(restaurant_id):
    resto = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = resto.id)

    output = ""
    output = "<h1>%s Menu</h1>" % resto.name
    output += '</br>'
    output += '<ol>'
    for i in items:
        output += '<li>'
        output += '<h3>%s</h3>' % i.name
        output += i.price
        output += '</br>'
        output += i.description
        output += '</br></br>'
        output += '</li>'
    output += '</ol>'

    return output

if __name__ == '__main__': 
    app.debug = True
    app.run(host = '0.0.0.0', port= 5000) 
