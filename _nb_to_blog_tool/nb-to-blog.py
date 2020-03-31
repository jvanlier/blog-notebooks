#!/usr/bin/env python
from typing import Tuple
from pathlib import Path
import subprocess
import shutil

import click
import yaml


IMG_PATH = "assets/img/blog"


def _create_destination_dirs(notebook_dir: Path) -> Tuple[Path, Path]:
    dest_post_dir = notebook_dir.parent / "_output" / "_posts"
    dest_post_dir.mkdir(parents=True, exist_ok=True)
    dest_asset_dir = notebook_dir.parent / "_output" / IMG_PATH / notebook_dir.name
    dest_asset_dir.parent.mkdir(parents=True, exist_ok=True)
    if dest_asset_dir.exists():
        print(f"Warning: {dest_asset_dir} already exists, aborting.")
        exit(1)

    return dest_post_dir, dest_asset_dir


def _run_jupyter_nbconvert(notebook: Path) -> Tuple[Path, Path]:
    cmd = ["jupyter", "nbconvert", "--to", "markdown", str(notebook)]
    result = subprocess.run(cmd)
    if not result.returncode == 0:
        print("jupyter nbconvert call returned with non-zero error code, aborting.")
        exit(1)
 
    return notebook.parent / (notebook.stem + ".md"), \
           notebook.parent / (notebook.stem + "_files")


def _move_nbconvert_output(nbconvert_md: Path, nbconvert_files_dir: Path, dest_post: Path,
                           dest_asset_dir: Path):
    shutil.move(nbconvert_md, dest_post)
    shutil.move(nbconvert_files_dir, dest_asset_dir)


def _rewrite_png_links(notebook_stem: str, dest_post: Path, dest_asset_dir: Path):
    str_to_replace = notebook_stem + "_files"

    with open(dest_post, "r") as f:
        contents = f.read()

    contents = contents.replace(str_to_replace, "/" + IMG_PATH + "/" + dest_post.stem)

    with open(dest_post, "w") as f:
        f.write(contents)


@click.command()
@click.argument("notebook", nargs=1, type=click.Path(exists=True))
def main(notebook: str):
    notebook = Path(notebook)
    if notebook.suffixes != [".ipynb"]:
        raise ValueError("Must pass .ipynb file")

    dest_post_dir, dest_asset_dir = _create_destination_dirs(notebook.parent)
    # Name of post = name of directory:
    dest_post = dest_post_dir / (notebook.parent.name + ".md")

    nbconvert_md, nbconvert_files_dir = _run_jupyter_nbconvert(notebook)

    _move_nbconvert_output(nbconvert_md, nbconvert_files_dir, dest_post, dest_asset_dir)

    _rewrite_png_links(notebook.stem, dest_post, dest_asset_dir)

if __name__ == "__main__":
    main()
