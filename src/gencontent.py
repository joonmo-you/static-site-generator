import os
from pathlib import Path

from block_markdown import markdown_to_html_node


def generate_pages_recursive(
    dir_path_contents: str, template_path: str, dest_dir_path: str
) -> None:
    for filename in os.listdir(dir_path_contents):
        from_path = os.path.join(dir_path_contents, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            generate_page(
                from_path, template_path, Path(dest_path).with_suffix(".html")
            )
        else:
            generate_pages_recursive(from_path, template_path, dest_path)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    from_file = open(from_path, "r")
    markdown = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown)
    html = node.to_html()

    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)


def extract_title(markdown: str):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.split("# ", maxsplit=1)[1]
    raise ValueError("no title found")
