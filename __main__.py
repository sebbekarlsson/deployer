from deployer.deploy import deploy


deploy(
    'git@github.com:sebbekarlsson/locsearch.git',
    'locsearch',
    ['loc.dev'],
    'python'
)
