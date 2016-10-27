from setuptools import find_packages, setup


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
        'cotidia.account': [
            'templates/admin/account/*.html',
            'templates/admin/includes/*.html',
            'templates/account/*.html',
            'templates/account/notices/*.html',
            'templates/account/notices/*.txt',
        ]
    },
    namespace_packages=['cotidia'],
    include_package_data=True,
    install_requires=[
        'django>=1.10.2',
        'djangorestframework>=3.5.1',
    ],
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
    ],
)
