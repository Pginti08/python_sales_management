## to clone the code

git clone https://github.com/Vyzion-Innovation/python_sales_management 

## install python  https://www.python.org/downloads/

## to check if python installed 
python --version
# or
python3 --version

## install Pip   
apt install python3-pip

## Create Virtual Environment
python -m venv venv
source venv/bin/activate 

## Install Django and PostgreSQL Dependencies
pip install django psycopg2-binary

## Install PostgreSQL and Create Database  https://www.postgresql.org/download/
sudo service postgresql start

## make migration & migrate 
python manage.py makemigrations
python manage.py migrate

## Create Superuser 
python manage.py createsuperuser

## Run the Development Server

sudo -i -u postgres psql
sudo service postgresql restart

python manage.py migrate

source venv/bin/activate

// to open database 
sudo -u postgres psql test_development;

// to keep server running in background.
nohup python manage.py runserver 0.0.0.0:8000 &