import os

from setuptools import find_packages, setup


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        # Only keep the last directory of the path
        path = path.replace(directory, directory.split("/")[-1])
        for filename in filenames:
            paths.append(os.path.join(path, filename))
    return paths


template_files = package_files("cotidia/account/templates")

setup(
    name="cotidia-account",
    description="Account management and API for Cotidia base project.",
    version="1.0",
    author="Guillaume Piot",
    author_email="guillaume@cotidia.com",
    url="https://code.cotidia.com/cotidia/account/",
    packages=find_packages(),
    package_dir={"account": "account"},
    package_data={"cotidia.account": template_files},
    namespace_packages=["cotidia"],
    include_package_data=True,
    install_requires=[
        "django==2.1.*",
        "djangorestframework==3.8.*",
        "django-two-factor-auth==1.7.*",
        "django-appconf==1.0.*",
        "django-formtools==2.1.*",
        "django-cors-headers==2.4.*",
        "django-storages==1.7.*",
        "raven==6.10.*",
    ],
    classifiers=[
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
    ],
)
