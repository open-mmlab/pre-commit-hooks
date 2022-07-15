import os
import os.path as osp

from pre_commit_hooks.check_copyright import check_copyright


def test_copyright():
    includes = ['./tests/data']
    excludes = ['./tests/data/exclude']
    suffixes = ['.py', '.cpp', '.h', '.cu', '.cuh', '.hpp']
    contain_copyright = ['./tests/data/contain_copyright']
    assert check_copyright(includes, excludes, suffixes) == 1

    for dir in includes:
        for root, dirs, files in os.walk(dir):
            for file in files:
                filepath = osp.join(root, file)
                with open(filepath, encoding='utf-8') as f:
                    lines = f.readlines()
                    if root not in excludes:
                        assert lines[0].split(' ').count('Copyright') > 0
                    else:
                        assert lines[0].split(' ').count('Copyright') == 0
                with open(filepath, 'w', encoding='utf-8') as f:
                    if root not in excludes and root not in contain_copyright:
                        f.writelines(lines[1:])
                    else:
                        f.writelines(lines)

    for dir in contain_copyright:
        for root, dirs, files in os.walk(dir):
            for file in files:
                filepath = osp.join(root, file)
                with open(filepath, encoding='utf-8') as f:
                    line = f.readline()
                    assert line.split(' ').count('OpenMMLab.') > 0
