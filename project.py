from flask import Flask, render_template, url_for, request, redirect      
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
@app.route('/restaurant/<int:restaurant_id>/new/', methods=["POST", "GET"])
def newMenuItem(restaurant_id):
    resto = session.query(Restaurant).filter_by(id = restaurant_id).one()

    if request.method == 'POST':
        newItem = MenuItem(name=request.form['newItem'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('restoMenuItem', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', resto=resto, restaurant_id=restaurant_id)


# Task 2: Create route for editMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/', methods=["POST", "GET"])
def editMenuItem(restaurant_id, menu_id):
    resto = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem.name).filter_by(restaurant_id = restaurant_id).values(MenuItem.name)
    item_list = list(items)
    item_list_len = len(item_list)

    if request.method == 'POST':
        if request.form['editItem']:
            itemToEdit = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, name=item_list[menu_id].name).one()
            itemToEdit.name = request.form['editItem']
            session.add(itemToEdit)
            session.commit()
        return redirect(url_for('restoMenuItem', restaurant_id=restaurant_id))
    else:
        return render_template('editmenuitem.html', resto=resto, item_list=item_list, menu_id=menu_id, item_list_len=item_list_len)
    

# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/', methods=["POST", "GET"])
def deleteMenuItem(restaurant_id, menu_id):
    resto = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem.name).filter_by(restaurant_id = restaurant_id).values(MenuItem.name)
    item_list = list(items)
    item_list_len = len(item_list)

    if request.method == 'POST':
        deleteItem = item_list[menu_id].name
        itemToDelete = session.query(MenuItem).filter_by(name = deleteItem).one()
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('restoMenuItem', restaurant_id=restaurant_id))
    else:
        return render_template('deletemenuitem.html', resto=resto, item_list=item_list, menu_id=menu_id, item_list_len=item_list_len)


if __name__ == '__main__': 
    app.debug = True
    app.run(host = '0.0.0.0', port= 5000) 
