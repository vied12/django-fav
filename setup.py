import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-fav',
    version='0.2',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    description='A simple reusable app for django that makes it easy to deal with faving and unfaving any object from any application.',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://vied12.github.io',
    author='Edouard Richard',
    author_email='edou4rd@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
