#!/bin/sh

cd jupyter-notebooks
git checkout ipynb

jupyter nbconvert --sanitize-html --to notebook --inplace */*.ipynb

# format notebooks
black -l 79 */*.ipynb

# sort imports
isort */*.py

# convert Jupyter Notebooks to Python scripts
jupyter nbconvert --to script */*.ipynb

# remove "# In []" and multiple blank lines
for f in */*.py;
do sed -i -e '/^# In\[/d' $f
cat -s $f > $f.txt
mv $f.txt $f
done

# format scripts
black -l 79 */*.py

# delete existing Python scripts
rm -r ../draft/nb
mkdir ../draft/nb

# copy files to temporary directory
# https://unix.stackexchange.com/a/132601
cp **/*.py --parents ../draft/nb
