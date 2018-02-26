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
@app.route('/catalog/<int:category_id>/new/')
def newCategoryItem(category_id):
    return "A page to create a new item"
# 2.Write edit item function
@app.route('/catalog/<int:category_id>/<int:item_id>/edit/')
def editCategoryItem(category_id, item_id):
    return "A page to edit an item"
# 3.Write delete item function
@app.route('/catalog/<int:category_id>/<int:item_id>/delete/')
def deleteCategoryItem(category_id, item_id):
    return "A page to delete an item"

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
