import os
from distutils.core import setup
from setuptools import find_packages


VERSION = __import__("account").VERSION

CLASSIFIERS = [
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Topic :: Software Development',
]

install_requires = [
    'Django>=1.10.2',
    'djangorestframework>=3.5.1',
]

# taken from django-registration
# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir:
    os.chdir(root_dir)

for dirpath, dirnames, filenames in os.walk('account'):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'):
            del dirnames[i]
    if '__init__.py' in filenames:
        pkg = dirpath.replace(os.path.sep, '.')
        if os.path.altsep:
            pkg = pkg.replace(os.path.altsep, '.')
        packages.append(pkg)
    elif filenames:

        #######################################################################
        # !!! IMPORTANT !!!                                                   #
        # To get the right prefix, enter the index key of the same            #
        # value as the length of your package folder name,                    #
        # including the slash.                                                #
        # Eg: for 'account/'' , key will be 4                                 #
        #######################################################################

        prefix = dirpath[4:]  # Strip "account/" or "account\"
        for f in filenames:
            data_files.append(os.path.join(prefix, f))

setup(
    name="cotidia-account",
    description="Account management and API for Cotidia base project.",
    version=VERSION,
    author="Guillaume Piot",
    author_email="guillaume@cotidia.com",
    url="https://code.cotidia.com/cotidia/account",
    package_dir={'account': 'account'},
    packages=packages,
    package_data={'account': data_files},
    include_package_data=True,
    install_requires=install_requires,
    classifiers=CLASSIFIERS,
)
