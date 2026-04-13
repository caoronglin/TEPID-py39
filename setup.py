#!/usr/bin/env python3

from setuptools import setup

import versioneer


INSTALL_REQUIRES = [
    "numpy>=2.0.2,<2.1",
    "pandas>=2.3.3,<3.0",
    "pybedtools>=0.10.0",
    "pysam>=0.22.0",
]


if __name__ == "__main__":
    setup(
        name="TEPID",
        version=versioneer.get_version(),
        cmdclass=versioneer.get_cmdclass(),
        description="TEPID: transposable element polymorphism identification",
        author="Tim Stuart",
        author_email="timstuart90@gmail.com",
        url="https://github.com/ListerLab/TEPID",
        python_requires=">=3.9",
        install_requires=INSTALL_REQUIRES,
        extras_require={
            "dev": ["pytest>=8.0"],
        },
        scripts=[
            "Scripts/tepid-map",
            "Scripts/tepid-map-se",
            "Scripts/tepid-discover",
            "Scripts/tepid-refine",
        ],
        packages=["tepid"],
    )
