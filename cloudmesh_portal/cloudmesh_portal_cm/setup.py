import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-cloudmesh-portal-cm',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    license='Apache 2.0 License',
    description='A Django app to interact with multiple clouds.',
    long_description=README,
    url='https://www.example.com/',
    author='Gregor von Laszewski',
    author_email='laszewski@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8.14',  
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 2.7.12',
        #'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
