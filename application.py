from flask import Flask, render_template, request
from flask import redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Item, Category, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
import math

app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json',
                       'r').read())['web']['client_id']

APPLICATION_NAME = "Blue Sky Tech Boutique"

engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create a state-token to prevent request forgery
# Store it in the session for later use


@app.route('/catalog/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = jsonify({'response':'Invalid state parameter.'}), 401
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = jsonify({'response':'Failed to upgrade the authorization code.'}), 401
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = jsonify({'response':result.get('error')}), 500
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = jsonify({'response':"Token's user ID doesn't match given user ID."}), 401
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = jsonify({'response':"Token's client ID does not match app's."}), 401
        print("Token's client ID does not match app's.")
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = jsonify({'response':'Already connected.'}), 200
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    flash("you are now logged in as %s" % login_session['username'])
    print("done!")
    return output

# TODO returns traceback error JSON response not serializable
# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
        # Only disconnect a connected user.
    access_token = login_session['access_token']
    if access_token is None:
        response = jsonify({'response':'Current user not connected.'}), 401
        flash(response)
        return redirect(url_for('showCatalog'))
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = jsonify({'response':'Successfully disconnected.'}), 200
        flash(response)
        #return response
        return redirect(url_for('showCatalog'))
    else:
        # For whatever reason, the given token was invalid.
        response = jsonify({'response':'Failed to revoke token for given user.'}), 200
        flash(response)
        return redirect(url_for('showCatalog'))

# JSON endpoint for category items
@app.route('/catalog/<int:category_id>/JSON')
def categoryJSON(category_id):
    items = session.query(Item).filter_by(category_id=category_id)
    return jsonify(items=[i.serialize for i in items])


@app.route('/catalog/<int:category_id>/<int:item_id>/JSON')
def itemJSON(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(item.serialize)


# Returns category name in template, passes category_id from a single item
def getCatName(category_id):
    catName = session.query(Category).filter_by(id=category_id).one()
    return catName.name


@app.route('/')
@app.route('/catalog/')
def showCatalog():
    categories = session.query(Category).all()
# TODO filter and order items by timestamp when field is added to Items Table
    items = session.query(Item).limit(6).all()
# Splits items list into sublists for use in html elements
    rowOneItems = items[0:2]
    rowTwoItems = items[2:4]
    rowThreeItems = items[4:6]
    return render_template('hometester.html',
                           categories=categories,
                           rowOneItems=rowOneItems,
                           rowTwoItems=rowTwoItems,
                           rowThreeItems=rowThreeItems,
                           login_session=login_session,)


# Write function that renders each category
@app.route('/catalog/<int:category_id>/')
def showCategory(category_id):
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id)
    return render_template('category.html',
                           category=category,
                           categories=categories,
                           items=items,
                           login_session=login_session)


@app.route('/catalog/<int:category_id>/<int:item_id>/')
def showItem(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    return render_template('item.html', category_id=category_id, item=item)


# 1.Write create new item function
@app.route('/catalog/<int:category_id>/new/', methods=['GET', 'POST'])
def newItem(category_id):
    if 'username' not in login_session:
        return redirect('/catalog/login')
    if request.method == 'POST':
        newItem = Item(name=request.form['name'],
                       description=request.form['description'],
                       price=request.form['price'],
                       category_id=category_id,
                       user_id=getUserID(login_session['email']))
        session.add(newItem)
        session.commit()
        flash("%s has been created!" % newItem.name)
        return redirect(url_for('showCategory', category_id=category_id))
    else:
        return render_template('newItem.html', category_id=category_id)


# New Category function
@app.route('/catalog/new', methods=['GET', 'POST'])
def newCategory():
    if 'username' not in login_session:
        return redirect('/catalog/login')
    if request.method == 'POST':
        newCategory = Category(name=request.form['name'],
                               user_id=login_session['user_id'])
        session.add(newCategory)
        session.commit()
        flash("%s has been created!" % newCategory)
        return redirect(url_for('showCatalog'))
    else:
        return render_template('newCategory.html')


# 2. Edit item function
@app.route('/catalog/<int:category_id>/<int:item_id>/edit/', methods=['GET',
                                                                      'POST'])
def editItem(category_id, item_id):
    if 'username' not in login_session:
        return redirect('/catalog/login')
    editedItem = session.query(Item).filter_by(id=item_id).one()
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
                               category_id=category_id,
                               item_id=item_id,
                               i=editedItem)


# Edit category function
@app.route('/catalog/<int:category_id>/edit', methods=['GET', 'POST'])
def editCategory(category_id):
    if 'username' not in login_session:
        return redirect('/catalog/login')
    editedCategory = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedCategory.name = request.form['name']
        session.add(editedCategory)
        session.commit()
        flash("%s has been edited!" % editCategory.name)
        return redirect(url_for('showCategory', category_id=category_id))
    else:
        return render_template('editCategory.html', category_id=category_id,
                               i=editedCategory)


# Delete Category function
@app.route('/catalog/<int:category_id>/delete', methods=['GET', 'POST'])
def deleteCategory(category_id):
    if 'username' not in login_session:
        return redirect('/catalog/login')
    categoryToDelete = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        session.delete(categoryToDelete)
        session.commit()
        flash("%s has been deleted!" % categoryToDelete.name)
        return redirect(url_for('showCatalog'))
    else:
        return render_template('deleteCategory.html', category=categoryToDelete)


# 3. Delete item function
@app.route('/catalog/<int:category_id>/<int:item_id>/delete/',
           methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
    if 'username' not in login_session:
        return redirect('/catalog/login')
    itemToDelete = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("%s has been deleted!" % itemToDelete.name)
        return redirect(url_for('showCategory', category_id=category_id))
    else:
        return render_template('deleteItem.html',
                               category_id=category_id,
                               i=itemToDelete)


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.jinja_env.globals.update(getCatName=getCatName)
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
