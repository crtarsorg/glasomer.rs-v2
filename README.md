# What Is This?
---------------

A quiz to assess who you should vote for in Serbian elections.

## Installation instructions:
---------------

### Things that are needed to install are listed in:

    - requirements.txt

### To install all the points from requirements file we have to run:

    - "bash install.sh"

### For the configuration stuff rename the config-template.cfg to:

    - "config.cfg"
    
### To add in the config.cfg that we just created:


    [Application]
    SERVER_PORT=
    SECRET_KEY=
    [Mongo]
    DB_NAME=
    [Logging]
    PATH=logs/error.log
    LEVEL=debug

## Deployment instructions:

1. Install Apache Virtual Hosts (if the server is configured for the first time)
   - sudo apt-get update

   - sudo apt-get install apache2

    After installing apache than there are created directories var/www
    Clone the app on the www directory:

    sudo git clone https://github.com/crtarsorg/glasomer.rs-v2.git

2. Enter now inside the glasomer.rs-v2 directory
3. Run the bash script in order to install the libraries that should be installed
       sudo bash install.sh

4. Check where the virtualenv is created as a directory venv

5. Installation and configuration of apache:

    - Install module mod_wsgi,
    this is a module of Apache HTTP Server that provides services for hosting Python apps that are web based .

        sudo apt-get install libapache2-mod-wsgi

    - After installation of this module there is created a file in our app as:

      app.wsgi

    - Configure the Server:
      There is a configuration file inside the directory of apache2 and the path to find this file is :

        etc/apache2/sites-available

        sudo nano glasomer.rs-v2.conf

          <VirtualHost *:80>
                          ServerName glasomer.rs
                          ServerAdmin admin@mywebsite.com
                          WSGIScriptAlias / /var/www/glasomer.rs-v2/app.wsgi
                          <Directory /var/www/glasomer.rs-v2/>
                                  Order allow,deny
                                  Allow from all
                          </Directory>
                          Alias /static /var/www/glasomer.rs-v2/app/static
                          <Directory /var/www/glasomer.rs-v2/app/static/>
                                  Order allow,deny
                                  Allow from all
                          </Directory>
                          ErrorLog ${APACHE_LOG_DIR}/error.log
                          LogLevel warn
                          CustomLog ${APACHE_LOG_DIR}/access.log combined
          </VirtualHost>

7. Install mongo
      sudo apt-get update
      sudo apt-get install -y mongodb-org

## Instructions for the login page:

Since we have also adminstration part,
 we are using authentication and there are some configurations that should be added on the config.cfg:

    [Authentication]
    LOGIN_USER_TEMPLATE_PATH=mod_auth/login.html
    LOGIN_URL=/auth/login
    REGISTER_USER_TEMPLATE_PATH=mod_auth/register.html
    CAN_REGISTER=True
    CONFIRM_EMAIL=False
    SEND_REGISTER_EMAIL=False
    SEND_PASSWORD_CHANGE_EMAIL=False
    SEND_CONFIRM_EMAIL_WITHIN=False
    PASSWORD_CHANGEABLE=False
    PASSWORD_HASH=bcrypt
    PASSWORD_SALT=

User registraion:
    For security reasons and we have only one user(admin) for the moment.
    In case we need to enable the registration, or to add another user as admin,
     we have to enable the action for registration in the :
        - mod_auth/registation
    For the moment this action is commented and we can't access to it.

Login:
    The url for the admin page is:

        http://glasomer.rs/admin

    If we are not authenticated than we will be redirected to:

        http://glasomer.rs/auth/login

    After login than we redirected again to:

        http://glasomer.rs/admin

## Instructions how admin is organized and how question should be added:

    The level of how the questions are added:

      1. Project
      2. Group
      3. Question

    By level we mean that the questions first are dependent from the project
    and than by the group that they are in.

    What do we mean by project?

    There is a possibility to add multiple projects and than enable or disable a project.
    There cannot be multiple projects enabled at once.
    The reason why we use projects is that we can make questionaries for different reasons,
    and we don't need to delete them.
    We can disable that project, create another one,
    enable it and start adding groups and questions for the enabled project.

    Managing Groups and questions:

    Here we are managing all in one table, we have datable for the groups and sub datatable the questions.
    So first we create a group and than we can enter in a group to add questions, into the sub datatable.

    Managing Groups:
    We are able to add, edit and delete the groups
    Notice for delete action: If we delete a group,
     there also will be deleted the questions that were dependent to that group.

    Managing questions:
    Also in the questions we can add, edit and delete them.

    Manage Candidates Dashboard:

    There is a part where we manage candidates, like adding, editing or deleting.
    Also after adding questions for an enabled projects,
    we can assign answers to candidates or editings answers to a specific candidate and a specific question.


    Text for the page "Sta je Glasomer"?

    The text displayed in the page is managed from the admin dashboard, and there is a specific page for it.
     We can add or edit it.
    Its not related something to the enabled project.















