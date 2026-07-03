class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str] | None = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        props_html: list[str] = []
        for key, value in self.props.items():
            props_html.append(f'{key}="{value}"')
        return " ".join(props_html)

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(
        self, tag: str, children: list["HTMLNode"], props: dict[str, str] | None = None
    ) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag == None:
            raise ValueError("invalid HTML: no tag")

        if self.children == None:
            raise ValueError("invalid HTML: no children")

        return f"<{self.tag}{"" if self.props == None else " " + self.props_to_html()}>{"".join([child.to_html() if isinstance(child, HTMLNode) else child for child in self.children])}</{self.tag}>"


class LeafNode(HTMLNode):
    def __init__(
        self, tag: str | None, value: str, props: dict[str, str] | None = None
    ) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value == None:
            raise ValueError("invalid HTML: no value")

        if self.tag == None:
            return self.value

        return f"<{self.tag}{"" if self.props == None else " " + self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> None:
        return f"HTMLNode({self.tag}, {self.value}, {self.props})"
