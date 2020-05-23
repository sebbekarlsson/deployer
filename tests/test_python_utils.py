from deployer.python_utils import get_python_bin


def test_get_python_bin():
    binfile = get_python_bin()

    assert binfile
