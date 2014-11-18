#!/bin/bash

createuser -s sysofrec
createdb -U sysofrec -O sysofrec sysofrec -T template0
