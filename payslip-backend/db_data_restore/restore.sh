#!/bin/bash
set -e

# Wait for Postgres to be ready
until pg_isready -U postgres; do sleep 1; done

# Only create the database if it doesn't exist
if ! psql -U postgres -lqt | cut -d \| -f 1 | grep -qw payslip_db; then
  psql -U postgres -c "CREATE DATABASE payslip_db;"
fi

# Restore the backup, ignoring owner/privileges and errors about existing objects
pg_restore -U postgres --no-owner --no-privileges -d payslip_db /docker-entrypoint-initdb.d/test_db || true