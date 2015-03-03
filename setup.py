from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='activitywatch',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/development.html#single-sourcing-the-version
    version='0.1.0',

    description='Logs all your computer activities',
    long_description="For more, see the README.",

    # The project's main homepage.
    url='https://github.com/ErikBjare/activitywatch',

    # Author details
    author='Erik Bjäreholt',
    author_email='erik@bjareho.lt',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    # What does your project relate to?
    keywords='development quantifiedself zenobase logger',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    package_dir={'': 'src'},
    packages=["activitywatch"],

    # List run-time dependencies here.  These will be installed by pip when your
    # project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/technical.html#install-requires-vs-requirements-files
    install_requires=['psutil', 'pyuserinput', 'pyzenobase', 'python3-xlib'],

    dependency_links=['https://github.com/ErikBjare/pyzenobase/archive/master.zip#egg=pyzenobase',
                      'https://git@github.com/liulang/python3-xlib/archive/master.zip#egg=python3-xlib']
)
