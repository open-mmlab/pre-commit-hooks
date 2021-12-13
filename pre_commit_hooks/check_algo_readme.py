#!/usr/bin/env python3

import argparse
import os.path as osp
import pprint
import re
from typing import Tuple

import yaml

abstract_start_matcher = r'.*\[ABSTRACT\].*'
abstract_start_pattern = re.compile(abstract_start_matcher)

icon_start_matcher = r'.*\[IMAGE\].*'
icon_start_pattern = re.compile(icon_start_matcher)
src_matcher = r'.*src=.*'
src_line_pattern = re.compile(src_matcher)
src_link_pattern = re.compile(r"\".*?\"")


def extract_readme(readme_path: str) -> Tuple[str, str]:
    abstract = ''
    image = ''

    abstract_start_search = False
    image_start_search = False
    if osp.exists(readme_path):
        with open(readme_path, encoding='utf-8') as file:
            line = file.readline()
            while line:
                # extract abstract
                if abstract_start_search and not abstract:
                    if not line.strip() == '':
                        abstract = line
                if not abstract_start_search:
                    abstract_start_search = abstract_start_pattern.match(line)

                # extract image
                if image_start_search and not image:
                    src_group = src_line_pattern.search(line)
                    if src_group:
                        link_group = src_link_pattern.search(src_group.group())
                        if link_group:
                            image = link_group.group()[1:-1]
                if not image_start_search:
                    image_start_search = icon_start_pattern.match(line)
                line = file.readline()

    if not abstract:
        print('Failed to extract abstract field from readme, '
              f'please check {readme_path} again.')

    if not image:
        print('Failed to extract image field from readme, '
              f'please check {readme_path} again.')

    return abstract, image


def handle_collection_name(name: str) -> str:
    # handler for mmpose
    display_name_pattern = re.compile(r'\[(.*?)\]')
    display_name = re.findall(display_name_pattern, name)
    if display_name:
        name = display_name[0]

    return name


def full_filepath(path: str, cur_filepath: str = None) -> str:
    if cur_filepath is not None:
        dirname = osp.dirname(cur_filepath)
        if dirname:
            path = osp.join(dirname, path)

    return path


def load_any_file(path: str):

    if not osp.exists(path):
        print(f'File "{path}" does not exist.')
        return None

    with open(path, 'r') as f:
        raw = yaml.load(f, Loader=yaml.SafeLoader)

    return raw


def check_algorithm(model_index_path: str = 'model-index.yml',
                    debug: bool = False) -> int:

    retv = 0

    # load collections
    model_index_data = load_any_file(model_index_path)

    # make sure the input is a dict
    if model_index_data is None or not isinstance(model_index_data, dict):
        print(f"Expected the file '{model_index_path}' to contain a dict, "
              "but it doesn't.")
        collections = []
        retv = 1
    else:
        import_files = model_index_data.get('Import')

        collections = []
        for import_file in import_files:
            import_file = full_filepath(import_file, model_index_path)
            meta_file_data = load_any_file(import_file)
            if meta_file_data:
                col = meta_file_data.get('Collections')
                collections.extend(col)

            # set return code
            if meta_file_data is None:
                retv = 1

    for collection in collections:
        name = collection.get('Name')
        display_name = handle_collection_name(name)

        readme_path = full_filepath(collection.get('README'), model_index_path)
        abstract, image = extract_readme(readme_path)

        if not abstract or not image:
            retv = 1

        if debug:
            pprint.pprint({
                'name': display_name,
                'readmePath': readme_path,
                'introduction': abstract,
                'image': image,
            })

    return retv


def main():
    parser = argparse.ArgumentParser(description='Check algorithm readme')
    parser.add_argument(
        '--model-index',
        default='model-index.yml',
        help='model-index file path')
    parser.add_argument('--dry-run', action='store_true', help='Just dry run')
    parser.add_argument(
        '--debug', action='store_true', help='Print debug info')
    args = parser.parse_args()

    retv = check_algorithm(args.model_index, args.debug)

    if args.dry_run:
        return 0

    return retv


if __name__ == '__main__':
    raise SystemExit(main())
