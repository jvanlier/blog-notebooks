# Jupyter Notebooks for my blog

This repo contains the notebooks for my [blog](https://jvlanalytics.nl/blog). 

Each directory is supposed to be fully self-contained, ideally with a requirements.txt file in order to be able to reproduce environments easily. There should be one `.ipynb` file containing the actual post (code + markdown). The other files aren't used.

A simple Python script on the root of the repo converts the post and images to a format that can be consumed by jekyll.

Some conventions:
- Name of markdown filename (and thus link) = name of directory. The notebook filename can be whatever.
- Dir should contain a file called `meta.txt` with content: 

```
title: "My post"
date: yyyy-MM-dd hh:mm:ss +02:00
math: true  # or false
```

- Output:
    - `<post-name>.md` goes into `_output/_post/`
    - Assets go into `_output/assets/blog/<post-name>`

Just copy each of these to the root of the blog and you should be fine. Don't make changes in the `.md` file, make them in the Notebook and export again.

Tool usage:
	
	python nb-to-blog.py awesome-blog-post/notebook.ipynb

This will produce files:

	_output/blog/awesome-blog-post.md
	_output/assets/awesome-blog-post/1.png
	_output/assets/awesome-blog-post/2.png
	...

