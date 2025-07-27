#!/usr/bin/env python3
"""
Setup script for Vader - Lenguaje de Programación Universal
"""

from setuptools import setup, find_packages
import os

# Read README for long description
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

# Version
__version__ = "2.0.0"

setup(
    name="vader-lang",
    version=__version__,
    author="Vader Development Team",
    author_email="dev@vader-lang.org",
    description="Lenguaje de programación universal y conversacional en español",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/LangVader/core",
    project_urls={
        "Bug Tracker": "https://github.com/LangVader/core/issues",
        "Documentation": "https://vader-lang.org/docs",
        "Source Code": "https://github.com/LangVader/core",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Compilers",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Education",
        "Natural Language :: Spanish",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "pytest-benchmark>=4.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
            "bandit>=1.7.5",
        ],
        "docs": [
            "mkdocs>=1.5.0",
            "mkdocs-material>=9.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "vader=src.vader:main",
            "vader-transpile=src.vader:main",
            "vader-generate=src.app_generator:main",
            "vader-project=src.project_generator:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.yml", "*.yaml", "*.json"],
        "examples": ["*.vdr"],
        "templates": ["*.json", "*.vdr"],
        "docs": ["*.md"],
    },
    keywords=[
        "programming-language",
        "transpiler",
        "spanish",
        "conversational",
        "universal",
        "code-generation",
        "education",
        "democratization",
    ],
    zip_safe=False,
)
