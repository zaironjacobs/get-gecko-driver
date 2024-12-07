from setuptools import setup
from setuptools import find_packages

name = "get-gecko-driver"
version = "1.4"

with open("README.md", "r") as fh:
    long_description = fh.read()

requires = ["beautifulsoup4==4.12.3", "requests==2.32.3", "urllib3==2.2.3", "typer==0.15.1"]

setup(
    name=name,
    version=version,
    author="Zairon Jacobs",
    author_email="zaironjacobs@gmail.com",
    description="A tool to download and install GeckoDriver.",
    long_description=long_description,
    url="https://github.com/zaironjacobs/get-gecko-driver",
    download_url=f"https://github.com/zaironjacobs/get-gecko-driver/archive/v{version}.tar.gz",
    keywords=["gecko", "geckodriver", "download", "install", "web", "driver", "tool"],
    packages=find_packages(),
    entry_points={
        "console_scripts": [f"{name}=get_gecko_driver.app:app"],
    },
    install_requires=requires,
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.11",
        "Natural Language :: English",
    ],
    python_requires=">=3",
)
