#!/bin/sh

git checkout ipynb

# convert Jupyter Notebooks to Python scripts
jupyter nbconvert --to script */*.ipynb

# remove "# In []" and multiple blank lines
for f in */*.py;
do sed -i -e '/^# In\[/d' $f
cat -s $f > $f.txt
mv $f.txt $f
done
