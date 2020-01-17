import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="customslurmspawner",
    version="0.1",
    author="Caspar van Leeuwen",
    author_email="caspar.vanleeuwen@surfsara.nl",
    description="This package provides a fully customizable SLURM spawner for Jupyterhub by deriving from batchspawner.SlurmSpawner and implementing an options_form.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sara-nl/CustomSlurmSpawner",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPLv3 License",
        "Operating System :: OS Independent",
    ],
    python_requires='~=3.3',
)
