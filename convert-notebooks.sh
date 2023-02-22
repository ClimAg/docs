# convert Jupyter Notebooks to Python scripts
jupyter nbconvert --to script jupyter-notebooks/*/*.ipynb

# remove "# In []" and multiple blank lines
for f in jupyter-notebooks/*/*.py;
do sed -i -e '/^# In\[/d' $f
cat -s $f > $f.txt
mv $f.txt $f
done

# format scripts
black -l 79 jupyter-notebooks/*/*.py
