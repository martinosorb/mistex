from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="mistex",  # Replace with your own username
    version="0.0.1",
    author='Martino Sorbaro',
    author_email='martino.sorbaro@posteo.net',
    description="A markdown and latex blender",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/martinosorb/mistex",
    packages=["mistex", "mistex.plugins"],
    classifiers=[
        "Programming Language :: Python :: 3",
        # "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    tests_require=['pytest-cov'],
    install_requires=['mistune>=2.0.*'],
)
