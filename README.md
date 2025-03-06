# dumpsWikipedia

# Introduction

This set of programs allows the extraction of article text having a category form a given list of categories from Wikipedia dumps. This is useful for the creation of comparable corpora for a given subject.

To run the programs we need a set of files:

* The database: [http://lpg.uoc.edu/CCWikipedia/CPFromWiki-20250306.sqlite](http://lpg.uoc.edu/CCWikipedia/CPFromWiki-20250306.sqlite)
* The wikipedia dump: it is the file *-pages-articles.xml.bz2 from the given language wikipedia from [https://dumps.wikimedia.org/](https://dumps.wikimedia.org/)
* The categories (in English) that we want to explore. You can get a list of categories by academic discipline from: [https://en.wikipedia.org/wiki/Outline_of_academic_disciplines](https://en.wikipedia.org/wiki/Outline_of_academic_disciplines)

# Get the list of relevant categories in the target language

To create the list of relevant categories in the target language from an English category or a set of English categories, we can use the program createCategoryList.py. The option -h shows the help of the program:

```
python createCategoryList.py -h
usage: createCategoryList.py [-h] -d FILENAME -c CATEGORIA --level LEVEL --lang LANG -o OUTFILE

Script for the creation of lists of categories from Wikipedia

options:
  -h, --help            show this help message and exit
  -d FILENAME, --database FILENAME
                        The CCW sqlite database to use.
  -c CATEGORIA, --categories CATEGORIA
                        The categories to search for (a category or a list of categories separated by ,
  --level LEVEL         The category level depth.
  --lang LANG           The language (two letter ISO code used in Wikipedia.
  -o OUTFILE, --output OUTFILE
                        The name of the output path.
```

To get all the categories in Catalan from Linguistics and Philology with a deph of 3, we can write:

```
python createCategoryList.py -d CPfromWiki.sqlite -c Linguistics,Philology --level 3 --lang ca -o categories-cat.txt
```

In the file categories-cat.txt we will have th list of categories that can be used in the next step.

This program has a version with an easy-to-use GUI interface: createCategoryListGUI. The windows executable version is available in the release. When we start the program the following interface is shown:

![](https://github.com/mtuoc/tutorials/blob/main/images/CreateCategoryList.JPG)

# Extract the text by category

To extract all the text of all Wikipedia articles having a category from a list of categories, the script wikipedia2text.py can be used.  The option -h shows the help:

```
python3 wikipedia2text.py -h
usage: wikipedia2text.py [-h] -d DUMP_PATH -l LANGUAGE -c CATEGORIES -o OUTDIR

Script to convert Wikipedia dumps to text files according to a set of categories

options:
  -h, --help            show this help message and exit
  -d DUMP_PATH, --dump DUMP_PATH
                        The wikipedia dump.
  -l LANGUAGE, --language LANGUAGE
                        The language code (en, es, fr ...).
  -c CATEGORIES, --categories CATEGORIES
                        A file with one category per line.
  -o OUTDIR, --outdir OUTDIR
                        The output directory
```

The list of categories should be in a file with one category per line. The categories should be written in the same language as the Wikipedia we're using. As the list of categories we can use the file obtained by createCategoryList program explained above.

An example of use would be:

```python3 wikipedia2text.py -d cawiki-20240501-pages-articles.xml.bz2 -l ca -c categories-cat.txt -o linguistics-cat```

In the file categories-cat.txt we have a list of categories in Catalan. We have downloaded the dump cawiki-20240501-pages-articles.xml.bz2 from  [https://dumps.wikimedia.org/backup-index.html](https://dumps.wikimedia.org/backup-index.html)

This program has a GUI version wikipedia2textGUI, that is also available as a windows executable in the release. When you run the program the following interface is shown:

![](https://github.com/mtuoc/tutorials/blob/main/images/wikipedia2textGUI.JPG)

