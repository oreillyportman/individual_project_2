#! /bin/bash
./validate-env.sh

# mysql
mysql_environment=(
    "s/{{MYSQL_ROOT_PASSWORD}}/${MYSQL_ROOT_PASSWORD}/g;" 
    "s/{{MYSQL_DATABASE}}/${MYSQL_DATABASE}/g;" 
    "s/{{MYSQL_USER}}/${MYSQL_USER}/g;" 
    "s/{{MYSQL_PASSWORD}}/${MYSQL_PASSWORD}/g;"
)
sed "$(IFS=; echo "${mysql_environment[*]}")" flask-blog-mysql.yaml

