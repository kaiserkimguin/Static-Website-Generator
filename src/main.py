import os
import shutil
import sys

from textnode import TextNode, TextType
from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive

if sys.argv[0] != None:
    basepath = sys.argv[0]
else:
    basepath = "/"

def main():
    public = './docs'
    static = './static'
    if os.path.exists(public):
        shutil.rmtree(public)
    os.mkdir(public)
    copy_files_recursive(static, public)
    print('about to generate page(s)')
    generate_pages_recursive('content', 'template.html', 'docs')
    
    



main()