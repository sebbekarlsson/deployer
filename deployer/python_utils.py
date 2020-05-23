import subprocess

import logging

import os

from deployer.exceptions import PythonSetupException, BinNotFoundException


def get_python_bin():
    logging.info('Looking for python binary...')

    for binfile in [
        '/usr/bin/python3.7m',
        '/usr/bin/python3.7',
        '/usr/bin/python3.6m',
        '/usr/bin/python3.7',
        '/usr/bin/python3.6m',
        '/usr/bin/python3.6',
        '/usr/bin/python2.7'
    ]:
        if os.path.isfile(binfile):
            return binfile

    raise BinNotFoundException('Could not find a python binary.')


def create_python_venv(basepath):
    logging.info('Creating python virtualenv...')

    binfile = get_python_bin()

    logging.info(f'Using python binary: {binfile}')

    subprocess.Popen(
        f'virtualenv -p {binfile} ' + os.path.join(basepath, './venv'),
        shell=True,
        stdout=subprocess.PIPE
    ).stdout.read()


def run_python_setup(basepath):
    logging.info('Running python setup.py')

    if not os.path.isfile('setup.py'):
        raise PythonSetupException('setup.py not found')

    logging.info(subprocess.Popen(
        f'''
        cd {basepath} 
        ./venv/bin/python setup.py install
        ./venv/bin/python setup.py develop
        ''',
        shell=True,
        stdout=subprocess.PIPE
    ).stdout.read())
