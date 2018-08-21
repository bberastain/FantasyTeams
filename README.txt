FLASK TEMPLATE

basic login and email functionality
just add logic to 'main' and templates to folder

TO USE

create a folder, copy over contents of this template

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

flask db init

flask db migrate -m 'init'

flask db upgrade

NOW YOU'RE READY :)

to run, use

export FLASK_APP=app_name.py

export FLASK_DEBUG= 0 or 1 (depending whether you want debugging mode on)

flask run

AND THAT'S IT
