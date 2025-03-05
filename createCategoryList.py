#!/usr/bin/python3
#    createCCWCorpus
#    Copyright (C) 2021  Antoni Oliver
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sqlite3
import os
import gzip
import re
from bz2 import BZ2File as bzopen
import codecs
from lxml import etree as et
import sys
import argparse


    

def ensure_indices(cursor, indices):
    for index_name, index_sql in indices.items():
        # Verificar si el índice ya existe
        cursor.execute("""
            SELECT COUNT(1) 
            FROM sqlite_master 
            WHERE type='index' AND name=?;
        """, (index_name,))
        exists = cursor.fetchone()[0]
        if not exists:
            print(f"Creating index: {index_name}")
            cursor.execute(index_sql)
def go():
    required_indices = {
    "titles_title_idx": "CREATE INDEX IF NOT EXISTS titles_title_idx ON titles(title);",
    "langlinks_ident_lang_idx": "CREATE INDEX IF NOT EXISTS langlinks_ident_lang_idx ON langlinks(ident, lang);"
    }
    
    print("Verifying indexes.")
    ensure_indices(cur, required_indices)

    # Confirmar los cambios
    conn.commit()

    global categoria
    global level
    global articlelist
    global lang
    categories=[]
    categoriesTEMP=[]

    for cat in categoria.split(","):
        cat=cat.strip()
        categories.append(cat)
        categoriesTEMP.append(cat)
    categoriesAUX=[]
    while level>0:
        while(len(categoriesTEMP))>0:
            categoria=categoriesTEMP.pop(0)
            cur.execute('SELECT categoryREL from categoryrelations WHERE category=?', (categoria,))
            data=cur.fetchall()
            for d in data:
                categories.append(d[0])
                categoriesAUX.append(d[0])
        categoriesTEMP.extend(categoriesAUX)
        categoriesAUX=[]
        level-=1
    for categoriaEN in categories:
        if lang=="en":
            print(categoriaEN)
            sortida.write(categoriaEN+"\n")
        else:
            #select ident from titles where title="Existence";
            cur.execute('SELECT ident from titles WHERE title=?', (categoriaEN,))
            data=cur.fetchall()
            for d in data:
                identCat=d[0]
                #select title from langlinks where ident="312739" and lang="an";
                cur2.execute('SELECT title from langlinks WHERE ident=? and lang=?', (str(identCat),lang))
                data2=cur2.fetchall()
                for d2 in data2:
                    titleTGT=d2[0].replace("\\","")
                    print(titleTGT)
                    sortida.write(titleTGT+"\n")


if __name__ == "__main__":        
    parser = argparse.ArgumentParser(description='Script for the creation of lists of categories from Wikipedia')
    
    parser.add_argument("-d",'--database', action="store", dest="filename", help='The CCW sqlite database to use.',required=True)

    parser.add_argument("-c",'--categories', action="store", dest="categoria", help='The categories to search for (a category or a list of categories separated by ,',required=True)

    parser.add_argument('--level', action="store", dest="level", type=int, help='The category level depth.',required=True)
    
    parser.add_argument('--lang', action="store", dest="lang", help='The language (two letter ISO code used in Wikipedia.',required=True)
        
    parser.add_argument("-o",'--output', action="store", dest="outfile", help='The name of the output path.',required=True)
        
    args = parser.parse_args()  
    
    filename=args.filename

    conn=sqlite3.connect(filename)
    cur = conn.cursor() 
    cur2 = conn.cursor() 
    categoria=args.categoria
    level=args.level
    lang=args.lang
    outfile=args.outfile
    
    sortida=codecs.open(outfile,"w",encoding="utf-8")
    
 
    go()