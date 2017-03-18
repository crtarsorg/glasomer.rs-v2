from app.forms.forms import LoginForm
from flask import Blueprint, render_template, request, Response, redirect, url_for, current_app
from app import user_datastore, bcrypt
from flask.ext.security import login_user, logout_user, roles_required
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')


@mod_auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":

        # Return the login form template
        return render_template('mod_auth/login.html')
    else:
        # Get data from the submitted form
        email = request.form['email']
        password = request.form['password']

        # Get the user from the database
        user = user_datastore.find_user(email=email)

        # Check if user exists
        if user:
            # Check if the given password matches with the one from the database
            if bcrypt.check_password_hash(user['password'], password):
                # If the password matches log in the user.
                login_user(user)
                # Return user to the index page after successful login
                return redirect(url_for('main.index'))
            else:
                # Return an error message
                error = "Password doesn't match."
                return render_template('mod_auth/login.html', error=error)
        else:
            error = "Sorry, user doesn't exist."
            return render_template('mod_auth/login.html', error=error)



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
