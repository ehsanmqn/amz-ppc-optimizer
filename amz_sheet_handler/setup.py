from setuptools import setup, find_packages

setup(
    name='Amazon PPC Report Sheets Handler',
    version='0.1.0',
    description='Python package for handling Amazon advertising campaign data',
    author='Ehsan Maiqani',
    author_email='ehsan.maiqani@gmail.com',
    packages=find_packages(),
    install_requires=[
        'pandas',
        # Add any other dependencies here
    ],
)
