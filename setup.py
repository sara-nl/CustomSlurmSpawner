from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="customslurmspawner",
    version="0.1",
    author="Caspar van Leeuwen",
    author_email="caspar.vanleeuwen@surfsara.nl",
    description="This package provides a fully customizable SLURM spawner for Jupyterhub by deriving from batchspawner.SlurmSpawner and implementing an options_form.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sara-nl/CustomSlurmSpawner",
    packages=['customslurmspawner'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPLv3 License",
        "Operating System :: OS Independent",
    ],
    python_requires='~=3.3',
    install_requires=[
        'batchspawner>=0.8.1',
        'jinja2',
        'textwrap',
        'subprocess',
    ],
)
