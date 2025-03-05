import mwxml
import mwparserfromhell
import bz2
import sys
import argparse
import codecs
import os
import re

from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askdirectory

from tkinter import ttk


import tkinter 

# Function to extract plain text from wikitext
def extract_text_from_wikitext(wikitext):
    wikicode = mwparserfromhell.parse(wikitext)
    return wikicode.strip_code()

# Function to extract categories from wikitext based on language-specific category namespace
def extract_categories_from_wikitext(wikitext, category_namespace):
    wikicode = mwparserfromhell.parse(wikitext)
    categories = []
    for link in wikicode.filter_wikilinks():
        if link.title.lower().startswith(category_namespace.lower() + ":"):
            categories.append(str(link.title))
    return categories

    


def go():
    dump_path = E1.get()
    language = E2.get()
    categoriesfile=E4.get()
    outdir=E3.get()
    titlesfile=E5.get()
    if titlesfile==None:
        titlesfile="titles-list.txt"
    sortidatitles=codecs.open(titlesfile,"w",encoding="utf-8")

    if not os.path.exists(outdir):
        os.makedirs(outdir)

    usercategories=[]
    if not categoriesfile==None:
        entrada=codecs.open(categoriesfile,"r",encoding="utf-8")
        for linia in entrada:
            linia=linia.rstrip()
            usercategories.append(linia)
        entrada.close()

    # Define a dictionary with category namespaces for different languages
    category_namespaces = {
        "en": "Category",
        "ceb": "Kategoriya",
        "de": "Kategorie",
        "fr": "Catégorie",
        "sv": "Kategori",
        "nl": "Categorie",
        "ru": "Категория",
        "it": "Categoria",
        "es": "Categoría",
        "pl": "Kategoria",
        "ja": "カテゴリ",
        "vi": "Thể loại",
        "war": "Kaarangay",
        "zh": "分类",
        "uk": "Категорія",
        "ar": "تصنيف",
        "pt": "Categoria",
        "fa": "رده",
        "ca": "Categoria",
        "sr": "Категорија",
        "id": "Kategori",
        "ko": "분류",
        "no": "Kategori",
        "fi": "Luokka",
        "hu": "Kategória",
        "cs": "Kategorie",
        "ro": "Categorie",
        "tr": "Kategori",
        "eu": "Kategoria",
        "eo": "Kategorio",
        "da": "Kategori",
        "bg": "Категория",
        "sk": "Kategória",
        "kk": "Санат",
        "he": "קטגוריה",
        "lt": "Kategorija",
        "hr": "Kategorija",
        "az": "Kateqoriya",
        "sl": "Kategorija",
        "et": "Kategooria",
        "el": "Κατηγορία",
        "gl": "Categoría",
        "simple": "Category",
        "th": "หมวดหมู่",
        "sh": "Kategorija",
        "be": "Катэгорыя",
        "ms": "Kategori",
        "ka": "კატეგორია",
        "hi": "श्रेणी",
        "mk": "Категорија",
        "bs": "Kategorija",
        "af": "Kategorie",
        "uz": "Turkum",
        "bn": "বিষয়শ্রেণী",
        "lv": "Kategorija",
        "hy": "Կատեգորիա",
        "tt": "Төркем",
        "ur": "زمرہ",
        "azb": "بؤلمه",
        "ta": "பகுப்பு",
        "be-tarask": "Катэгорыя",
        "zh-min-nan": "分類",
        "te": "వర్గం",
        "tl": "Kategorya",
        "jv": "Kategori",
        "oc": "Categoria",
        "tg": "Гурӯҳ",
        "su": "Kategori",
        "kn": "ವರ್ಗ",
        "mg": "Sokajy",
        "mi": "Rōpū",
        "arz": "تصنيف",
        "scn": "Categoria",
        "sa": "वर्गः",
        "ne": "श्रेणी",
        "ckb": "پۆل",
        "gd": "Roinn-seòrsa",
        "ht": "Kategori",
        "mr": "वर्ग",
        "sq": "Kategori",
        "is": "Flokkur",
        "so": "Qeyb",
        "cy": "Categori",
        "br": "Rummad",
        "co": "Categoria",
        "szl": "Kategoria",
        "tk": "Kategoriýa",
        "pnb": "زمرہ",
        "sw": "Jamii",
        "fj": "Wase",
        "lrc": "پۆل",
        "dv": "ޤިސްމު",
        "nah": "Neneuhcāyōtl",
        "bat-smg": "Kateguorėjė",
        "bug": "Kategori",
        "cu": "Катигорїꙗ",
        "kw": "Class",
        "gv": "Ronney",
        "lez": "Категория",
        "ab": "Категориа",
        "bm": "Catégorie",
        "tyv": "Категория",
        "ve": "Konḓwa",
        "sn": "Chikamu",
        "pi": "विभागो",
        "iu": "ᑎᑎᕋᐅᓯᔭᖅ",
        "ny": "Gulu",
        "min": "Kategori",
        "zu": "Isigaba",
        "qu": "Katiguriya",
        "fy": "Kategory",
        "sah": "Категория",
        "kl": "Sumut ataqatigiissut",
        "kab": "Awrir",
        "haw": "Māhele",
        "ln": "Catégorie",
        "ug": "تۈر",
        "an": "Categoría",
        "mwl": "Categoria",
        "bi": "Kategori",
        "st": "Sehlopha",
        "li": "Categorie",
        "mt": "Kategorija",
        "tpi": "Kategri",
        "hsb": "Kategorija",
        "to": "Vahe",
        "ki": "Kĩrĩ",
        "yo": "Ẹ̀ka",
        "tw": "Nkyekyɛmu",
        "mg": "Sokajy",
        "tyv": "Категория",
        "ve": "Konḓwa",
        "tum": "Tchingwe",
        "lo": "ປະເພດ",
        "lad": "Kateggoría",
        "csb": "Kategòrëjô",
        "as": "শ্ৰেণী",
        "rw": "Icyiciro",
        "xh": "Udidi",
        "ts": "Xikategoria",
        "tn": "Setlhopha",
        "tk": "Kategoriýa",
        "tw": "Nkyekyɛmu",
        "wa": "Categoreye",
        "wo": "Wàll",
        "wuu": "分类",
        "xh": "Udidi",
        "yi": "קאַטעגאָריע",
        "yo": "Ẹ̀ka",
        "diq": "Kategoriye",
        "zap": "Ninyakayu",
        "sn": "Chikamu",
        "za": "分類",
        "zu": "Isigaba",
        "ast": "Categoría"
    }

    if not language in category_namespaces:
        print("ERROR: the specified language is not in the category_namespaces. Edit the code to add it.")
        



    valid_categories = []
    for cat in usercategories:
        catcat=category_namespaces[language]+":"+cat
        valid_categories.append(catcat)

    # Get the category namespace for the specified language
    category_namespace = category_namespaces.get(language, "Category")

    # Open the dump file
    with bz2.open(dump_path, 'rb') as f:
        # Parse the dump file
        dump = mwxml.Dump.from_file(f)
        
        # Iterate over each page in the dump
        for page in dump:
            if not page.redirect:  # Skip redirect pages
                for revision in page:
                    # Extract categories from the wikitext
                    categories = extract_categories_from_wikitext(revision.text, category_namespace)
                    if any(category in valid_categories for category in categories) or len(valid_categories)==0:
                        text = extract_text_from_wikitext(revision.text)
                        print(f"Title: {page.title}")
                        sortidatitles.write(page.title+"\n")
                        filename=page.title.replace(" ","_")+".txt"
                        full_path = os.path.join(outdir, filename)
                        try:
                            sortida=codecs.open(full_path,"w",encoding="utf-8")
                            sortida.write(page.title+"\n")
                            linies=text.split("\n")
                            for linia in linies:
                                linia=linia.strip()
                                
                                if not linia.startswith(category_namespaces[language]) and not linia.startswith("|") and not linia.startswith("<") and not linia.startswith("!") and not linia.startswith("{")and len(linia)>0:
                                    sortida.write(linia+"\n")
                            sortida.close()
                        except:
                            pass
    sortidatitles.close()


