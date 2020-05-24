from deployer.deploy import deploy

from argparse import ArgumentParser


def run():
    parser = ArgumentParser()
    parser.add_argument('-c', '--clone_url')
    parser.add_argument('-a', '--app_name')
    parser.add_argument('-s', '--server_names')
    parser.add_argument('-t', '--app_type')
    parser.add_argument('-r', '--runnable', required=False)
    args = parser.parse_args()

    args.server_names = args.server_names.split(',')

    deploy(
        args.runnable,
        args.app_name,
        [args.server_names] if not type(args.server_names) == list
            else args.server_names,
        args.app_type
    )
