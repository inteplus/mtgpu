#!/usr/bin/env python3

from setuptools import setup, find_namespace_packages
from mt.gpu.version import version

setup(name='mtgpu',
      version=version,
      description="Minh-Tri Pham's approach to detect gpu capacity",
      author=["Minh-Tri Pham"],
      packages=find_namespace_packages(include=['mt.*']),
      install_requires=[
          # 'pynvml', # if you have nvidia gpus, install this package
          # 'rocm-smi', # if you have amdgpu cards, the rocm image should contain this package. Otherwise install it.
      ],
      url='https://github.com/inteplus/mtgpu',
      project_urls={
          'Documentation': 'https://mtdoc.readthedocs.io/en/latest/mt.gpu/mt.gpu.html',
          'Source Code': 'https://github.com/inteplus/mtgpu',
          }
      )
