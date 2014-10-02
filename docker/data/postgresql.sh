#!/bin/sh
# `/sbin/setuser postgres` runs the given command as the user `postgres`.
# If you omit that part, the command will be run as root.
exec /sbin/setuser postgres /usr/lib/postgresql/9.3/bin/postgres \
    -D /var/lib/postgresql/9.3/main \
    -c config_file=/etc/postgresql/9.3/main/postgresql.conf >> /var/log/postgresql.log 2>&1