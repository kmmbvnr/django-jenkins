#!/bin/bash

echo "Waiting for PostgreSQL to run..."
sleep 1
while ! /usr/bin/pg_isready -q
do
    sleep 1
    echo -n "."
done

/sbin/setuser postgres /usr/bin/psql -c "ALTER USER postgres with PASSWORD 'postgres';"