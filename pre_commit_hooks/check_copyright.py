import argparse
import os
import os.path as osp
from typing import List

HEADER = 'Copyright (c) OpenMMLab. All rights reserved.\n'

HEADER_KEYWORDS = {'Copyright', 'License'}


def has_copyright(lines: List[str]) -> bool:
    for line in lines:
        if not HEADER_KEYWORDS.isdisjoint(set(line.split(' '))):
            return True
    return False


def parse_args():
    parser = argparse.ArgumentParser(description='Add copyright to files')
    parser.add_argument(
        'includes', type=str, nargs='+', help='directory to add copyright')
    parser.add_argument(
        '--excludes',
        nargs='*',
        type=str,
        default=[],
        help='excludes directory')
    parser.add_argument(
        '--suffixes',
        nargs='*',
        type=str,
        default=['.py'],
        help='copyright will be added to files with suffixes')
    parser.add_argument('--ignore-file-not-found-error', action='store_true')
    args = parser.parse_args()
    return args


def check_args(includes: List[str],
               excludes: List[str],
               suffixes: List[str],
               ignore_file_not_found_error: bool = False):
    """Check the correctness of args and format them."""

    valid_suffixes = {'.py', '.h', '.cpp', '.cu', '.cuh', '.hpp'}

    # remove possible duplication
    includes = list(set(includes))
    excludes = list(set(excludes))
    suffixes = list(set(suffixes))

    # check the correctness and format args
    for i, dir in enumerate(includes):
        if not osp.exists(dir):
            if not ignore_file_not_found_error:
                raise FileNotFoundError(f'Include {dir} can not be found')
        else:
            includes[i] = osp.abspath(dir)

    for i, dir in enumerate(excludes):
        if not osp.exists(dir):
            if not ignore_file_not_found_error:
                raise FileNotFoundError(f'Exclude {dir} can not be found')
        else:
            excludes[i] = osp.abspath(dir)

    for suffix in suffixes:
        if suffix not in valid_suffixes:
            raise ValueError(
                f'Expected suffixes are {valid_suffixes}, but got {suffix}')

    return includes, excludes, suffixes


def get_filepaths(includes: List[str], excludes: List[str],
                  suffixes: List[str]) -> List[str]:
    """Get all file paths that match the args."""

    filepaths = []
    for include in includes:
        for root, _, files in os.walk(include):
            is_exclude = False
            for exclude in excludes:
                if root.startswith(exclude):
                    is_exclude = True
                    break
            if is_exclude:
                continue
            else:
                for file in files:
                    _, ext = osp.splitext(file)
                    if ext in suffixes:
                        filepath = osp.join(root, file)
                        filepaths.append(filepath)
    return filepaths


def check_copyright(includes: List[str],
                    excludes: List[str],
                    suffixes: List[str],
                    ignore_file_not_found_error: bool = False) -> int:
    """Add copyright for those files which lack copyright.

    Args:
        includes: Directory to add copyright.
        excludes: Exclude directory.
        suffixes: Copyright will be added to files with suffixes.
        ignore_file_not_found_error: Whether to ignore `FileNotFoundError` when
            some directories are specified to add copyright but they are not
            found.

    returns:
        Returns 0 if no file is missing copyright, otherwise returns 1.
    """
    rev = 0
    fixed_filepaths = []
    try:
        includes, excludes, suffixes = check_args(includes, excludes, suffixes,
                                                  ignore_file_not_found_error)
    except (FileNotFoundError, ValueError) as e:
        print(repr(e))
        return 1
    else:
        filepaths = get_filepaths(includes, excludes, suffixes)
        for filepath in filepaths:
            with open(filepath, encoding='utf-8') as f:
                lines = f.readlines()
            if not has_copyright(lines):
                fixed_filepaths.append(filepath)
                with open(filepath, 'w', encoding='utf-8') as f:
                    prefix = '# ' if osp.splitext(
                        filepath)[1] == '.py' else '// '
                    f.writelines([prefix + HEADER] + lines)
                    rev = 1
    for filepath in fixed_filepaths:
        print(f'Fixed {filepath}')
    return rev


def main():
    args = parse_args()
    return check_copyright(args.includes, args.excludes, args.suffixes,
                           args.ignore_file_not_found_error)


if __name__ == '__main__':
    raise SystemExit(main())
