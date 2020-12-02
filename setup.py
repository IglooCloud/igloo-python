import setuptools

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='igloo-python',
    packages=['igloo', 'igloo.models'],
    version='1.0.13',
    license='MIT',
    description='Python SDK for Igloo',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Igloo Team',
    author_email='hello@igloo.ooo',
    url='https://github.com/IglooCloud/igloo_python',
    keywords=['iot', 'igloo'],
    install_requires=[
        'requests', 'asyncio', 'pathlib', 'websockets', 'aiodataloader', 'aiohttp'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development ',
        'License :: OSI Approved :: MIT License  ',
        'Programming Language :: Python :: 3',
    ],
)
