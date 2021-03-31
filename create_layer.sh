#!/bin/bash

mkdir python
printf "oauth2client\ngoogle-api-python-client\npandas" > requirements.txt

if [ -f service_account.json ]; then
     mv service_account.json $PWD/python/.
else
    echo "Missing ga api credentials."
fi

docker run --rm \
--volume=$(pwd):/lambda-build \
-w=/lambda-build \
lambci/lambda:build-python3.8 \
pip3 install -r requirements.txt --target python

zip -r layer.zip python/