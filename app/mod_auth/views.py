
from flask import Blueprint, render_template, request, redirect, url_for
from app import user_datastore, bcrypt
from flask.ext.security import login_user, logout_user
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

@mod_auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return redirect(url_for('admin.index'))



#@mod_auth.route('/register', methods=['GET', 'POST'])
#def register():
    if request.method == "GET":
        # Return the login form template
        return render_template('mod_auth/register.html')
    else:
        # Get data from the submitted form
        form = request.form
        email = form['email']

        # Generate a password hash
        password = bcrypt.generate_password_hash(form['password'], rounds=12)

        # Check if the email exists in the database and return an error
        if user_datastore.find_user(email=email):
            error = "A user with that e-mail already exists in the database"
            return render_template('mod_auth/register.html', error=error)
        else:
            # Create the user with the given credentials
            user_datastore.create_user(
                email=email,
                password = password
            )

            # Get the user instance
            user = user_datastore.find_user(email=email)

            # Login user
            login_user(user)

            # Return to the main index page
            return redirect(url_for('main.index'))


@mod_auth.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('map.index'))
