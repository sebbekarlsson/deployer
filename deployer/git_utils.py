import git
import os


def clone(url, path):
    if os.path.isdir(path):
        os.rmdir(path)

    git_ssh_identity_file = os.path.expanduser('~/.ssh/id_rsa')
    git_ssh_cmd = 'ssh -i %s' % git_ssh_identity_file

    with git.Git().custom_environment(GIT_SSH_COMMAND=git_ssh_cmd):
        git.Repo.clone_from(url, path, branch='master')


def pull(path):
    g = git.cmd.Git(path)
    g.pull()
