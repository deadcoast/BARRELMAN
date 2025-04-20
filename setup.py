from setuptools import setup, find_packages

setup(
    name='barrelman-tools',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'bmanlint = bmanlint:main',
            'bmanfmt = bmanfmt:main'
        ]
    },
    author='Barrelman Project',
    description='CLI tooling for the BARRELMAN syntax format',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
    ],
    python_requires='>=3.8',
)
