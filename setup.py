from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    description = fh.read()

AUTHOR_NAME = 'Tharindu Sahan'
SRC_REPO = 'src'
LIST_OF_REQUIREMENTS = ['streamlit']


setup(
    name = SRC_REPO,
    version = '0.0.1',
    author = AUTHOR_NAME,
    author_email = 'it21207822@my.sliit.lk',
    description = 'This is movie recommendation system',
    package = [SRC_REPO],
    python_requires = ">=3.7",
    install_requires = LIST_OF_REQUIREMENTS

)