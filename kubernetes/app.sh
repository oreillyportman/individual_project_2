#! /bin/bash
./validate-env.sh

# flask-app
app_environment=(
    "s/{{MYSQL_USER}}/${MYSQL_USER}/g;" 
    "s/{{MYSQL_PASSWORD}}/${MYSQL_PASSWORD}/g;" 
    "s/{{MYSQL_DATABASE}}/${MYSQL_DATABASE}/g;" 
    "s/{{SECRET_KEY}}/${SECRET_KEY}/g;" 
)
sed "$(IFS=; echo "${app_environment[*]}")" flask-blog-app.yaml

