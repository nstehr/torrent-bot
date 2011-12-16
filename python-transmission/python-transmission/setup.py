
from setuptools import setup, find_packages

setup(
    name = "transmissionClient",
    version = "0.5",
    packages= ['transmissionClient'],
    author = "lesion",
    author_email = "lesion@autistici.org",
    description = "Python bindings for the Transmission 1.33 BitTorrent Client",
    license = "GPL2",
    keywords = "bittorrent transmission",
    url = "http://lesion.noblogs.org/",
    zip_safe = True,
    long_description = """ python-transmission module is a ''Python API'' to manage the Transmission BitTorrent Client through its JSONRPC interface """,
    classifiers=["Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GPL2",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Communications :: File Sharing",
    ],
)
