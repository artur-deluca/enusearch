from setuptools import find_packages, setup

dev_requires = [
    "pylint",
    "flake8"
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="enusearch",
    packages=find_packages(),
    version="v0.0.1",
    author="Artur de Luca",
    author_email="arturbackdeluca@gmail.com",
    description="A collection of enumerative search algorithms in Python for combinatorial optimization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/artur-deluca/enusearch",
    include_package_data=True,

    extras_require={
        "dev": dev_requires
    },

    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering"

    ]
)
