import argparse

import yaml

VALID_TYPE = [
    'Official Implementation',
    'Community Implementation',
    'Competition',
    'Library',
    'Service',
    'Tutorial',
    'Demo',
    'Others',
]

VALID_MMREPOS = [
    'mmcv', 'mmclassification', 'mmdetection', 'mmdetection3d', 'mmrotate',
    'mmsegmentation', 'mmocr', 'mmpose', 'mmhuman3d', 'mmselfsup', 'mmrazor',
    'mmfewshot', 'mmaction2', 'mmtracking', 'mmflow', 'mmediting',
    'mmgeneration', 'mmdeploy'
]


def parse_args():
    parser = argparse.ArgumentParser(
        description='Check the validity of the key in ecosystem information')
    parser.add_argument(
        'input_files', type=str, nargs='+', help='path of the yaml file')

    args = parser.parse_args()
    return args


def check_ecosystem_validity(input_files: str) -> int:
    """Check the validity of the key-value in the ecosystem project yaml.

    Args:
        input_files: Path of the ecoystem project information

    Returns:
        Return 0 if there exists invalid key or value, otherwise return 1.
    """
    rev = 1

    # read the data in yaml
    f = open(input_files, 'r')
    projects = yaml.safe_load(f)
    for one_project in projects:
        validity_check(one_project)

    return rev


def validity_check(project_info: dict) -> int:
    """Check the validity of one project."""
    # parsing the each key-value
    repo_url = project_info['repo_url']
    paper_url = project_info['paper_url']
    type = project_info['type']
    mmrepos = project_info['mmrepos']
    tags = project_info['tags']
    summary = project_info['summary']

    # check validity

    # check repo url
    assert repo_url.startswith('https://github.com/') or repo_url.startswith(
        'https://gitee.com/'), 'repo_url is invalid'

    # check paper url
    if paper_url is None:
        pass
    else:
        assert paper_url.startswith('https://') or paper_url.startswith(
            'http://'), 'paper_url is invalid'

    # check type
    assert type in VALID_TYPE, 'type: {} is invalid, must be one of \
    {}'.format(type, VALID_TYPE)

    # check mmrepos
    for item in mmrepos:
        assert item in VALID_MMREPOS, '{} is invalid, must be one of \
        {}'.format(item, VALID_MMREPOS)

    # check tags
    for tag in tags:
        assert ',' not in tag
        assert tag is not None

    # check summary
    assert len(
        summary) == 2 and 'en' in summary.keys() and 'zh' in summary.keys()


def main():
    args = parse_args()
    return check_ecosystem_validity(args.input_files)


if __name__ == '__main__':
    raise SystemExit(main())
