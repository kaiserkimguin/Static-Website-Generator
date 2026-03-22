import unittest
import re

from markdown_block import markdown_to_blocks, block_to_block_type, markdown_to_html_node, BlockType

class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

        md = """
This is **bolded** paragraph

\n\n\n\n\n\nThis is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line\n\n\n\n\n

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


        
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

              - This is a list
- with items           
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

class TestBlockToBlock(unittest.TestCase):
    def test_block_to_block(self):
        # heading true
        md_heading_true = '###### heading'

        blocktype = block_to_block_type(md_heading_true)

        self.assertEqual(blocktype,BlockType.HEADING)

        # heading false
        md_heading_false = '######heading'

        blocktype = block_to_block_type(md_heading_false)

        self.assertEqual(blocktype, BlockType.PARAGRAPH)

        # code true

        md_code_true = '```\n#this is code```'

        blocktype1 = block_to_block_type(md_code_true)

        self.assertEqual(blocktype1, BlockType.CODE)

        # code false

        md_code_false = '``` this is code```'

        blocktype = block_to_block_type(md_code_false)

        self.assertEqual(blocktype, BlockType.PARAGRAPH)

        # quote true

        md_quote_true = '''> abc
> cde
> fgh'''

        blocktype = block_to_block_type(md_quote_true)

        self.assertEqual(blocktype, BlockType.QUOTE)

        # quote false

        md_heading_false = '''> abc
> cde
< fgh'''

        blocktype = block_to_block_type(md_heading_false)

        self.assertEqual(blocktype, BlockType.PARAGRAPH)

        # ulist true

        md_ulist_true =  '- abc\n- cde\n- efg'

        blocktype = block_to_block_type(md_ulist_true)

        self.assertEqual(blocktype, BlockType.ULIST)

        # ulist false

        md_ulist_false = '''
- abc
- cde
- fgh'''

        blocktype = block_to_block_type(md_ulist_false)

        self.assertEqual(blocktype, BlockType.PARAGRAPH)

        # olist true

        md_olist_true = '''1. abc
2. cde
3. fgh'''

        blocktype = block_to_block_type(md_olist_true)

        self.assertEqual(blocktype, BlockType.OLIST)

        # olist false

        md_olist_false = '''1. abc
2. cde
2. fgh'''
        blocktype = block_to_block_type(md_olist_false)

        self.assertEqual(blocktype, BlockType.PARAGRAPH)

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

if __name__ == "__main__":
    unittest.main()