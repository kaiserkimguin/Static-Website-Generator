import re
import os

from pathlib import Path

from markdown_block import markdown_to_html_node
from htmlnode import ParentNode

def extract_title(markdown):
    lines = markdown.split('\n')
    for line in lines:
        if line.startswith('# '):
            newline = line[2:].strip()
            return newline
    raise Exception('No "h1 header" found')


def generate_page(from_path, template_path, dest_path):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    from_read = open(from_path).read()
    template_read = open(template_path).read()
    from_node = markdown_to_html_node(from_read)
    from_html = from_node.to_html()
    from_title = extract_title(from_read)
    template_final = template_read.replace('{{ Title }}', from_title)
    template_final = template_final.replace('{{ Content }}', from_html)
    dest_dir_path = os.path.dirname(dest_path)
    os.makedirs(dest_dir_path, exist_ok=True)
    with open(dest_path, 'w') as f:
        f.write(template_final)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
     for item in os.listdir(dir_path_content):
            item_path = os.path.join(dir_path_content,item)
            dest_path = os.path.join(dest_dir_path, item)

            if os.path.isfile(item_path):
                dest_path = Path(dest_path).with_suffix(".html")
                generate_page(item_path, template_path, dest_path)
                
            elif os.path.isdir(item_path):
                os.makedirs(dest_path, exist_ok=True)
                generate_pages_recursive(item_path, template_path, dest_path)






