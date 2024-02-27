#!/usr/bin/env python3

import os
from setuptools import setup, find_namespace_packages

VERSION_FILE = os.path.join(os.path.dirname(__file__), "VERSION.txt")

setup(
    name="mtgpu",
    description="Minh-Tri Pham's approach to detect gpu capacity",
    author=["Minh-Tri Pham"],
    packages=find_namespace_packages(include=["mt.*"]),
    scripts=[
        "scripts/detect_machine",
    ],
    install_requires=[
        "psutil",  # for getting cpu memory usage
        "tqdm",  # nice printout
        # 'pynvml', # if you have nvidia gpus, install this package
        # 'rocm-smi', # if you have amdgpu cards, the rocm image should contain this package. Otherwise install it.
    ],
    url="https://github.com/inteplus/mtgpu",
    project_urls={
        "Documentation": "https://mtdoc.readthedocs.io/en/latest/mt.gpu/mt.gpu.html",
        "Source Code": "https://github.com/inteplus/mtgpu",
    },
    setup_requires=["setuptools-git-versioning<2"],
    setuptools_git_versioning={
        "enabled": True,
        "version_file": VERSION_FILE,
        "count_commits_from_version_file": True,
        "template": "{tag}",
        "dev_template": "{tag}.dev{ccount}+{branch}",
        "dirty_template": "{tag}.post{ccount}",
    },
)
