import setuptools

import versioneer

dependencies = ["pydantic", "sqlalchemy"]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ostanes",  # Replace with your own username
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="Bob Fang",
    author_email="Bob.Fang.London@gmail.com",
    description="A package for unit testing sqlalchemy modules",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bobfang1992/ostanes",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=dependencies,
    extras_require={"dev": ["black", "isort", "flake8", "pre-commit", "pytest"]},
)
