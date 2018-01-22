git fetch origin master
git reset --hard FETCH_HEAD
git clean -df
source .env/bin/activate
pip install --upgrade .