'''
parser = argparse.ArgumentParser(description='Script to convert Wikipedia dumps to text files according to a set of categories')
parser.add_argument('-d','--dump', action="store", dest="dump_path", help='The wikipedia dump.',required=True)
parser.add_argument('-l','--language', action="store", dest="language", help='The language code (en, es, fr ...).',required=True)
parser.add_argument('-o','--outdir', action="store", dest="outdir", help='The output directory.',required=True)
parser.add_argument('-c','--categories', action="store", dest="categories", help='A file with one category per line.',required=False)
parser.add_argument('-t','--titlesfile', action="store", dest="titlesfile", help='A file where the converted article titles will be stored. By default titles-list.txt.',required=False)
'''

def select_wikipedia_dump():
    inputfile = askopenfilename(initialdir = ".",filetypes =(("Dump files", ["*.bz2"]),("All Files","*.*")),
                           title = "Choose a wikipedia dump to use.")
    E1.delete(0,END)
    E1.insert(0,inputfile)
    E1.xview_moveto(1)
    
def select_output_dir():
    infile = askdirectory(initialdir = ".",title = "Select the output directory.")
    E3.delete(0,END)
    E3.insert(0,infile)
    E3.xview_moveto(1)
    
def select_categories_file():
    inputfile = askopenfilename(initialdir = ".",filetypes =(("text files", ["*.txt"]),("All Files","*.*")),
                           title = "Choose a category file to use.")
    E4.delete(0,END)
    E4.insert(0,inputfile)
    E4.xview_moveto(1)
    
