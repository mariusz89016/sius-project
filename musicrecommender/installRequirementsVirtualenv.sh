echo 'Type name virtualenv name:'
read env_name
virtualenv env_name
source env_name/bin/activate
pip install -r requirements.txt
