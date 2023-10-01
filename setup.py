from setuptools import setup, find_packages

setup(
    name='Amazon PPC Optimizer',
    version='0.1.0',
    description='Python package for optimizing Amazon advertising campaigns',
    author='Ehsan Maiqani',
    author_email='ehsan.maiqani@gmail.com',
    packages=find_packages(),
    install_requires=[
        'pandas',
    ],
)
