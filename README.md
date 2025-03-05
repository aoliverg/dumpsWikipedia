# dumpsWikipedia

# Introduction

This set of programs allows the extraction of article text having a category form a given list of categories from Wikipedia dumps. This is useful for the creation of comparable corpora for a given subject.

To run the programs we need a set of files:

* The database  [http://lpg.uoc.edu/CPfromWiki202310.sqlite]( http://lpg.uoc.edu/CPfromWiki202310.sqlite)
* The wikipedia dump: it is the file *-pages-articles.xml.bz2 from the given language wikipedia from [https://dumps.wikimedia.org/](https://dumps.wikimedia.org/)
* The categories (in English) that we want to explore. You can get a list of categories by academic discipline from: [https://en.wikipedia.org/wiki/Outline_of_academic_disciplines](https://en.wikipedia.org/wiki/Outline_of_academic_disciplines)

# Get the list of relevant categories in the target language

# Extract the text by category

To extract all the text of all Wikipedia articles having a category from a list of categories, the script wikipedia2text.py can be used. The option -h shows the help:

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

The list of categories should be in a file with one category per line. The categories should be written in the same language as the Wikipedia we're using. 

An example of use would be:

```python3 wikipedia2text.py -d astwiki-20240501-pages-articles.xml.bz2 -l ast -c categories-ast.txt -o medicine-ast```

In the file categories-ast.txt we have a list of categories in Asturian. We have downloaded the dump astwiki-20240501-pages-articles.xml.bz2 from  https://dumps.wikimedia.org/backup-index.html.

# Creating a list of related categories
