import os
import sys
import shutil

from copystatic import copy_files
from gencontent import generate_page, generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_contents = "./contents"
template_path = "./template.html"


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files(dir_path_static, dir_path_public)

    print("Generating page...")
    generate_pages_recursive(
        dir_path_contents, template_path, dir_path_public, basepath
    )


if __name__ == "__main__":
    main()
