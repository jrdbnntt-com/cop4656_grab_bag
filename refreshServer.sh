#!/usr/bin/env bash

echo -e "\nUPDATING SOURCE\n"
git reset --hard
git pull origin master

echo -e "\nINSTALLING DEPENDENCIES\n"
./venv/bin/pip3.5 install -r ./requirements.txt


echo -e "\nRECOLLECTING STATIC FILES\n"
rm -rf ./static_collected
./venv/bin/python3.5 ./manage.py collectstatic

echo -e "\nREBOOTING WEB SERVER\n"
apachectl restart

echo -e "\nSERVER REFRESH COMPLETE\n"
