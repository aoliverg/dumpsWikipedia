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

from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askdirectory

from tkinter import ttk


import tkinter 
    

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

    filename=E1.get()

    conn=sqlite3.connect(filename)
    cur = conn.cursor() 
    cur2 = conn.cursor() 
    categoria=E2.get()
    level=int(E3.get())
    lang=E4.get()
    outfile=E5.get()
    
    sortida=codecs.open(outfile,"w",encoding="utf-8")
    
    required_indices = {
    "titles_title_idx": "CREATE INDEX IF NOT EXISTS titles_title_idx ON titles(title);",
    "langlinks_ident_lang_idx": "CREATE INDEX IF NOT EXISTS langlinks_ident_lang_idx ON langlinks(ident, lang);"
    }
    
    print("Verifying indexes.")
    ensure_indices(cur, required_indices)

    # Confirmar los cambios
    conn.commit()

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


def select_database():
    inputfile = askopenfilename(initialdir = ".",filetypes =(("SQLite files", ["*.sqlite"]),("All Files","*.*")),
                           title = "Choose a database to use.")
    E1.delete(0,END)
    E1.insert(0,inputfile)
    E1.xview_moveto(1)
    
def select_output():
    articlelistfile = asksaveasfilename(initialdir = ".",filetypes =(("text files", ["*.txt"]),("All Files","*.*")),
                           title = "Choose a file to save the list of categories.")
    E5.delete(0,END)
    E5.insert(0,articlelistfile)
    E5.xview_moveto(1)

top = Tk()
top.title("Create Category List")

B1=tkinter.Button(top, text = str("Select Database"), borderwidth = 1, command=select_database,width=14).grid(row=0,column=0)
E1 = tkinter.Entry(top, bd = 5, width=50, justify="right")
E1.grid(row=0,column=1)

L2 = Label(top,text="Categories:").grid(sticky="E",row=1,column=0)
E2 = tkinter.Entry(top, bd = 5, width=50, justify="left")
E2.grid(row=1,column=1)

L3 = Label(top,text="Level:").grid(sticky="E",row=2,column=0)
E3 = tkinter.Entry(top, bd = 5, width=3, justify="left")
E3.grid(sticky="W",row=2,column=1)

L4 = Label(top,text="Lang:").grid(sticky="E",row=3,column=0)
E4 = tkinter.Entry(top, bd = 5, width=3, justify="left")
E4.grid(sticky="W",row=3,column=1)

B5=tkinter.Button(top, text = str("Select output"), borderwidth = 1, command=select_output,width=14).grid(row=4,column=0)
E5 = tkinter.Entry(top, bd = 5, width=50, justify="left")
E5.grid(row=4,column=1)

E5.delete(0,END)

B6=tkinter.Button(top, text = str("Go"), borderwidth = 1, command=go,width=14).grid(row=5,column=0)

E1.delete(0,END)
E1.xview_moveto(1)

E2.delete(0,END)
E2.xview_moveto(1)


    
top.mainloop()
    
 