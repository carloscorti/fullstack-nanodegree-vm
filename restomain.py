from flask import Flask, render_template, url_for, request, redirect, flash, jsonify, abort
 
app = Flask(__name__)


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem


engine = create_engine('sqlite:///restaurantmenu.db', connect_args={'check_same_thread': False})

Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

#error handling
@app.errorhandler(404)
def page_not_found(error):
        return render_template("error.html",error="Ups, page not found :("), 404


#API endpoint
##Restaurant list
@app.route('/all/restaurant/JSON')
def restaurantListJSON():
    if request.method == 'GET':
        restos = session.query(Restaurant).all()
        return jsonify(RestoList=[resto.serialize for resto in restos])
    else:
        return "<h1>Only GET requests</h1>"

##Single restaurant
@app.route('/restaurant/<int:restaurant_id>/JSON')
def singleRestaurantJSON(restaurant_id):
    ids = session.query(Restaurant.id).values(Restaurant.id)
    idList = list(ids)
    if (restaurant_id,) in idList:
        if request.method == 'GET':
            resto = session.query(Restaurant).filter_by(id=restaurant_id).one()
            return jsonify(Resto=resto.serialize)
        else:
            return "<h1>Only GET requests</h1>"
    else:
        return jsonify(Response="no resuslts found, check your uri")

##Menu Items list
@app.route('/all/menuitems/JSON')
def menuItemsListJSON():
    if request.method == 'GET':
        menuItems = session.query(MenuItem).all()
        return jsonify(MenuItemsList=[item.serialize for item in menuItems])
    else:
        return "<h1>Only GET requests</h1>"

##Single Item Menu
@app.route('/menuitems/<int:menu_id>/JSON')
def singleMenuItemsJSON(menu_id):
    ids = session.query(MenuItem.id).values(MenuItem.id)
    idList = list(ids)
    if (menu_id,) in idList:
        if request.method == 'GET':
            menuItems = session.query(MenuItem).filter_by(id=menu_id).one()
            return jsonify(MenuItem=menuItems.serialize)
        else:
            return "<h1>Only GET requests</h1>"
    else:
        return jsonify(Response="no resuslts found, check your uri")

##Restaurant menu list
@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuListJSON(restaurant_id):
    ids = session.query(Restaurant.id).values(Restaurant.id)
    idList = list(ids)
    if (restaurant_id,) in idList:
        if request.method == 'GET':
            resto = session.query(Restaurant).filter_by(id=restaurant_id).one()
            menuItems = session.query(MenuItem).filter_by(restaurant_id = resto.id)

            return jsonify(a_Resto=resto.serialize, b_MenuList=[item.serialize for item in menuItems])
        else:
            return "<h1>Only GET requests</h1>"
    else:
        return jsonify(Response="no resuslts found, check your uri")

##All Restaurants menu list
@app.route('/all/restaurant/menu/JSON')
def allRestaurantMenuListJSON():
    if request.method == 'GET':
        restos = session.query(Restaurant).all()
        menuItems = session.query(MenuItem).all()
        allRestoMenu =  {} 
        for resto in restos:
            key = resto.name.strip().replace("'","").replace(" ","_").lower()
            toAppend = (resto.serialize, [item.serialize for item in menuItems if item.restaurant_id == resto.id ])
            allRestoMenu[key]=toAppend
        return jsonify(allRestoMenu)
    else:
        return "<h1>Only GET requests</h1>"


##web fuctionality

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
def editRestaurant(restaurant_id):
    ids = session.query(Restaurant.id).values(Restaurant.id)
    idList = list(ids)
    if (restaurant_id,) in idList:
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
    else:
        abort(404)

#delete restaurant
@app.route('/restaurant/<int:restaurant_id>/delete/', methods=["POST", "GET"])
def deleteRestaurant(restaurant_id):
    ids = session.query(Restaurant.id).values(Restaurant.id)
    idList = list(ids)
    if (restaurant_id,) in idList:
        resto = session.query(Restaurant).filter_by(id=restaurant_id).one()
        if request.method == 'POST':
            deletedResto = resto.name
            restoToDelete = session.query(Restaurant).filter_by(id=restaurant_id).one()
            session.delete(restoToDelete)
            session.commit()
            menuItemsToDelete = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
            for menuItem in menuItemsToDelete:
                session.delete(menuItem)
                session.commit()
            flash('Restaurant %s was deleted!!' % deletedResto)
            return redirect(url_for('restaurantList'))
        else:
            return render_template('deleteresto.html', resto=resto, restaurant_id=restaurant_id)
    else:
        abort(404)

#show menu regarding restaurant selected
@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def restoMenuList(restaurant_id):
    ids = session.query(Restaurant.id).values(Restaurant.id)
    idList = list(ids)
    if (restaurant_id,) in idList:
        resto = session.query(Restaurant).filter_by(id = restaurant_id).one()
        items = session.query(MenuItem).filter_by(restaurant_id = resto.id)

        return render_template('menulist.html', resto=resto, items=items)
    else:
        abort(404)

