from setuptools import setup, find_packages

with open('README.rst') as tmp_file:
    readme = tmp_file.read()

with open('LICENSE') as tmp_file:
    license = tmp_file.read()

setup(
    name='TBR Tenshi',
    version='0.1.0dev',
    description='TBR Tenshi is a bot written by mongoishere for managing the TBR Discord Server',
    long_description=readme,
    author='Trevor Medina',
    url='https://github.com/mongoishere/new_pyproject',
    license=license,
    packages=find_packages(exclude=(
        'docs',
        'tests',
        '.vscode'
    ))
)