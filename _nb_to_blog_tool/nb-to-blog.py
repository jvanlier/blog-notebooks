#!/usr/bin/env python
from pathlib import Path
import subprocess
import shutil

import click
import yaml


IMG_PATH = "assets/img/blog"


def _create_destination_dirs(path_notebook_dir):
    post_path_dir = path_notebook_dir.parent / "_output" / "_posts"
    post_path_dir.mkdir(parents=True, exist_ok=True)
    asset_path_dir = path_notebook_dir.parent / "_output" / IMG_PATH / path_notebook_dir.name
    asset_path_dir.parent.mkdir(parents=True, exist_ok=True)
    if asset_path_dir.exists():
        print(f"Warning: {asset_path_dir} already exists, aborting.")
        exit(1)

    return post_path_dir, asset_path_dir


def _run_jupyter_nbconvert(path_notebook):
    cmd = ["jupyter", "nbconvert", "--to", "markdown", str(path_notebook)]
    result = subprocess.run(cmd)
    if not result.returncode == 0:
        print("jupyter nbconvert call returned with non-zero error code, aborting.")
        exit(1)


def _move_nbconvert_output(path_notebook, post_path_dir, post_filename, asset_path_dir):
    shutil.move(path_notebook.parent / (path_notebook.stem + ".md"), post_path_dir / post_filename)
    shutil.move(path_notebook.parent / (path_notebook.stem + "_files"), asset_path_dir)


def _rewrite_png_links(post_path, asset_path_dir):
    to_replace = path_notebook.stem + "_files"

    with open(post_path, "r") as f:
        contents = f.read()

    contents = contents.replace(to_replace, "/" + IMG_PATH)

    with open(post_path, "w") as f:
        f.write(contents)


@click.command()
@click.argument("path_notebook", nargs=1, type=click.Path(exists=True))
def main(path_notebook):
    path_notebook = Path(path_notebook)
    if path_notebook.suffixes != [".ipynb"]:
        raise ValueError("Must pass .ipynb file")
    post_filename = path_notebook.parent.name + ".md"

    post_path_dir, asset_path_dir = _create_destination_dirs(path_notebook.parent)

    _run_jupyter_nbconvert(path_notebook)

    _move_nbconvert_output(path_notebook, post_path_dir, post_filename, asset_path_dir)

    _rewrite_png_links(post_path_dir / post_filename, asset_path_dir)

if __name__ == "__main__":
    main()
