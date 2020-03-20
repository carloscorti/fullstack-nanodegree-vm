from flask import Flask, render_template         
app = Flask(__name__)

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
#from webserver import pathChunk

#By default, check_same_thread is True and only the creating thread may use the connection.
# If set False, the returned connection may be shared across multiple threads. 
# When using multiple threads with the same connection writing operations should be serialized by the user to avoid data corruption

engine = create_engine('sqlite:///restaurantmenu.db', connect_args={'check_same_thread': False})



Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/')
@app.route('/restaurant/<int:restaurant_id>/')
def RestoItem(restaurant_id=3):
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

# Task 1: Create route for newMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/new/')
def newMenuItem(restaurant_id):
    resto = session.query(Restaurant).filter_by(id = restaurant_id).one()
    output = "<h1>%s | Add Menu Item</h1>" % resto.name
    return "page to create a new menu item. Task 1 complete!</br></br>" + output

# Task 2: Create route for editMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/')
def editMenuItem(restaurant_id, menu_id):
    resto = session.query(Restaurant.name).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem.name).filter_by(restaurant_id = restaurant_id).values(MenuItem.name)
    item_list = list(items)
    output = "<h1>%s | Total Menu Items %s <br> Edit Menu Item %s</h1>" % (resto.name, len(item_list), item_list[menu_id].name)
    return "page to edit a menu item. Task 2 complete!" + output

# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/')
def deleteMenuItem(restaurant_id, menu_id):
    resto = session.query(Restaurant.name).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem.name).filter_by(restaurant_id = restaurant_id).values(MenuItem.name)
    item_list = list(items)
    output = "<h1>%s | Total Menu Items %s <br> Delete Menu Item %s</h1>" % (resto.name, len(item_list), item_list[menu_id].name)
    return "page to delete a menu item. Task 3 complete!" + output

if __name__ == '__main__': 
    app.debug = True
    app.run(host = '0.0.0.0', port= 5000) 
