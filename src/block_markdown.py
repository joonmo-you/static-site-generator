from enum import Enum

from htmlnode import HTMLNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    if all(
        lines[lineIndex].startswith(f"{lineIndex + 1}. ")
        for lineIndex in range(len(lines))
    ):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown):
    return list(
        filter(
            lambda block: block != "",
            map(lambda block: block.strip(), markdown.split("\n\n")),
        )
    )


def markdown_to_html_node(markdown: str):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_to_html_node(block)


def block_to_html_node(block: str):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html_node(block)
    raise ValueError("invalid block type")


def text_to_children(text: str) -> TextNode:
    return [text_node_to_html_node(text_node) for text_node in text_to_textnodes(text)]


def paragraph_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    paragraph = " ".join(lines)
    return ParentNode("p", text_to_children(paragraph))


def heading_to_html_node(block: str) -> ParentNode:
    [heading, text] = block.split(" ", 1)
    return ParentNode(f"h{len(heading)}", text_to_children(text))


def code_to_html_node(block: str) -> ParentNode:
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    child = text_node_to_html_node(
        TextNode(block.lstrip("```\n").rstrip("\n```"), TextType.TEXT)
    )
    code = ParentNode("code", child)
    return ParentNode("pre", [code])


def quote_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
    return ParentNode(
        "blockquote",
        text_to_children(" ".join(map(lambda line: line.lstrip(">").strip(), lines))),
    )


def unordered_list_to_html_node(block: str) -> ParentNode:
    items = block.split("\n")
    return ParentNode("ul", [ParentNode("li", item.lstrip("- ")) for item in items])


def ordered_list_to_html_node(block: str) -> ParentNode:
    items = block.split("\n")
    return ParentNode(
        "ol", [ParentNode("li", item.split(". ", 1)[1]) for item in items]
    )
