import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='nts-skazazes',
    version='0.0.1',
    author='Sean Kazazes',
    author_email='sean@skazazes.com',
    description=('Use the Twitter Application API '
                 'and Neo4J to build a graph of tweets'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/skazazes/Neo4j-TwitterAPI-Streamer',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3.6.7',
        'License :: OSI Approved :: GNU GPL v3.0',
        'Operating System :: OS Independant'
    ],
)
