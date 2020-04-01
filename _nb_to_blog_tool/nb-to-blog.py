#!/usr/bin/env python
import json
from pathlib import Path
import re
import shutil
import subprocess
from typing import Tuple

import click


IMG_PATH = "assets/img/blog"


def _create_destination_dirs(notebook_dir: Path, post_name: str) -> Tuple[Path, Path]:
    """Create destination directory for post and image assets. Exits if image asset dir already
    exists.
    """
    dest_post_dir = notebook_dir.parent / "_output" / "_posts"
    dest_post_dir.mkdir(parents=True, exist_ok=True)
    dest_asset_dir = notebook_dir.parent / "_output" / IMG_PATH / post_name
    dest_asset_dir.parent.mkdir(parents=True, exist_ok=True)
    if dest_asset_dir.exists():
        print(f"Warning: {dest_asset_dir} already exists, aborting.")
        exit(1)

    return dest_post_dir, dest_asset_dir


def _extract_date_from_ipynb(notebook: Path) -> str:
    """Jekyll requires the date in the prefix of a post filename. Since we have the convention of
    putting it in the first cell of the Notebook, extract it from there.
    """
    with notebook.open("r") as f:
        nb_content = json.load(f)

    first_cell = nb_content["cells"][0]["source"]
    date_line = [l for l in first_cell if l.startswith("date")]
    if not len(date_line) == 1:
        print("Could not find single line with date in first cell")
        exit(1)
    date_line = date_line[0]

    if m := re.match(r"^date:[\s]*([0-9-]*)", date_line):
        date_str = m.group(1)
        print(f"Extracted date string from notebook: {date_str}")
        return m.group(1)
    else:
        print("Could not extract date string from line starting with 'date' in first cell.")
        exit(1)


def _run_jupyter_nbconvert(notebook: Path) -> Tuple[Path, Path]:
    """Launch subprocess to convert notebook to markdown."""
    cmd = ["jupyter", "nbconvert", "--to", "markdown", str(notebook)]
    result = subprocess.run(cmd)
    if not result.returncode == 0:
        print("jupyter nbconvert call returned with non-zero error code, aborting.")
        exit(1)
 
    return notebook.parent / (notebook.stem + ".md"), \
           notebook.parent / (notebook.stem + "_files")


def _move_nbconvert_output(nbconvert_md: Path, nbconvert_files_dir: Path, dest_post: Path,
                           dest_asset_dir: Path):
    """Move output of jupyter nbconvert from its default location to _output in root of repo."""
    shutil.move(nbconvert_md, dest_post)
    shutil.move(nbconvert_files_dir, dest_asset_dir)


def _rewrite_image_refs(notebook_stem: str, dest_post: Path, dest_asset_dir: Path):
    """Rewrite references to images to be compatible with the Jekyll organisation."""
    jekyll_path = "/" + IMG_PATH + "/" + dest_post.stem

    with dest_post.open("r") as f:
        contents = f.read()

    # First, custom images for which we assume that they're placed in "img/". So we match on the partial
    # markdown tag "](img/"
    contents = re.sub(r"\](\(img\/)", "](" + jekyll_path + "/", contents)

    # Next, the embedded images (originally base64 encoded in notebook):
    contents = contents.replace(notebook_stem + "_files", jekyll_path)

    with dest_post.open("w") as f:
        f.write(contents)


def _copy_standalone_images(notebook_dir: Path, dest_asset_dir: Path):
    """Copy standalone images; if any. Convention is that they're placed in a dir called 'img'."""
    img_dir = notebook_dir / "img"
    if img_dir.is_dir():
        for img in img_dir.glob("*"):
            print(f"Including standalone image {img}")
            shutil.copy(img, dest_asset_dir / img.name)


def _sanitize(dest_post: Path):
    """Remove lines from the markdown file that do not add value to blog post. Such as HTML-based `tqdm`
    progress bar boxes, that don't work anyway after conversion. This is currently the only thing that
    gets removed.
    """
    with dest_post.open("r") as f:
        contents = f.read().split("\n")
    
    contents_clean = [line
                      for line in contents
                      if not any(nc in line for nc in {"HBox(children=(FloatProgress"})]

    with dest_post.open("w") as f:
        f.write("\n".join(contents_clean))


@click.command()
@click.argument("notebook", nargs=1, type=click.Path(exists=True))
def main(notebook: str):
    notebook = Path(notebook)
    if notebook.suffixes != [".ipynb"]:
        raise ValueError("Must pass .ipynb file")

    date_str = _extract_date_from_ipynb(notebook)
    post_name = date_str + "-" + notebook.parent.name

    dest_post_dir, dest_asset_dir = _create_destination_dirs(notebook.parent, post_name)
    dest_post = dest_post_dir / (post_name + ".md")

    nbconvert_md, nbconvert_files_dir = _run_jupyter_nbconvert(notebook)

    _move_nbconvert_output(nbconvert_md, nbconvert_files_dir, dest_post, dest_asset_dir)

    _rewrite_image_refs(notebook.stem, dest_post, dest_asset_dir)

    _copy_standalone_images(notebook.parent, dest_asset_dir)

    _sanitize(dest_post)

if __name__ == "__main__":
    main()
