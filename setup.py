import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='bowtie',
    version='0.1.1',
    author='fabiosaracco',
    description='Built upon igraph, bowtie decompose a directed network according to the bow-tie decomposition',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/fabiosaracco/bowtie',
    license='MIT',
    packages=['bowtie'],
    install_request=['numpy', 'datetime', 'igraph', 'tqdm'],
)
