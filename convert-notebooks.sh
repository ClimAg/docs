cd docs

git checkout main

# delete existing Python scripts
rm */*.py

cd ../draft/nb/

# https://stackoverflow.com/a/63841503
cp **/*.py --parents ../../docs
