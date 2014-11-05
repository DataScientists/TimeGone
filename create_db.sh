#!/bin/bash
set -x
set -e
mysql -u root  << EOF
drop database if exists TimeGone;
create database TimeGone default character set "utf8";
grant all on TimeGone.* to TimeGone@localhost identified by "TimeGone";
EOF
cd TimeGone
./manage.py syncdb --noinput
./manage.py loaddata initial_data
echo "You can 'cd TimeGone && ./manage.py runserver' now"
