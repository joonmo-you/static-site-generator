from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        new_nodes.extend(
            list(
                filter(
                    lambda node: node.text != "",
                    [
                        TextNode(
                            sections[i], TextType.TEXT if i % 2 == 0 else text_type
                        )
                        for i in range(len(sections))
                    ],
                )
            )
        )
    return new_nodes
