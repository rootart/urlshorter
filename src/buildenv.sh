#!/bin/sh
echo Creating env environment
virtualenv env

echo Install PIP inside virtual environment
./env/bin/easy_install pip

echo Installing dependencies to venv environment
./env/bin/pip install -E env -r ./pipreq.txt

