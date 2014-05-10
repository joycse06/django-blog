This is a very simple Blog built with django as part of my attempt to learn django.

Installation:
-------------------

1. Checkout the code
2. Create a virtual Environment
3. Install the dev dependencies with the following command
   pip install -r reqs/dev.txt
4. Once all the dependencies are installed create the database using syncdb like
   python manage.py syncdb

   It will create the database tables from Models and also ask for creating a super user. Create one with
    your preferred username and password.

5. then run migration with
    python manage.py migrate
6. Now start the server and view the site in browser
    python manage.py runserver

    It will start the server and listen on http://127.0.0.1:8000