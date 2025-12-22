from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="faosim",
    version="0.1.0",
    author="FAO-Sim Team",
    description="FB Ads Autonomous Optimization & Simulation Lab",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "langchain>=0.1.0",
        "chromadb>=0.4.22",
        "timesfm>=1.0.0",
        "pydantic>=2.0.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "deap>=1.4.0",
        "loguru>=0.7.0",
    ],
    entry_points={
        "console_scripts": [
            "faosim=faosim.cli:main",
        ],
    },
)
