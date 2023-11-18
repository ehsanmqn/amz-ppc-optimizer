from setuptools import setup, find_packages

setup(
    name='amz-ppc-optimizer',
    version='0.1.8',
    description='Python package for optimizing Amazon advertising campaigns',
    author='Ehsan Maiqani',
    author_email='ehsan.maiqani@gmail.com',
    packages=find_packages(),
    install_requires=[
        'pandas==2.0.4',
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ehsanmqn/amz-ppc-optimizer',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
