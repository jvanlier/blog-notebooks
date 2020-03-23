# Jupyter Notebooks for my blog

This repo contains the notebooks for my [blog](https://jvlanalytics.nl/blog). 

Each directory is supposed to be fully self-contained, ideally with a requirements.txt file in order to be able to reproduce environments easily. There should be one .ipynb file containing the actual post (code + markdown). The other files aren't used.

A simple Python script on the root of the repo converts the post + images to a format that can be consumed by jekyll.

Some conventions:
- Name of dir = name of post. ipynb filename can be whatever.
- Dir should contain a file called `meta.yaml` with `date: yyyy-MM-dd hh:mm:ss +02:00`.
- Output:
    - `<post-name>.md` goes into `_output/_post/`
    - Assets go into `_output/assets/blog/<post-name>`
