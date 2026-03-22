import os
import shutil
import sys

from textnode import TextNode, TextType
from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive



def main():
    default_basepath = '/'
    basepath = default_basepath
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    
    
    public = './docs'
    static = './static'
    if os.path.exists(public):
        shutil.rmtree(public)
    os.mkdir(public)
    copy_files_recursive(static, public)
    print('about to generate page(s)')
    generate_pages_recursive('content', 'template.html', 'docs', basepath)
    
    



main()