import os
from setuptools import setup, find_packages

# Read README if it exists
readme = ""
if os.path.exists("README.md"):
    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()

setup(
    name="theme_switcher",
    version="2.3.0",
    packages=find_packages(),
    package_data={"theme_switcher": ["themes/*.css"]},
    install_requires=[
        "streamlit>=1.45.0",
    ],
    author="drushlopez.dev",
    author_email="drushlopez.dev@gmail.com",
    description="Streamlit theme switcher utility",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/theme-switcher",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.10",
)