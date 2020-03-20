from flask import Flask, render_template, url_for       
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

@app.route('/restaurant/<int:restaurant_id>/')
def restoMenuItem(restaurant_id=3):
    resto = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = resto.id)

    return render_template('menulist.html', resto=resto, items=items)


# Task 1: Create route for newMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/new/')
def newMenuItem(restaurant_id):
    resto = session.query(Restaurant).filter_by(id = restaurant_id).one()
    
    return render_template('newmenuitem.html', resto=resto)

# Task 2: Create route for editMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/')
def editMenuItem(restaurant_id, menu_id):
    resto = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem.name).filter_by(restaurant_id = restaurant_id).values(MenuItem.name)
    item_list = list(items)
    item_list_len = len(item_list)

    return render_template('editmenuitem.html', resto=resto, item_list=item_list, menu_id=menu_id, item_list_len=item_list_len)
    

# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/')
def deleteMenuItem(restaurant_id, menu_id):
    resto = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem.name).filter_by(restaurant_id = restaurant_id).values(MenuItem.name)
    item_list = list(items)
    item_list_len = len(item_list)

    return render_template('deletemenuitem.html', resto=resto, item_list=item_list, menu_id=menu_id, item_list_len=item_list_len)


if __name__ == '__main__': 
    app.debug = True
    app.run(host = '0.0.0.0', port= 5000) 
