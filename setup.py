from setuptools import setup, find_packages
import io
import os

__author__ = 'Cedric Zhuang'
__version__ = '0.1.7'


def here(filename=None):
    ret = os.path.abspath(os.path.dirname(__file__))
    if filename is not None:
        ret = os.path.join(ret, filename)
    return ret


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n\n')
    buf = []
    for filename in filenames:
        with io.open(here(filename), encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


def read_requirements(filename):
    with open(filename) as f:
        return f.read().splitlines()


def get_description():
    return ("Utility for retrieving basic China "
            "stock data from different sources.")


def get_long_description():
    filename = 'README.md'
    try:
        import pypandoc
        ret = pypandoc.convert(filename, 'rst')
    except ImportError:
        ret = read(filename)
    return ret


setup(
    name="cn_stock_src",
    version=__version__,
    author="Cedric Zhuang",
    author_email="cedric.zhuang@gmail.com",
    description=get_description(),
    license="BSD",
    keywords="Stock data retriever for China stock market.",
    url="http://github.com/jealous/cn_stock_src",
    include_package_data=True,
    packages=find_packages(),
    platforms=['any'],
    long_description=get_long_description(),
    classifiers=[
        "Programming Language :: Python",
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    install_requires=read_requirements('requirements.txt'),
    tests_require=read_requirements('test-requirements.txt')
)
