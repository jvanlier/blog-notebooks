from setuptools import find_packages, setup

setup(
    name="nb-to-blog",
    version="0.0.1",
    description="NB-to-Jekyll-Blog",
    author="Jori van Lier",
    long_description=long_description,
    author_email="jori@jvlanalytics.nl",
    packages=find_packages(exclude=("tests/",)),
    install_requires=[
        "click>=7.*.*",
        "pyyaml>=5.*.*",
        "jupyter>=1.0.*"
    ]
)
