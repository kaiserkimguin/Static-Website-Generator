import os
import shutil

from textnode import TextNode, TextType
from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive



def main():
    public = './public'
    static = './static'
    if os.path.exists(public):
        shutil.rmtree(public)
    os.mkdir(public)
    copy_files_recursive(static, public)
    print('about to generate page(s)')
    generate_pages_recursive('content', 'template.html', 'public')
    
    



main()