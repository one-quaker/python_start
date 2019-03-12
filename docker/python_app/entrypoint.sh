#!/bin/bash

cd $APP_DIR/day7/django_app/

until make migrate;
do
    echo ...
    sleep 5
done

make create_admin
make collectstatic
$ENV_BIN_ROOT/gunicorn django_app.wsgi:application --name django_app --workers 2 --bind=0.0.0.0:8000 --reload --log-level=debug --log-file=-

# while [ "true" ]
#   do /bin/sleep 1
# done
