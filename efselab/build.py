#!/usr/bin/env python3
from distutils.core import setup, Extension

MODULES_TO_BUILD = ["fasthash", "suc", "lemmatize"]

def main():
    for module in MODULES_TO_BUILD:
        setup(
            name=module,
            ext_modules=[
                Extension(
                    name=module,
                    sources=['%s.c' % module],
                    libraries=[],
                    extra_compile_args=['-Wall', '-Wno-unused-function'],
                    extra_link_args=[]
                )
            ],
            script_args=['build_ext', '--inplace']
        )

if __name__ == '__main__':
    main()
