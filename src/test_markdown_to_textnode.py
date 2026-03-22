import unittest

from markdown_to_textnode import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes , extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType

class TestMarkdownToTextNode(unittest.TestCase):
    def test_text(self):
        # Function test
        old_nodes = [
            TextNode("This is text with a `code block` word", TextType.TEXT),
            ]
        new_nodes = split_nodes_delimiter(old_nodes,"`", TextType.CODE)
        self.assertTrue(len(new_nodes)==3)

        # test wether the text_type != text eliminates the split
        old_nodes = [
            TextNode("This is text with a `code block` word", TextType.CODE),
            ]
        new_nodes = split_nodes_delimiter(old_nodes,"`", TextType.CODE)
        self.assertTrue(len(new_nodes)==1)

        # test wether no split when no delimiter
        old_nodes = [
            TextNode("This is text with a `code block` word", TextType.TEXT),
            ]
        new_nodes = split_nodes_delimiter(old_nodes,"", TextType.CODE)
        self.assertTrue(len(new_nodes)==1)
        self.assertTrue(new_nodes[0].text_type == TextType.TEXT)

        #test wether empty string is eliminated when delimiter at end or beginning
        old_nodes = [
            TextNode("`code block` word", TextType.TEXT),
            ]
        new_nodes = split_nodes_delimiter(old_nodes,"`", TextType.CODE)
        self.assertTrue(len(new_nodes)==2)

        # test multiple bold sections
        old_nodes = [
            TextNode("This **bold** is text **bold** with **bold** a **bold** word", TextType.TEXT),
            ]
        new_nodes = split_nodes_delimiter(old_nodes,"**", TextType.BOLD)
        self.assertTrue(len(new_nodes)==9)

        # test unclosed delimiter
        old_nodes = [
            TextNode("This **bold** is text **bold** with **bold** a **bold word", TextType.TEXT),
            ]
        with self.assertRaises(Exception):
            split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        
        # test len(old_nodes > 1)
        old_nodes = [
            TextNode("This is text with a `code block` word", TextType.TEXT),
            TextNode("This is text with a `code block` word", TextType.TEXT),
            TextNode("This is text with a `code block` word `code2` string", TextType.TEXT),
            ]
        new_nodes = split_nodes_delimiter(old_nodes,"`", TextType.CODE)
        self.assertTrue(len(new_nodes)==11)

class TestMarkdownImageToTextNode(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

class TestMarkdownLinkToTextNode(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [
                 TextNode("This is text with a link ", TextType.TEXT),
                 TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                 TextNode(" and ", TextType.TEXT),
                 TextNode(
                     "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                 ),
             ],
             new_nodes,
        )

class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnode(self):
        text = 'This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)'
        new_nodes = text_to_textnodes(text)

        self.assertEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

class TestExtractObjects(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

if __name__ == "__main__":
    unittest.main()

