cd jupyter-notebooks
# git checkout ipynb

# # convert Jupyter Notebooks to Python scripts
# jupyter nbconvert --to script */*.ipynb

# # remove "# In []" and multiple blank lines
# for f in */*.py;
# do sed -i -e '/^# In\[/d' $f
# cat -s $f > $f.txt
# mv $f.txt $f
# done

# # format scripts
# black -l 79 */*.py

# # copy files to temporary directory
# # https://unix.stackexchange.com/a/132601
# cp **/*.py --parents ../draft/nb

git checkout main

# delete existing Python scripts
rm */*.py

cd ../draft/nb/

# https://stackoverflow.com/a/63841503
cp **/*.py --parents ../../jupyter-notebooks
