import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="larousse-api",
    version="0.0.1",
    author="Hugo Ferreira",
    author_email="hugoferreirapro803@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hugo291/larousse_api",
    packages=setuptools.find_packages(),
    install_requires=[
        "requests>=2.22.0",
        "bs4>=0.0.1",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