#add new menu item for selected restaurant
@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=["POST", "GET"])
def newMenuItem(restaurant_id):
    ids = session.query(Restaurant.id).values(Restaurant.id)
    idList = list(ids)
    if (restaurant_id,) in idList:
        resto = session.query(Restaurant).filter_by(id = restaurant_id).one()

        if request.method == 'POST':
            formData = {k : v if v else "To Be Defined" for k,v in request.form.items()}
            newItemName = formData['newItemName']
            newItemCourse = formData['newItemCourse']
            newItemDescription = formData['newItemDescription']
            newItemPrice = formData['newItemPrice']
            newItem = MenuItem(name=newItemName, course=newItemCourse, description=newItemDescription, price=newItemPrice, restaurant_id=restaurant_id)
            session.add(newItem)
            session.commit()

            flash('New Menu Item %s was created!!' % newItem.name)
            return redirect(url_for('restoMenuList', restaurant_id=restaurant_id))
        else:
            return render_template('newmenuitem.html', resto=resto, restaurant_id=restaurant_id)
    else:
        abort(404)

#edit menu item 
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=["POST", "GET"])
def editMenuItem(restaurant_id, menu_id):
    ids = session.query(Restaurant.id).values(Restaurant.id)
    idList = list(ids)
    if (restaurant_id,) in idList:
        restos = session.query(Restaurant).all()
        resto = session.query(Restaurant).filter_by(id = restaurant_id).one()
        items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
        item_list = list(items)
        item_list_len = len(item_list)
        
        if 0 <= menu_id < item_list_len:
            if request.method == 'POST':
                itemToEdit = session.query(MenuItem).filter_by(id=item_list[menu_id].id).one()
                beforeEditItem = item_list[menu_id].name
                formData = request.form
                if formData["editItemName"]:
                    itemToEdit.name = formData["editItemName"]
                if formData["editItemCourse"]: 
                    itemToEdit.course = formData["editItemCourse"]
                if formData["editItemDescription"]:
                    itemToEdit.description = formData["editItemDescription"]
                if formData["editItemPrice"]:
                    itemToEdit.price = formData["editItemPrice"]
                if formData["editItemRestaurant"] != resto.id:
                    itemToEdit.restaurant_id = formData["editItemRestaurant"]

                session.add(itemToEdit)
                session.commit()

                flash('The Item %s was Edited!!' % beforeEditItem)
                return redirect(url_for('restoMenuList', restaurant_id=restaurant_id))
            else:
                return render_template('editmenuitem.html', database=False, resto=resto, item_list=item_list, menu_id=menu_id, item_list_len=item_list_len, restos=restos)
        else:
            abort(404)
    else:
        abort(404)

#delete menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods=["POST", "GET"])
def deleteMenuItem(restaurant_id, menu_id):
    ids = session.query(Restaurant.id).values(Restaurant.id)
    idList = list(ids)
    if (restaurant_id,) in idList:
        resto = session.query(Restaurant).filter_by(id = restaurant_id).one()
        items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
        item_list = list(items)
        item_list_len = len(item_list)

        if 0 <= menu_id < item_list_len:
            if request.method == 'POST':
                deletedItem = item_list[menu_id].name
                itemToDelete = session.query(MenuItem).filter_by(id=item_list[menu_id].id).one()
                session.delete(itemToDelete)
                session.commit()
                flash('The Item %s was Deleted!!' % deletedItem)
                return redirect(url_for('restoMenuList', restaurant_id=restaurant_id))
            else:
                return render_template('deletemenuitem.html', resto=resto, item_list=item_list, menu_id=menu_id, item_list_len=item_list_len)
        else:
            abort(404)
    else:
        abort(404)

#clean data base
@app.route('/database/', methods=["POST", "GET"])
def cleanDataBase():
    menuItems = session.query(MenuItem).all()
    if request.method == 'POST':
        idsToDelete = request.form.getlist("itemToDelete")
        for idToDelete in idsToDelete:
            itemToDelete = session.query(MenuItem).filter_by(id = idToDelete).one()
            session.delete(itemToDelete)
            session.commit()
        return render_template('database.html', menuItems=session.query(MenuItem).all())
    else:
        return render_template('database.html', menuItems=menuItems)

#edit item from database site
@app.route('/database/editmenuitem/', methods=["POST", "GET"])
def editMenuItemDataBase():
    if request.method == 'POST':
        formData = request.form
        itemToEdit = session.query(MenuItem).filter_by(id=formData["editItemId"]).one()  

        if formData["editItemName"]:
            itemToEdit.name = formData["editItemName"]
        if formData["editItemCourse"]: 
            itemToEdit.course = formData["editItemCourse"]
        if formData["editItemDescription"]:
            itemToEdit.description = formData["editItemDescription"]
        if formData["editItemPrice"]:
            itemToEdit.price = formData["editItemPrice"]
        if formData["editItemRestaurant"] != itemToEdit.restaurant_id:
            itemToEdit.restaurant_id = formData["editItemRestaurant"]

        session.add(itemToEdit)
        session.commit()

        #flash('The Item %s was Edited!!' % beforeEditItem)
        return redirect(url_for('cleanDataBase'))

    else:
        idToEdit = request.args.get("itemToEdit")
        if idToEdit:
            item = session.query(MenuItem).filter_by(id = idToEdit).one()
            restos = session.query(Restaurant).all()
            restoIds = session.query(Restaurant.id).values(Restaurant.id)
            restoIdList = list(restoIds)
            return render_template('edititemfromdatabase.html', item=item, restos=restos, restoIdList=restoIdList)
        else:
            abort(404)

if __name__ == '__main__': 
    app.secret_key = 'secret_key' #flask lo usa para crear sesiones para los usuarios tiene que ser un passwoerd seguro
    app.debug = True
    app.run(host = '0.0.0.0', port= 5000) 
