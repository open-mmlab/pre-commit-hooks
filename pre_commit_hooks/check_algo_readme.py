import argparse
import os.path as osp
import pprint
import re
from typing import Tuple

import yaml

type_matcher = r'.*<!-- \[ALGORITHM\] -->.*'
type_pattern = re.compile(type_matcher)

abstract_start_matcher = r'^## Abstract$'
abstract_start_pattern = re.compile(abstract_start_matcher)

skip_matcher = r'^## .*'
skip_pattern = re.compile(skip_matcher)


def extract_abstract(readme_path: str) -> Tuple[str, str]:
    """Check algorithm type and abstract.

    It will traverse the readme document and match by line. If all matched, it
    will jump out of traversal.
    """

    algorithm_type = False
    abstract = ''

    abstract_found = False
    # only search abstract under the heading of `## Abstract`, ignore other headings.
    skip_abstract_search = False
    if osp.exists(readme_path):
        with open(readme_path, encoding='utf-8') as f:
            for line in f:
                if algorithm_type and (abstract or skip_abstract_search):
                    break

                if not algorithm_type and type_pattern.match(line):
                    algorithm_type = True

                if skip_abstract_search:
                    continue

                if abstract_found:
                    if skip_pattern.match(line):
                        skip_abstract_search = True
                    elif not abstract and not line.strip(
                    ) == '' and not line.startswith('<!--'):
                        abstract = line
                elif abstract_start_pattern.match(line):
                    abstract_found = True

    if not algorithm_type:
        print('Failed to find "<!-- [ALGORITHM] -->" flag from readme, '
              f'please check {readme_path} again.')

    if not abstract:
        print('Failed to extract abstract field from readme, '
              f'please check {readme_path} again.')

    return abstract, algorithm_type


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
                collection = meta_file_data.get('Collections')
                if collection:
                    collections.extend(collection)

            # set return code
            if meta_file_data is None:
                retv = 1

    for collection in collections:
        name = collection.get('Name')
        display_name = handle_collection_name(name)

        readme_path = full_filepath(collection.get('README'), model_index_path)
        abstract, algorithm_type = extract_abstract(readme_path)

        if not abstract or not algorithm_type:
            retv = 1

        if debug:
            pprint.pprint({
                'name': display_name,
                'readmePath': readme_path,
                'abstract': abstract,
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
