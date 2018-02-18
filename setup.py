#!/usr/bin/env python

import setuptools

setuptools.setup(
    name='shibboleth_session',
    version='0.1.0',
    python_requires='>=3.5',
    author='Sachi King',
    author_email='shib_sess@nakato.nakato.io',
    description=('A wrapper around python-requests sessions to perform the '
                 'required authentication workflow'),
    license='BSD',
    install_requires=['requests'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
    ],
)
