#!/bin/sh
chmod u+rx,g+rx,o+rx ./
find ./ -type f  -exec chmod u-x+r,g-x+r,o-x+r {} \;
find ./ -type d -exec chmod u+rx,g+rx,o+rx {} \;
find ./ -type f -iname \*.py -exec chmod u+rx,g+rx,o+rx {} \;
