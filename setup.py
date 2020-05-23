from setuptools import setup, find_packages


setup(
    name='deployer',
    version='1.0.0',
    install_requires=[
        'requests',
        'pytest',
        'jinja2',
        'gitpython'
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
        ]
    }
)
