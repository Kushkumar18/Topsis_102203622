from setuptools import setup

setup(
    name='Topsis-Kush-102203622',
    version='0.1.0',
    description='TOPSIS implementation for ranking alternatives',
    author='Kush Kumar',
    author_email='kkumar1_be22@thapar.edu',
    packages=['topsis'],
    install_requires=['pandas', 'numpy'],
    entry_points={
        'console_scripts': [
            'topsis=topsis.topsis:main',
        ],
    },
)
