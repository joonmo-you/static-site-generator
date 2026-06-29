def markdown_to_blocks(markdown):
    return list(
        filter(
            lambda block: block != "",
            map(lambda block: block.strip(), markdown.split("\n\n")),
        )
    )
