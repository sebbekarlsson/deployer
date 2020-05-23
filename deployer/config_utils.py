from jinja2 import Environment, PackageLoader, select_autoescape


env = Environment(
    loader=PackageLoader('deployer', 'config_templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

def get_nginx_config(app_name, server_names, app_type):
    return env.get_template('nginx.nginx').render(
        app_name=app_name,
        server_names=server_names,
        app_type=app_type
    )


def get_systemd_config(app_name):
    return env.get_template('systemd.service').render(app_name=app_name)


def get_uwsgi_config(app_name):
    return env.get_template('uwsgi.ini').render(app_name=app_name)
