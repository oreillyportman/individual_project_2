#! /bin/bash

if [ -z ${MYSQL_ROOT_PASSWORD} ] || 
   [ -z ${MYSQL_USER} ] || 
   [ -z ${MYSQL_PASSWORD} ] ||
   [ -z ${SECRET_KEY} ] ||
   [ -z ${MYSQL_DATABASE} ]
then
    echo "make sure all of the environment variables are exported:"
    echo "MYSQL_PASSWORD, MYSQL_USER, MYSQL_ROOT_PASSWORD, SECRET_KEY, MYSQL_DATABASE"
    exit 1
fi
