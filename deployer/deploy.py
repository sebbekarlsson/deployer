from deployer.git_utils import clone, pull

import deployer.config_utils as config_utils
import deployer.python_utils as python_utils
import deployer.constants as constants

import logging

import os
import subprocess

import shutil
import requests


def raise_if_not_nginx():
    if not os.path.isdir(constants.SERVER_NGINX_AVAIL_PATH)\
            or not os.path.isdir(constants.SERVER_NGINX_ENABLED_PATH):
        raise Exception('Nginx is not installed')


def download_file(url, dest):
    r = requests.get(url, stream=True, allow_redirects=True)

    if r.status_code == 200:
        logging.info(f'Downloading {url} to {dest}...')
        with open(dest, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
    elif r.status_code == 303:
        logging.info('neger')
    else:
        logging.info(f'Could not download {url}')


def deploy(clone_url, app_name, server_names, app_type):
    raise_if_not_nginx()

    app_path = os.path.join(constants.SERVER_APPLICATION_PATH, app_name)

    logging.info('1. Cloning repo')

    if '.zip' in clone_url:
        download_file(clone_url, app_path)
    else:
        if not os.path.isdir(app_path):
            clone(clone_url, app_path)
        else:
            pull(app_path)
    
    logging.info('2. Creatng nginx files')
    open(
        os.path.join(
            constants.SERVER_NGINX_AVAIL_PATH, f'{app_name}.nginx'
        ),
        'w+'
    ).write(config_utils.get_nginx_config(app_name, server_names, app_type))
    subprocess.Popen(
        'ln -s {} {}'.format(
            os.path.join(
                constants.SERVER_NGINX_AVAIL_PATH, f'{app_name}.nginx'
            ),
            os.path.join(
                constants.SERVER_NGINX_ENABLED_PATH, f'{app_name}.nginx'
            )
        ),
        shell=True,
        stdout=subprocess.PIPE
    ).stdout.read()
    
    if app_type == 'python':
        logging.info('3. Creating systemd files')
        open(
            os.path.join(
                constants.SERVER_SYSTEMD_PATH, f'{app_name}.service'
            ),
            'w+'
        ).write(config_utils.get_systemd_config(app_name))
        
        logging.info('4. Creating uwsgi files')
        open(
            os.path.join(
                constants.SERVER_APPLICATION_PATH, app_name, 'uwsgi.ini'
            ),
            'w+'
        ).write(config_utils.get_uwsgi_config(app_name))
    
    logging.info('5. Creating SSL certs')
    logging.info(subprocess.Popen(
        'certbot --nginx --redirect --break-my-certs --register-unsafely-without-email ' + ' '.join(['-d ' + sname for sname in server_names]),
        shell=True,
        stdout=subprocess.PIPE
    ).stdout.read())
    
    if app_type == 'python':
        logging.info('6. Installing')
        python_utils.create_python_venv(app_path)
        python_utils.run_python_setup(app_path)
        
        logging.info('7. Starting services')
        subprocess.Popen('systemctl daemon-reload', shell=True, stdout=subprocess.PIPE).stdout.read()  # NOQA E501
        subprocess.Popen(f'systemctl restart {app_name}.service', shell=True, stdout=subprocess.PIPE).stdout.read()  # NOQA E501

    subprocess.Popen('systemctl reload nginx', shell=True, stdout=subprocess.PIPE).stdout.read()  # NOQA E501

    if app_type == 'python':
        subprocess.Popen(
            'chmod -R 777 {}'.format(
                os.path.join(constants.SERVER_SOCKET_PATH, f'{app_name}.sock')
            ),
            shell=True,
            stdout=subprocess.PIPE
        ).stdout.read()
