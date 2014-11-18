#!/bin/bash


./db/upgrade_database.sh

foreman start -f Procfile_for_dev_env 
