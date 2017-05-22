import os

from setuptools import find_packages, setup


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

template_files = package_files('cotidia/account/templates')

setup(
    name="cotidia-account",
    description="Account management and API for Cotidia base project.",
    version="1.0",
    author="Guillaume Piot",
    author_email="guillaume@cotidia.com",
    url="https://code.cotidia.com/cotidia/account/",
    packages=find_packages(),
    package_dir={'account': 'account'},
    package_data={
        'cotidia.account': template_files
    },
    namespace_packages=['cotidia'],
    include_package_data=True,
    install_requires=[
        'django>=1.10.2',
        'djangorestframework>=3.5.1',
        'django-two-factor-auth>=1.4.0',
        'django-appconf>=1.0.2'
    ],
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
    ],
)
