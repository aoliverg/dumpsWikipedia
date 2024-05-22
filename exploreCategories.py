import mwxml
import mwparserfromhell
import bz2
import sys
import argparse
import codecs
import os


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

parser = argparse.ArgumentParser(description='Script to explore categories from a Wikipedia dump')
parser.add_argument('-d','--dump', action="store", dest="dump_path", help='The wikipedia dump.',required=True)
parser.add_argument('-l','--language', action="store", dest="language", help='The language code (en, es, fr ...).',required=True)
parser.add_argument('-c','--categories', action="store", dest="category", help='A category or a list of categories separated by :.',required=True)
parser.add_argument('-o','--outfile', action="store", dest="outfile", help='The output directory.',required=True)
parser.add_argument('--limit', action="store", dest="limit", help='The limit in number of articles found.',required=False)

args = parser.parse_args()
dump_path = args.dump_path
language = args.language
category=args.category
outfile=args.outfile
limit=args.limit

categorylist=category.split(":")


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
    



category_namespace = category_namespaces.get(language, "Category")

# Open the dump file

categoriesmod=[]
for cat in categorylist:
    catmod=category_namespaces[language]+":"+cat
    categoriesmod.append(catmod)
    

categoryfreq={}
cont=0
with bz2.open(dump_path, 'rb') as f:
    # Parse the dump file
    dump = mwxml.Dump.from_file(f)
    
    # Iterate over each page in the dump
    for page in dump:
        if not page.redirect:  # Skip redirect pages
            for revision in page:
                # Extract categories from the wikitext
                categories = extract_categories_from_wikitext(revision.text, category_namespace)
                common_elements =  [element for element in categories if element in categoriesmod]
                if len(common_elements)>0:
                    cont+=1
                    print(cont,limit)
                    for categoria in categories:
                        categoria=categoria.replace(category_namespaces[language]+":","")
                        if not categoria in categoryfreq:
                            categoryfreq[categoria]=1
                        else:
                            categoryfreq[categoria]+=1
        if not limit==None and cont>=int(limit):
            break

sortida=codecs.open(outfile,"w",encoding="utf-8")

sorted_dict = dict(sorted(categoryfreq.items(), key=lambda item: item[1],reverse=True))

for key in sorted_dict:
    print(key,sorted_dict[key])
    sortida.write(key+"\n")
    
sortida.close()
