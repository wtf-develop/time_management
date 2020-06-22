#!/bin/sh
chmod u+rx,g+rx,o+rx ./
find ./ -type f -exec chmod u-x+r,g-x+r,o-x+r {} \;
find ./ -type d -exec chmod u+rx,g+rx,o+rx {} \;
find ./ -type f -iname \*.py -exec chmod u+rx,g+rx,o+rx {} \;
chmod u+rx,g+rx,o+rx ./zzz_install_and_then_remove_it.sh
chmod u-x,g-x,o-x ./_common/api/*
chmod u-x,g-x,o-x ./mobile_service/apiv1/_mobile.py
