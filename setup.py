import os

from setuptools import find_packages, setup


# Include package data like CSS files
def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        paths.extend(os.path.join('..', path, filename) for filename in filenames)
    return paths

static_files = package_files('src/static')

setup(
    name='barrelman-tools',
    version='1.0.0',
    packages=find_packages(),
    package_dir={'': 'src'},
    package_data={
        'static': static_files,
    },
    include_package_data=True,
    install_requires=[
        'flask',  # For preview_server.py
        'rich',   # For syntax highlighting in terminal
    ],
   entry_points={
       'console_scripts': [
           'barrelman = main:main',
           # If you keep scripts at root level
           'bmanlint = bmanlint:main',  # Assuming you'd also move files to root or add to PYTHONPATH
           'bmanfmt = bmanfmt:main'
       ]
   },
    author='Barrelman Project',
    description='CLI tooling for the BARRELMAN syntax format',
    long_description="""
BARRELMAN SYNTAX PROCESSING SYSTEM

A comprehensive toolset for processing BARRELMAN syntax files,
offering:

- Syntax validation and linting
- Multiple export formats (HTML, Markdown, Graphviz DOT)
- Live preview server with syntax highlighting
- Command-line interface for all operations
""",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: Markup',
        'Framework :: Flask',
    ],
    python_requires='>=3.8',
    project_urls={
        'Documentation': 'https://github.com/username/barrelman/wiki',
        'Source': 'https://github.com/username/barrelman',
    },
)
