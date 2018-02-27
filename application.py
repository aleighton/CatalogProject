from flask import Flask, render_template, request
from flask import redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Item, Category

app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Write function that serves all categories and new items


@app.route('/')
@app.route('/catalog/<int:category_id>/')
def categoryItems(category_id):
    category = session.query(Category).filter_by(id = category_id).one()
    items = session.query(Item).filter_by(category_id = category_id)
    return render_template('category.html', category=category, items=items)
# 1.Write create new item function
@app.route('/catalog/<int:category_id>/new/', methods=['GET', 'POST'])
def newCategoryItem(category_id):
    if request.method == 'POST':
        newItem = Item(name = request.form['name'],
                       description = request.form['description'],
                       price = request.form['price'],
                       category_id = category_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('categoryItems', category_id = category_id))
    else:
        return render_template('newItem.html', category_id = category_id)


# 2.Write edit item function
@app.route('/catalog/<int:category_id>/<int:item_id>/edit/', methods=['GET', 'POST'])
def editCategoryItem(category_id, item_id):
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
        return redirect(url_for('categoryItems', category_id=category_id))
    else:
        return render_template('editItem.html',
                                category_id = category_id,
                                item_id = item_id,
                                i = editedItem)


# 3.Write delete item function
@app.route('/catalog/<int:category_id>/<int:item_id>/delete/')
def deleteCategoryItem(category_id, item_id):
    return "A page to delete an item"

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
