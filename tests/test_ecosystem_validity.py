from pre_commit_hooks.check_ecosystem_validity import check_ecosystem_validity


def test_ecosystem_validity():
    filenames = './tests/test-ecosystem-validity.yaml'
    assert check_ecosystem_validity(filenames) == 1
