import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='nts-skazazes',
    version='0.0.17',
    author='Sean Kazazes',
    author_email='sean@skazazes.com',
    description=('Use the Twitter Application API '
                 'and Neo4J to build a graph of tweets'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/skazazes/Neo4j-TwitterAPI-Streamer',
    packages=setuptools.find_packages(),
    install_requires=['tweepy', 'py2neo'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent'
    ],
)
