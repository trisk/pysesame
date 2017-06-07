"""
Python API for Sesame smart locks.
"""

from setuptools import setup, find_packages

long_description = open('README.rst').read()

setup(
    name='pysesame',
    version='0.1.0',
    license='MIT',
    url='https://github.com/trisk/pysesame',
    author='Albert Lee',
    author_email='trisk@forkgnu.org',
    description='Python API for Sesame smart locks',
    long_description=long_description,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    platforms='any',
    install_requires=list(val.strip() for val in open('requirements.txt')),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Home Automation',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
)
