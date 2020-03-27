from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
app = Flask(__name__)


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem


engine = create_engine('sqlite:///restaurantmenu.db', connect_args={'check_same_thread': False})

Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

#show restaurant list
@app.route('/')
@app.route('/restaurant/')
def restaurantList():
    resto = session.query(Restaurant).all()
    return render_template('restolist.html', resto=resto)

#create new restaurant
@app.route('/restaurant/new/', methods=["POST", "GET"])
def createRestaurant():
    resto = session.query(Restaurant).all()
    if request.method == 'POST':
        if request.form['newResto']:
            newResto = Restaurant(name=request.form['newResto'])
            session.add(newResto)
            session.commit()
            flash('New restaurant called %s was created!!' % newResto.name)
            return redirect(url_for('restaurantList'))
        else:
            flash("Please enter the new restaurant's name")
            return render_template('createresto.html', resto=resto)
    else:
        return render_template('createresto.html', resto=resto)

#edit restaurant
@app.route('/restaurant/<int:restaurant_id>/edit/', methods=["POST", "GET"])
#verificar que restaurant_id este dentro de la lista de restos
def editRestaurant(restaurant_id):
    resto = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['newName']:
            oldName = resto.name
            resto.name = request.form['newName']
            session.add(resto)
            session.commit()
            flash('The restaurant %s was edited to %s!!' % (oldName, resto.name))
            return redirect(url_for('restaurantList'))
        else:
            flash("Please enter the new name for %s restaurant" % resto.name)
            return render_template('editresto.html', resto=resto, restaurant_id=restaurant_id)

    else:
        return render_template('editresto.html', resto=resto, restaurant_id=restaurant_id)

#delete restauratn
@app.route('/restaurant/<int:restaurant_id>/delete/', methods=["POST", "GET"])
#verificar que restaurant_id este dentro de la lsta de restos
def deleteRestaurant(restaurant_id):
    resto = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        deleteItem = resto.name
        itemToDelete = session.query(Restaurant).filter_by(id=restaurant_id).one()
        session.delete(itemToDelete)
        session.commit()
        flash('The restaurant %s was deleted!!' % deleteItem)
        return redirect(url_for('restaurantList'))
    else:
        return render_template('deleteresto.html', resto=resto, restaurant_id=restaurant_id)

#show menu for selected restaurant
@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def restoMenuList(restaurant_id):
    resto = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = resto.id)

    return render_template('menulist.html', resto=resto, items=items)

#add new menu item for selected restaurant
@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=["POST", "GET"])
def newMenuItem(restaurant_id):
    resto = session.query(Restaurant).filter_by(id = restaurant_id).one()

    if request.method == 'POST':
        newItem = request.form['newItem']
        return "<h1>Created menu item %s for %s with POST requests</h1>" % (newItem, resto.name)
        #newItem = MenuItem(name=request.form['newItem'], restaurant_id=restaurant_id)
        #session.add(newItem)
        #session.commit()
        #flash('New Menu Item %s was created!!' % newItem.name)
        #return redirect(url_for('restoMenuItem', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', resto=resto, restaurant_id=restaurant_id)

#edit menu item 
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=["POST", "GET"])
def editMenuItem(restaurant_id, menu_id):
    resto = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)#.values(MenuItem.name)
    #items_id = session.query(MenuItem.id).filter_by(restaurant_id = restaurant_id).values(MenuItem.id)
    item_list = list(items)
    #item_id_list = list(items_id)
    item_list_len = len(item_list)

    if request.method == 'POST':
        editItemName = request.form['editItemName']
        return "<h1>Edited menu item %s to %s from %s with POST requests</h1>" % (item_list[menu_id].name, editItemName, resto.name)
        #if request.form['editItem']:
            #itemToEdit = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, name=item_list[menu_id].name, id=item_id_list[menu_id].id).one()
            #itemToEdit.name = request.form['editItem']
            #session.add(itemToEdit)
            #session.commit()
            #flash('The Item %s was Edited to %s!!' % (item_list[menu_id].name, itemToEdit.name))
        #return redirect(url_for('restoMenuItem', restaurant_id=restaurant_id))
    else:
        return render_template('editmenuitem.html', resto=resto, item_list=item_list, menu_id=menu_id, item_list_len=item_list_len)

# delete menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods=["POST", "GET"])
def deleteMenuItem(restaurant_id, menu_id):
    resto = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)#.values(MenuItem.name)
    #items_id = session.query(MenuItem.id).filter_by(restaurant_id = restaurant_id).values(MenuItem.id)
    item_list = list(items)
    #item_id_list = list(items_id)
    item_list_len = len(item_list)

    if request.method == 'POST':
        return "<h1>Deleted menu item %s from %s with POST requests</h1>" % (item_list[menu_id].name, resto.name)
        #deleteItem = item_list[menu_id].name
        #itemToDelete = session.query(MenuItem).filter_by(name = deleteItem, id=item_id_list[menu_id].id).one()
        #session.delete(itemToDelete)
        #session.commit()
        #flash('The Item %s was Deleted!!' % deleteItem)
        #return redirect(url_for('restoMenuItem', restaurant_id=restaurant_id))
    else:
        return render_template('deletemenuitem.html', resto=resto, item_list=item_list, menu_id=menu_id, item_list_len=item_list_len)


if __name__ == '__main__': 
    app.secret_key = 'secret_key' #flask lo usa para crear sesiones para los usuarios tiene que ser un passwoerd seguro
    app.debug = True
    app.run(host = '0.0.0.0', port= 5000) 
