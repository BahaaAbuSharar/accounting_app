from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in accounting_app/__init__.py
from accounting_app import __version__ as version

setup(
	name="accounting_app",
	version=version,
	description="accounting",
	author="Bahaa",
	author_email="baha13667@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
