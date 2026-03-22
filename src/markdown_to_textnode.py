from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT or delimiter == None or delimiter == "" :
            new_nodes.append(node)
        
        else: 
            temp = node.text.split(delimiter)
            if len(temp) % 2 != 0: 
                for i, section in enumerate(temp):
                    if i % 2 == 0 and len(section) != 0:
                        new_nodes.append(TextNode(section,TextType.TEXT))
                    elif i % 2 != 0 and len(section) != 0:
                        new_nodes.append(TextNode(section, text_type))
            else:
                raise Exception("invalid markdown syntax")
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes



def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    temp_nodes = split_nodes_image([node])
    temp_nodes = split_nodes_link(temp_nodes)
    temp_nodes = split_nodes_delimiter(temp_nodes,'**',TextType.BOLD)
    temp_nodes = split_nodes_delimiter(temp_nodes,'`',TextType.CODE)
    temp_nodes = split_nodes_delimiter(temp_nodes, '_', TextType.ITALIC)
    return temp_nodes


def extract_markdown_images(text):
    matches = re.findall( r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return matches