# fab_test

1. create a virtual environment, activate it
2. pip install -r requirements.txt
3. Create an admin user: flask fab create-admin
4. run the application: flask run

task:

Go to the Upload File tab, you will see dropdowns for car brand and car model.
The idea is that if the user selects Toyota only the toyota models will show in the
next dropdown. 
The relevant files to modify are in the folder app, view.py and eventually model.py.

This has been created using flaskappbuilder, which in turn uses WTForms. 