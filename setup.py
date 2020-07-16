import setuptools

setuptools.setup(
    name='igloo-python',
    packages=['igloo', 'igloo.models'],
    version='1.0.3',
    license='MIT',
    description='Python client for igloo',
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
