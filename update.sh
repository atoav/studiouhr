#!/bin/sh
git fetch -q origin master
git reset -q --hard FETCH_HEAD
git clean -q -df
source .env/bin/activate
pip install --upgrade .