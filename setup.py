from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in arabic_pro/__init__.py
from arabic_pro import __version__ as version

setup(
	name="arabic_pro",
	version=version,
	description="Comprehensive Arabic translation and UI fixes for ERPNext 16.",
	author="Antigravity",
	author_email="info@example.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
