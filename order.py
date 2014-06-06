#!/usr/bin/env python
# -*- coding: utf-8 -*-

import zipfile
import os
from lxml import etree

def get_the_book(start_dir):
    """
    at first we have to take the book from directory, than we have to get some
    info from it and than to put it to the right place.
    So get_the_book recursevly gets each book from directory.
    """
    for dir, dirnames, filenames in os.walk(start_dir):
        if "ORDERED" not in dir:
            for file in filenames:
                if file.endswith(".fb2.zip"):
                    read_the_book(os.path.join(dir,file))
                if file.endswith(".fb2"):
                    file = compress_this(os.path.join(dir,file))
                    print file
                    read_the_book(file)


def compress_this(file):
    """
    function that is zipping the book
    """
    try:
        import zlib
        compression = zipfile.ZIP_DEFLATED
    except:
        compression = zipfile.ZIP_STORED
    print file
    zf = zipfile.ZipFile(file + ".zip","w")
    zf.write(file, os.path.basename(file), compress_type = compression)
    zf.close()
    os.remove(file)
    return file + ".zip"


def read_the_book(book):
    """
    read_the_book function gets xml-tree from the file and is looking for
    author's name and surname.
    """
    try:
        file = zipfile.ZipFile(book,"r")
    except zipfile.BadZipfile:
        return
    print book
    book_object = file.namelist()[0]
    book_content = file.open(book_object,"r")
    try:
        xml_content = etree.parse(book_content)
    except etree.XMLSyntaxError:
        return
    author_first_name = xml_content.xpath('//ns:first-name', \
            namespaces={'ns': 'http://www.gribuser.ru/xml/fictionbook/2.0'})[0].text
    author_last_name = xml_content.xpath('//ns:last-name', \
            namespaces={'ns': 'http://www.gribuser.ru/xml/fictionbook/2.0'})[0].text
    if author_first_name and author_last_name: 
        put_the_book(author_first_name, author_last_name, book)
    book_content.close()
    file.close()


def put_the_book(a_fname, a_lname, fname):
    """
    put_the_book-function moves the book to the right place
    a_fname - author's first name
    a_lname - author's last name
    fname - file name to proceed
    """
    global ROOT_PATH
    dir_name = os.path.join(ROOT_PATH, "ORDERED/", a_lname+" "+a_fname)
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    tail = os.path.split(fname)[1].decode('utf-8','replace')
    #print fname, os.path.join(dir_name,tail)
    os.rename(fname,os.path.join(dir_name,tail))


ROOT_PATH = os.getcwd()
get_the_book(ROOT_PATH)


