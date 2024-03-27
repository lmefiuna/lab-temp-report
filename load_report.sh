#! /bin/bash

########## Create python venv if does not exist ##########

if ! test -d ./venv; then
  echo "Python venv not found. Creating python venv"
  python3 -m venv venv
fi

source venv/bin/activate

python3 -c "import pandas" &>/dev/null
if [ ! $? -eq 0 ]; then
  echo "Installing requirements:"
  cat requirements.txt

  pip install -r requirements.txt >/dev/null
fi

python3 process_temperature_report.py "$1"

MYSQL_SECURE_FILE_PRIV_PATH="/var/lib/mysql-files"

cp "${1%.*}_processed.${1##*.}" $MYSQL_SECURE_FILE_PRIV_PATH
if [ ! $? -eq 0 ]; then
  echo
  echo "sudo privileges are needed to copy file to MySQL safe load data directory (/var/lib/mysql-files)"
  echo

  cp "${1%.*}_processed.${1##*.}" $MYSQL_SECURE_FILE_PRIV_PATH
fi

mysql -u example_user -D example_db --execute "LOAD data INFILE '$MYSQL_SECURE_FILE_PRIV_PATH/$(basename "${1%.*}_processed.${1##*.}")' INTO TABLE example_table FIELDS TERMINATED by ',' ENCLOSED by '\"' LINES TERMINATED by '\n' IGNORE 1 rows (@temp, @humidity,@timestamp) set Temp=@temp,RH=@humidity,Press=0,timestamp=@timestamp;"