def select_titles_file():
    inputfile = asksaveasfilename(initialdir = ".",filetypes =(("text files", ["*.txt"]),("All Files","*.*")),
                           title = "Choose a file to store the list of titles.")
    E4.delete(0,END)
    E4.insert(0,inputfile)
    E4.xview_moveto(1)

top = Tk()
top.title("Wikipedia2textGUI")

B1=tkinter.Button(top, text = str("Wikipedia dump"), borderwidth = 1, command=select_wikipedia_dump,width=14).grid(row=0,column=0)
E1 = tkinter.Entry(top, bd = 5, width=50, justify="right")
E1.grid(row=0,column=1)

L2 = Label(top,text="Language:").grid(sticky="E",row=1,column=0)
E2 = tkinter.Entry(top, bd = 5, width=3, justify="left")
E2.grid(sticky="W",row=1,column=1)

B3=tkinter.Button(top, text = str("Output dir"), borderwidth = 1, command=select_output_dir,width=14).grid(row=2,column=0)
E3 = tkinter.Entry(top, bd = 5, width=50, justify="right")
E3.grid(row=2,column=1)

B4=tkinter.Button(top, text = str("Categories file"), borderwidth = 1, command=select_categories_file,width=14).grid(row=3,column=0)
E4 = tkinter.Entry(top, bd = 5, width=50, justify="right")
E4.grid(row=3,column=1)

B5=tkinter.Button(top, text = str("Titles file"), borderwidth = 1, command=select_titles_file,width=14).grid(row=4,column=0)
E5 = tkinter.Entry(top, bd = 5, width=50, justify="right")
E5.grid(row=4,column=1)

E5.delete(0,END)
E5.insert(0,"titles-list.txt")
E5.xview_moveto(1)

B6=tkinter.Button(top, text = str("Go"), borderwidth = 1, command=go,width=14).grid(row=5,column=0)

   
top.mainloop()