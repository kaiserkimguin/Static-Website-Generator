
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None , add_tags: list | None = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        self.add_tags = add_tags

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        if self.props is None:
            return ""
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("invalid HTML: no value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag , children : list, props= None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("No tag given. Conversion to HTML unsuccesful.")
        elif self.children == None or len(self.children) == 0:
            raise ValueError("No children given. This is a leaf node. Conversion unsuccesful")
        else:
            children_html = "".join(child.to_html() for child in self.children)
            return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"