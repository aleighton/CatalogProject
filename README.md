<h1>Welcome!</h1>
Depending on which versions of *Flask*, *Sqlalchemy* and *Python* you're running,
the application may return an error, if so. Downgrade dependencies to these...

>     sudo pip install werkzeug==0.8.3
>     sudo pip install flask==0.9
>     sudo pip install Flask-Login==0.1.3
<ol type='1'>
<li>Run the database_setup.py as a Python script, this uses Sqlalchemy to create a sqlite Database
  with three tables: User, Item and Category. The User has an id that is a foreign key
  in both Item and Category tables. Category has an id that is a foreign key within Item and
  links each item with a corresponding category.</li>
<li>Run populate.py as a script in the terminal, it uses Sqlalchemy
  to start a connection to our newly created Database and populate it with data in each category.
  There is a dummy user specified at the top of the file. Feel free to change it with your own values
  </li>
  <li>Everything should be ready now, at this point just run application.py as a script on the terminal.
  </li>
<br>
  It will start a Flask server that you can access on http://localhost:5000/catalog
</ol>
Mentions: I'd like to acknowledge Udacity for supplying a large portion of authentication code for the project 


