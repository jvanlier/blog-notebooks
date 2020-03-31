# Jupyter Notebooks for my blog

This repo contains the notebooks for my [blog](https://jvlanalytics.nl/blog). 

Each directory is supposed to be fully self-contained, ideally with a requirements.txt file in order to be able to reproduce environments easily. There should be one `.ipynb` file containing the actual post (code + markdown). There may also be other `.py/.ipynb` files, but they aren't used to render the blog.

Self-contained also means that data will be part of the repo if it's small (and not confidential). If it's too large and unreasonably blows up the repo: place it on online storage and include a script to acquire the data. The subdir `README.md` should contain all necessary instructions to reproduce the result.

A simple Python script on the root of the repo converts the post and images to a format that can be consumed by Jekyll.

Conventions:
- Name of resulting markdown filename (and thus link in Jekyll) = name of directory. The notebook filename can be whatever. Let's assume the directory is called `awesome-blog-post`. 
- First cell of Notebook contains the Jekyll header in Raw NBConvert, e.g.:

```
---
layout: post
title:  "Awesome Blog Post"
date:   2020-03-31 14:00:00 +0200
categories: blog
math: true
---
```

Tool usage:
	
	python nb-to-blog.py awesome-blog-post/post.ipynb

Output:

	_output/_post/awesome-blog-post.md
	_output/assets/img/blog/awesome-blog-post/<jupyter-nbconvert-autogenerated-filename>.png
	... 

Just copy each of these to the root of the blog and you should be fine. Don't make changes in the `.md` file, make them in the Notebook and export again.

