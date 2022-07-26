import argparse

import cerberus
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
    'MMCV', 'MMClassification', 'MMDetection', 'MMDetection3D', 'MMRotate',
    'MMSegmentation', 'MMOCR', 'MMPose', 'MMHuman3D', 'MMSelfSup', 'MMRazor',
    'MMFewShot', 'MMAction2', 'MMTracking', 'MMFlow', 'MMEditing',
    'MMGeneration', 'MMDeploy'
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
    rev = 0

    # read the data in yaml
    f = open(input_files, 'r')
    projects = yaml.safe_load(f)
    for one_project in projects:
        validity_check(one_project)

    return rev


def repo_url_check(field, value, error):
    """Check the validity of repo_url."""
    valid_flag = value.startswith('https://github.com/') or \
        value.startswith('https://gitee.com/') or \
        value.startswith('https://gitlab.com/')
    if not valid_flag:
        error(
            field, 'repo_url is invalid, must start with one of '
            '[https://github.com/, https://gitee.com/, https://gitlab.com/]')


def paper_url_check(field, value, error):
    """Check the validity of paper_url."""
    valid_flag = True if not value else value.startswith('https://') or \
        value.startswith('http://')
    if not valid_flag:
        error(
            field, 'paper_url is invalid,  must starts '
            'with https:// or http://, or leave for empty')


def tag_check(field, value, error):
    """Check the validity of tag."""
    # check number of tags
    if len(value) > 5:
        error(
            field, 'Please use no more than 5 tags,'
            'current number: {}'.format(len(value)))
    # check string validity
    valid_flag = True
    for tag in value:
        if ',' in tag:
            valid_flag = False
    if not valid_flag:
        error(field, ' \',\' is not allowed used in tag')


def validity_check(project_info: dict) -> int:
    """Check the validity of one project."""
    ecosystem_schema = {
        'repo_url': {
            'type': 'string',
            'required': True,
            'check_with': repo_url_check
        },
        'paper_url': {
            'type': 'string',
            'required': True,
            'empty': True,  # allow to be ''
            'check_with': paper_url_check
        },
        'type': {
            'type': 'string',
            'allowed': VALID_TYPE,
            'required': True,
        },
        'mmrepos': {
            'type': 'list',
            'allowed': VALID_MMREPOS,
            'required': True,
        },
        'tags': {
            'type': 'list',
            'required': True,
            'check_with': tag_check
        },
        'summary': {
            'type': 'dict',
            'required': True,
            'schema': {
                'zh': {
                    'type': 'string',
                    'required': True
                },
                'en': {
                    'type': 'string',
                    'required': True
                }
            }
        }
    }
    validator = cerberus.Validator()
    assert validator.validate(project_info,
                              ecosystem_schema), validator._errors


def main():
    args = parse_args()
    return check_ecosystem_validity(args.input_files[0])


if __name__ == '__main__':
    raise SystemExit(main())
