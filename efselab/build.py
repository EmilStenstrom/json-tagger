#!/usr/bin/env python3
from distutils.core import setup, Extension

setup(
    name='fasthash',
    ext_modules=[
        Extension(
            name='fasthash',
            sources=['fasthash.c'],
            libraries=[],
            extra_compile_args=['-Wall'],
            extra_link_args=[]
        )
    ],
    script_args=['build_ext', '--inplace']
)

setup(
    name="suc",
    ext_modules=[
        Extension(
            name="suc",
            sources=["suc.c"],
            libraries=[],
            extra_compile_args=['-Wall', '-Wno-unused-function', '-Ofast', '-g'],
            extra_link_args=[]
        )
    ],
    script_args=['build_ext', '--inplace']
)
