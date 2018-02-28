from flask import Flask, render_template, request
from flask import redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Item, Category
from flask import session as login_session
import random, string

app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create a state-token to prevent request forgery
#Store it in the session for later use
@app.route('/catalog/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return "The current session state is %s" % login_session['state']

# JSON endpoint for category items
@app.route('/catalog/<int:category_id>/JSON')
def categoryJSON(category_id):
    category = session.query(Category).filter_by(id = category_id).one()
    items = session.query(Item).filter_by(category_id = category_id)
    return jsonify(items=[i.serialize for i in items])

@app.route('/catalog/<int:category_id>/<int:item_id>/JSON')
def itemJSON(category_id, item_id):
    item = session.query(Item).filter_by(id = item_id).one()
    return jsonify(item.serialize)



# TODO Write function that serves the home page with all categories and new/sale items
# add timestamp field to Item table filter for the newest 9 items
# add sale/discount field to Item table for featured sale items in showCatalog()

@app.route('/')
@app.route('/catalog/')
def showCatalog():
    categories = session.query(Category).all()
    items = session.query(Item).all()
    return render_template('home.html', categories=categories)

# Write function that renders each category
@app.route('/catalog/<int:category_id>/')
def showCategory(category_id):
    category = session.query(Category).filter_by(id = category_id).one()
    items = session.query(Item).filter_by(category_id = category_id)
    return render_template('category.html', category=category, items=items)

@app.route('/catalog/<int:category_id>/<int:item_id>/')
def showItem(category_id, item_id):
    item = session.query(Item).filter_by(id = item_id).one()
    return render_template('item.html', category_id=category_id, item=item)


# 1.Write create new item function
@app.route('/catalog/<int:category_id>/new/', methods=['GET', 'POST'])
def newItem(category_id):
    if request.method == 'POST':
        newItem = Item(name = request.form['name'],
                       description = request.form['description'],
                       price = request.form['price'],
                       category_id = category_id)
        session.add(newItem)
        session.commit()
        flash("%s has been created!" % newItem.name)
        return redirect(url_for('showCategory', category_id = category_id))
    else:
        return render_template('newItem.html', category_id = category_id)

@app.route('/catalog/new', methods=['GET','POST'])
def newCategory():
    if request.method == 'POST':
        newCategory = Category(name = request.form['name'])
        session.add(newCategory)
        session.commit()
        flash("%s has been created!" % newCategory)
        return redirect(url_for('showCatalog'))
    else:
        return render_template('newCategory.html')

# 2.Write edit item function
@app.route('/catalog/<int:category_id>/<int:item_id>/edit/', methods=['GET', 'POST'])
def editItem(category_id, item_id):
    editedItem = session.query(Item).filter_by(id = item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        session.add(editedItem)
        session.commit()
        flash("%s has been edited" % editedItem.name)
        return redirect(url_for('showCategory', category_id=category_id))
    else:
        return render_template('editItem.html',
                                category_id = category_id,
                                item_id = item_id,
                                i = editedItem)

@app.route('/catalog/<int:category_id>/delete', methods=['GET','POST'])
def deleteCategory(category_id):
    categoryToDelete = session.query(Category).filter_by(id = category_id).one()
    if request.method == 'POST':
        session.delete(categoryToDelete)
        session.commit()
        flash("%s has been deleted!" % categoryToDelete.name)
        return redirect(url_for('showCatalog'))
    else:
        return render_template('deleteCategory.html')

# 3.Write delete item function
@app.route('/catalog/<int:category_id>/<int:item_id>/delete/', methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
    itemToDelete = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("%s has been deleted!" % itemToDelete.name)
        return redirect(url_for('showCategory', category_id=category_id))
    else:
        return render_template('deleteItem.html', category_id=category_id, i=itemToDelete)



if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
