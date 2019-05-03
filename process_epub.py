#!/usr/bin/env python
# coding: utf-8

# In[36]:


import ebooklib
# import nltk  
from ebooklib import epub
from bs4 import BeautifulSoup


# In[82]:


def split_epub(filename):
    book=epub.read_epub(filename)
    text_list=[]
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            raw_text=item.get_body_content().decode('utf-8')
            soup = BeautifulSoup(raw_text, 'lxml')
            text_list.append(soup.get_text())
    return text_list

