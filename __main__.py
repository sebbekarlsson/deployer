from deployer.deploy import deploy


#deploy(
#    'git@github.com:sebbekarlsson/locsearch.git',
#    'locsearch',
#    ['loc.dev'],
#    'python'
#)

#deploy(
#    'git@github.com:sebbekarlsson/ianertson.git',
#    'ianertson',
#    ['ianertson.dev'],
#    None
#)

deploy(
    'git@github.com:sebbekarlsson/nofice_website.git',
    'nofice',
    ['nofice.dev'],
    'python'
)
