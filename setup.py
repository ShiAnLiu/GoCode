from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='gocode',
    version='0.1.0',
    description='A code programming tool that automates the entire development process',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/gocode',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests==2.31.0',
        'kivy>=2.3.0',
        'pytest==7.4.3',
        'sphinx==7.2.6',
        'beautifulsoup4==4.12.2',
        'lxml==4.9.3',
        'astor==0.8.1',
        'pycodestyle==2.11.1',
        'pyjwt==2.8.0',
        'platformdirs==4.1.0',
    ],
    entry_points={
        'console_scripts': [
            'gocode = cli.main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
