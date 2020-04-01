from setuptools import setup

setup(
    name="nb-to-blog",
    version="0.0.1",
    description="NB-to-Jekyll-Blog",
    author="Jori van Lier",
    author_email="jori@jvlanalytics.nl",
#    packages=["."],
    install_requires=[
        "click>=7.*.*",
        "jupyter>=1.0.*"
    ],
    scripts=["nb-to-blog.py"]
)
