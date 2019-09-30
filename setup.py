from setuptools import setup, find_packages

setup(
    name='thunderdb',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'requests',
        'bottle',
        'waitress'
    ],
    entry_points={
        'console_scripts': [
            'thunderdb = thunderdb.thunderdb:main',
        ],
    },
    zip_safe=False,
)
