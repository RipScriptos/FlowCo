"""Setup script for FlowCo."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

# Read requirements
requirements_path = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_path.exists():
    requirements = requirements_path.read_text().strip().split('\n')
    requirements = [req.strip() for req in requirements if req.strip() and not req.startswith('#')]

setup(
    name="flowco",
    version="1.0.0",
    description="AI Business Success Evaluation System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="FlowCo Team",
    author_email="info@flowco.ai",
    url="https://github.com/RipScriptos/FlowCo",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords="ai, business, evaluation, analysis, machine learning, entrepreneurship",
    entry_points={
        "console_scripts": [
            "flowco=main:main",
        ],
    },
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-asyncio>=0.21.1",
            "black>=23.11.0",
            "flake8>=6.1.0",
            "pytest-cov>=4.1.0",
        ],
    },
)