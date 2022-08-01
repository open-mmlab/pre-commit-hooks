import argparse
import pprint

import cerberus
import yaml

VALID_TYPES = [
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


def check_repo_url(field, value, error):
    """Check the validity of repo_url."""
    valid_urls = ('https://github.com/', 'https://gitee.com/',
                  'https://gitlab.com/')
    valid_flag = value.startswith(valid_urls)
    if not valid_flag:
        error(field,
              f'repo_url is invalid, must start with one of {valid_urls}')


def check_paper_url(field, value, error):
    """Check the validity of paper_url."""
    valid_flag = True if not value else value.startswith('https://') or \
        value.startswith('http://')
    if not valid_flag:
        error(
            field, 'paper_url is invalid,  must starts '
            'with https:// or http://, or leave for empty')


def check_tag(field, value, error):
    """Check the validity of tag."""
    # check number of tags
    if len(value) > 5:
        error(
            field, 'Please use no more than 5 tags,'
            f'current number: {len(value)}')
    # check string validity
    valid_flag = True
    for tag in value:
        if ',' in tag:
            valid_flag = False
    if not valid_flag:
        error(field, "',' is not allowed used in tag")


def check_project_validity(project_info: dict) -> int:
    """Check the validity of one project."""
    ecosystem_schema = {
        'repo_url': {
            'type': 'string',
            'required': True,
            'check_with': check_repo_url
        },
        'paper_url': {
            'type': 'string',
            'required': True,
            'empty': True,  # allow to be ''
            'check_with': check_paper_url
        },
        'type': {
            'type': 'string',
            'allowed': VALID_TYPES,
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
            'check_with': check_tag
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
    retv = validator.validate(project_info, ecosystem_schema)
    if not retv:
        prrint_handle = pprint.PrettyPrinter()
        prrint_handle.pprint(project_info)
        for error in validator._errors:
            print(f'Value of {error.document_path} is {error.value}'
                  f'\n\tconstraint: {error.constraint}\n\trule:{error.info}')
    return retv


def check_ecosystem_validity(filename: str) -> int:
    """Check the validity of the key-value in the ecosystem project yaml.

    Args:
        filename: Path of the ecoystem project information

    Returns:
        Return 0 if all key and value are valid, otherwise return 1.
    """
    retv = 0

    # read the data in yaml
    f = open(filename)
    projects = yaml.safe_load(f)
    # check validity of each project
    for project in projects:
        if not check_project_validity(project):
            retv = 1

    # check with/without repeated projects
    projects_dict = {}
    for idx, project in enumerate(projects):
        curr_repo_url = project['repo_url']
        if not curr_repo_url not in projects_dict.keys():
            retv = 1
            print(f"'{curr_repo_url}' is repeated,"
                  ' please search it and remove the repeated items')
        projects_dict[curr_repo_url] = {'idx': idx}

    return retv


def main():
    parser = argparse.ArgumentParser(
        description='Check the validity of the key in ecosystem information')
    parser.add_argument('filename', type=str, help='path of the yaml file')
    args = parser.parse_args()

    return check_ecosystem_validity(args.filename)


if __name__ == '__main__':
    raise SystemExit(main())
