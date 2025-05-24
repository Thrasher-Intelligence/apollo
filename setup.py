from setuptools import setup, find_packages

setup(
    name="apollo-deps",
    version="0.1.0",
    description="Python Dependency Analyzer with Interactive Directory Selection",
    author="Jacob Eaker",
    author_email="jacob.eaker@gmail.com",
    url="https://github.com/thrasher-intelligence/apollo",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'apollo=apollo.main:main',
        ],
    },
    install_requires=[
        'blessed>=1.19.0',
        'argparse>=1.4.0',
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.6",
)
